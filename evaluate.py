"""Evaluate a frozen model against assistant-reviewed labels. Inputs remain private."""
import argparse,json,math,csv,hashlib
from pathlib import Path
from collections import Counter,defaultdict
from src.core import classify,load_model

def wilson(k,n):
    if not n:return [0,1]
    z=1.96;p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [round(c-h,4),round(c+h,4)]

def evaluate(path,out):
    labels=json.loads(Path(path).read_text());model=load_model();results=[];conf=Counter();bycat=defaultdict(Counter)
    for row in labels:
        if not row.get('reviewed_category'):raise ValueError('Every row must have a reviewed_category')
        pred=classify(row['customer_message'],model);gold=row['reviewed_category'];accepted=pred['category']!='Needs review';correct=pred['category']==gold
        results.append({'ticket_id':row['ticket_id'],'reviewed_category':gold,'predicted_category':pred['category'],'suggested_category':pred['suggested_category'],'score':pred['score'],'margin':pred['margin'],'accepted':accepted,'correct':correct})
        conf[(gold,pred['category'])]+=1;bycat[gold]['n']+=1;bycat[gold]['correct']+=int(correct);bycat[gold]['abstained']+=int(not accepted)
    retrospective=[]
    for row in labels:
        a=classify(row['customer_message'],model);b=classify(row['customer_message']+' '+row['agent_notes'],model)
        disagree=a['category']!='Needs review' and b['category']!='Needs review' and a['category']!=b['category']
        category='Needs review' if disagree else b['category']
        retrospective.append((category, row['reviewed_category']))
    rn=sum(a!='Needs review' for a,b in retrospective);re=sum(a!='Needs review' and a!=b for a,b in retrospective)
    n=len(results);accepted=sum(r['accepted'] for r in results);errors=sum(r['accepted'] and not r['correct'] for r in results);abstained=n-accepted
    digest=hashlib.sha256(Path('src/core.py').read_bytes()).hexdigest();freeze=json.loads(Path('docs/model-freeze.json').read_text())
    if freeze['sha256']!=digest:raise ValueError('Frozen classifier changed: mark this sample as development and create a new holdout')
    report={'sample_size':n,'sampling':'Seeded simple random sample (seed 20261004) from 11,541 reporting-window rows after excluding 100 previously viewed development records; uniform ticket sampling, no category balancing.',
      'reviewer':'ChatGPT/Codex assistant; manually read customer opening and closing note with exported tags and teams hidden. Reviewed labels assigned before computing frozen-model predictions. Not independent human ground truth.',
      'feature_mode':'Opening text only; reviewed labels may use closing note to establish root issue. This exposes opening-text ambiguity rather than removing it.',
      'retrospective':{'accepted':rn,'abstained':len(labels)-rn,'wrong_accepted':re,'coverage':rn/len(labels),'error_rate_among_accepted':re/rn if rn else None,'wrong_accepted_wilson_95_interval':wilson(re,rn),'note':'Opening plus closing notes; disagreements abstain. These figures are retrospective only.'},
      'model_sha256':digest,'accepted':accepted,'abstained':abstained,'coverage':accepted/n,'wrong_accepted':errors,'error_rate_among_accepted':errors/accepted if accepted else None,
      'wrong_accepted_wilson_95_interval':wilson(errors,accepted),'errors_plus_abstentions':errors+abstained,'non_correct_or_review_rate':(errors+abstained)/n,
      'per_category':dict(bycat),'confusion':[{'reviewed':g,'predicted':p,'count':count} for (g,p),count in sorted(conf.items())],
      'failure_examples':[{k:r[k] for k in ['ticket_id','reviewed_category','predicted_category','suggested_category','score','margin']} for r in results if not r['correct']],
      'limitations':['Same AI assistant authored classifier and reference labels; correlated interpretation errors are possible.','No independent Vireo agent adjudication; production accuracy is unproven.','Small sample; no assurance for classes absent from the sample.','Synthetic example similarity is not calibrated probability; thresholds are heuristic.','Repeated templates can make ticket-random validation easier than future, genuinely novel messages.']}
    out=Path(out);out.mkdir(exist_ok=True,parents=True)
    for i,r in enumerate(report['failure_examples']):r['sample_case_id']='review-case-'+str(i+1);r.pop('ticket_id',None)
    (out/'validation.json').write_text(json.dumps(report,indent=2))
    with open(out/'evaluation_rows_PRIVATE.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
    return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--labels',default='data/evaluation_labels_PRIVATE.json');p.add_argument('--out',default='output');a=p.parse_args();print(json.dumps(evaluate(a.labels,a.out),indent=2))
