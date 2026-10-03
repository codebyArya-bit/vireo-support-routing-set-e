"""Read the pack and write reconciled reporting outputs. No external dependencies."""
import csv,json,hashlib,time
from collections import Counter,defaultdict
from datetime import datetime
from pathlib import Path
from statistics import median,mean
from .core import read_csv,parse_time,resolution_time,roster_team,classify,load_model,business_case,clean

START=datetime(2025,1,1);END=datetime(2026,7,1)
SLA={'chat':15,'email':480,'voice':120,'social':240}

def locate(folder,name):
    matches=sorted(Path(folder).glob('*'+name))
    exact=Path(folder)/name
    if exact.is_file():return exact
    matches=[p for p in matches if '(1)' not in p.name]
    if len(matches)!=1:raise ValueError(f'Expected one {name}; found {len(matches)}. Use canonical filenames.')
    return matches[0]

def write_csv(path,rows,fields=None):
    if not rows and not fields:return
    fields=fields or list(rows[0])
    with open(path,'w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def run(data_dir,out_dir):
    began=time.perf_counter();out=Path(out_dir);out.mkdir(parents=True,exist_ok=True)
    paths={name:locate(data_dir,name) for name in ['tickets.csv','agents.csv','products.csv','orders.csv','customers.csv']}
    raw=read_csv(paths['tickets.csv']);roster=read_csv(paths['agents.csv']);model=load_model()
    products={r['sku']:r for r in read_csv(paths['products.csv'])};customers={r['customer_id'] for r in read_csv(paths['customers.csv'])};orders={r['order_id']:r for r in read_csv(paths['orders.csv'])}
    diagnostics=Counter(raw_rows=len(raw));seen={};kept=[];suspects=[]
    for row in raw:
        key=row['ticket_id']
        if key in seen:
            diagnostics['duplicate_ticket_id_rows']+=1
            if row['source_system']=='helpdesk' and seen[key]['source_system']!='helpdesk':seen[key]=row
        else:seen[key]=row
    for row in seen.values():
        created=parse_time(row['created_at'])
        if not created:diagnostics['invalid_created_at']+=1;continue
        if not START<=created<END:diagnostics['outside_window']+=1;continue
        kept.append(row)
    fingerprints=defaultdict(list)
    for r in kept:
        fingerprints[(r['customer_id'],r['product_sku'],r['order_id'],clean(r['customer_message']),r['created_at'])].append(r['ticket_id'])
    for ids in fingerprints.values():
        if len(ids)>1:suspects.append({'ticket_ids':' | '.join(ids),'reason':'same customer, SKU, order, message and creation timestamp'})
    diagnostics['exact_event_duplicate_groups']=len(suspects)
    # Different IDs are not silently removed: a repeat contact may be a genuine new attendance.
    enriched=[];monthly=defaultdict(Counter)
    for r in kept:
        created=parse_time(r['created_at']);first=parse_time(r['first_response_at']);resolved=resolution_time(r)
        completed=r['status'] in ('resolved','closed');valid_resolution=bool(completed and resolved and resolved>=created and (not first or resolved>=first))
        if r['source_system']=='legacy_fd' and resolved:diagnostics['legacy_resolution_corrected']+=1
        if resolved and (resolved<created or (first and resolved<first)):diagnostics['invalid_resolution_chronology']+=1
        if completed and not resolved:diagnostics['completed_without_resolution_time']+=1
        team=roster_team(r['agent_id'],resolved if completed and resolved else created,roster)
        if team=='Unknown':diagnostics['unmatched_or_ambiguous_roster']+=1
        delta=(first-created).total_seconds()/60 if first else None
        valid_first=delta is not None and delta>=0 and r['channel'] in SLA
        if not valid_first:diagnostics['invalid_or_missing_first_response']+=1
        breach=bool(valid_first and delta>SLA[r['channel']])
        opening=classify(r['customer_message'],model)
        historical=classify(r['customer_message']+' '+r['agent_notes'],model)
        disagreement=opening['category']!='Needs review' and historical['category']!='Needs review' and opening['category']!=historical['category']
        retrospective='Needs review' if disagreement else historical['category']
        if disagreement:diagnostics['opening_closing_disagreement']+=1
        transfer=None
        if r['transfers'].strip():
            try:transfer=float(r['transfers']);transfer=transfer if transfer>=0 else None
            except ValueError:pass
        else:diagnostics['unknown_transfers']+=1
        if r['customer_id'] not in customers:diagnostics['unknown_customer_id']+=1
        if r['product_sku'] not in products:diagnostics['unknown_sku']+=1
        if r['order_id']:
            if r['order_id'] not in orders:diagnostics['unknown_order_id']+=1
            elif orders[r['order_id']]['customer_id']!=r['customer_id'] or orders[r['order_id']]['sku']!=r['product_sku']:diagnostics['order_customer_or_sku_mismatch']+=1
        else:diagnostics['missing_order_id']+=1
        month=created.strftime('%Y-%m');shift='Morning' if 6<=created.hour<14 else 'Day' if 14<=created.hour<22 else 'Night'
        resolution_hours=(resolved-created).total_seconds()/3600 if valid_resolution else None
        csat=None
        if r['csat_score'].strip():
            try:csat=float(r['csat_score']);csat=csat if 1<=csat<=5 else None
            except ValueError:pass
        e={**r,'month':month,'recorded_agent_team':team,'completed':completed,'resolved_ist':resolved.isoformat(sep=' ') if resolved else '',
           'resolution_hours':resolution_hours,'first_response_minutes':delta if valid_first else None,'sla_breach':breach,'created_shift_ist':shift,'transfers_known':transfer,
           'intake_ai_category':opening['category'],'intake_suggestion':opening['suggested_category'],'intake_score':opening['score'],'intake_margin':opening['margin'],
           'retrospective_ai_category':retrospective,'opening_closing_disagreement':disagreement,'csat_valid':csat}
        enriched.append(e)
        for basis,category in [('Exported tag',r['category']),('Opening text',opening['category']),('Opening + closing text',retrospective),('First assigned team',r['assigned_team']),('Recorded agent team',team)]:monthly[(month,basis)][category]+=1
    cross=Counter((r['month'],r['assigned_team'],r['recorded_agent_team'],r['category'],r['intake_ai_category'],r['retrospective_ai_category']) for r in enriched)
    cross_rows=[dict(zip(['month','initial_team','recorded_agent_team','exported_tag','opening_category','retrospective_category','tickets'],(*key,n))) for key,n in sorted(cross.items())]
    monthly_rows=[{'month':m,'basis':b,'category':cat,'tickets':n} for (m,b),counts in sorted(monthly.items()) for cat,n in sorted(counts.items())]
    q2=[r for r in enriched if '2026-04'<=r['month']<='2026-06']
    # Conservative eligible opportunity: current system, completed, one recorded transfer,
    # unambiguous opening-text delivery classification and Logistics recorded resolving team.
    opportunities=[r for r in q2 if r['source_system']=='helpdesk' and r['completed'] and r['assigned_team']=='Billing' and r['recorded_agent_team']=='Logistics' and r['intake_ai_category']=='Delivery & Shipping' and r['transfers_known'] is not None and r['transfers_known']>=1]
    case=business_case(len(opportunities),len(q2))
    case.update({'billing_q2_tickets':sum(r['assigned_team']=='Billing' for r in q2),'period':'2026-04-01 to 2026-06-30','ticket_ids':[r['ticket_id'] for r in opportunities],
        'eligible_definition':'Q2 current-system completed tickets: initial Billing, unambiguous opening-text Delivery, recorded Logistics resolver, >=1 known transfer. One avoided hand-off per eligible ticket.',
        'sensitivity':[{ 'avoidance':rate, 'observed_quarter_inr':len(opportunities)*rate*305,'at_vireo_quarter_inr':650*13*case['opportunity_rate']*rate*305} for rate in [.25,.5,.75]]})
    if case['billing_q2_tickets']:case['billing_opportunity_share']=len(opportunities)/case['billing_q2_tickets']
    team_stats=[]
    for team in sorted(set(r['recorded_agent_team'] for r in enriched)):
        rs=[r for r in enriched if r['recorded_agent_team']==team];dur=[r['resolution_hours'] for r in rs if r['resolution_hours'] is not None];cs=[r['csat_valid'] for r in rs if r['csat_valid'] is not None]
        team_stats.append({'team':team,'recorded_agent_tickets':len(rs),'completed':sum(r['completed'] for r in rs),'resolution_time_n':len(dur),'median_resolution_hours':round(median(dur),2) if dur else None,'csat_n':len(cs),'csat_mean':round(mean(cs),2) if cs else None,'note':'Resolution elapsed time includes customer/courier waiting; not agent handle hours. Tier 2 is not comparable to Tier 1.'})
    summary={'data_kind':'synthetic_demo' if enriched and all(r['ticket_id'].startswith('DEMO-') for r in enriched) else 'supplied_vireo_pack','window':'Jan 2025 - Jun 2026 (creation month, IST)','tickets':len(enriched),'completed':sum(r['completed'] for r in enriched),
        'initial_teams':dict(Counter(r['assigned_team'] for r in enriched)),'recorded_agent_teams':dict(Counter(r['recorded_agent_team'] for r in enriched)),
        'intake_categories':dict(Counter(r['intake_ai_category'] for r in enriched)),'retrospective_categories':dict(Counter(r['retrospective_ai_category'] for r in enriched)),
        'diagnostics':dict(diagnostics),'business_case':case,'team_stats':team_stats,
        'sla':{'first_response_breaches':sum(r['sla_breach'] for r in enriched),'valid_first_response_n':sum(r['first_response_minutes'] is not None for r in enriched),'credit_eligible_completed_breaches':sum(r['sla_breach'] and r['completed'] for r in enriched),'policy_credit_exposure_inr':350*sum(r['sla_breach'] and r['completed'] for r in enriched),'note':'Policy exposure, not reconciled issued cash or incremental routing savings. Attribution to initial queue, not resolving agent.'},
        'classifier':{'type':'TF-IDF nearest synthetic example; word, word-pair and character-trigram features','examples':model['examples'],'score_threshold':.27,'margin_threshold':.035,'scores_are_probabilities':False},
        'input_sha256':{name:hashlib.sha256(p.read_bytes()).hexdigest() for name,p in paths.items()}}
    summary['run_seconds']=round(time.perf_counter()-began,3)
    write_csv(out/'classified_tickets_PRIVATE.csv',enriched)
    write_csv(out/'monthly_breakdown.csv',monthly_rows)
    write_csv(out/'monthly_category_team.csv',cross_rows)
    write_csv(out/'duplicate_candidates_PRIVATE.csv',suspects,['ticket_ids','reason'])
    write_csv(out/'team_metrics.csv',team_stats)
    (out/'summary_PRIVATE.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    public=json.loads(json.dumps(summary));public['business_case'].pop('ticket_ids')
    (out/'summary.json').write_text(json.dumps(public,indent=2),encoding='utf-8')
    from .dashboard import make_dashboard
    make_dashboard(public,monthly_rows,out/'dashboard.html',cross_rows)
    return summary
