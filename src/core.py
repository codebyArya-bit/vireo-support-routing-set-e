"""Offline supervised text classifier and policy-based data utilities."""
import csv, json, math, re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timedelta
ROOT = Path(__file__).resolve().parents[1]

SYNTHETIC = {
'Delivery & Shipping': [
'order not delivered tracking not updating shipment not received delivery delayed dlvry delayed ord not delivered',
'payment successful but order not delivered paid but package not delivered',
'paid confirmed then nothing days and counting still waiting for something to show up',
'money gone from account item not with me nothing at my door doorstep says otherwise box never came',
'courier marked delivered but nobody received package lost in transit',
'wrong item delivered incorrect product shipped wrong colour wrong variant received',
'product arrived damaged box crushed unit cracked damaged in transit',
'order status stuck on shipped tracking out for delivery courier AWB logistics reshipped RTO',
'payment went through but order has not gone through front door transaction done where is my stuff',
'it has been days and I have nothing in hand havent received my order payment was done parcel stuck'],
'Billing & Payments': [
'money debited but order not showing payment deducted no order created payment debited no order',
'payment went through but no order id no order confirmation UPI success app shows nothing',
'bank says money went to you but site says no orders amount deducted without order',
'page failed after I paid nothing shows in account failed order after payment',
'charged twice double charge duplicate payment card charged two times',
'GST invoice request GSTIN tax bill invoice not downloading invoice PDF link 404',
'coupon code not working discount not applied checkout promo code invalid price adjustment'],
'Returns & Refunds': [
'still waiting for my refund refund not credited refund promised days ago nothing checked bank',
'refund delay refund pending rfnd not credited rfnd pending ARN shared refund reprocessed',
'return pickup has not happened reverse pickup pending pkp missed pickup not done nobody came',
'pickup scheduled but no one showed up rescheduled pickup twice app said pickup today',
'where is the money for the return checked reverse pickup QC status'],
'Charging & Battery': [
'left earbud not charging right one fine left bud not taking charge L bud no charge in case',
'case no LED no charge case dead no light when plugged in plugging in does nothing',
'battery draining fast battery drains very fast barely lasts hours poor battery backup',
'battery life dropped almost nothing battery draining even when not in use',
'case same battery level for a week charging case dead LED dead'],
'Connectivity': [
'Bluetooth keeps cutting out connection dropping random disconnects during calls bt dropouts',
'cannot pair device laptop pairing failure not discoverable forget re pair',
'connects for a second then vanishes from device list silent for a second every few minutes comes back',
'Wifi setup fails last step unable connect wifi router band interference'],
'Audio Quality': [
'static noise playing music buzzing sound speaker audio distortion',
'works for music useless for meetings callers asking repeat low mic pickup microphone',
'no sound right earbud music in one ear only other mute single side audio no audio one side',
'sound too low audio muffled poor sound crackling speaker'],
'App & Firmware': [
'app crashes device settings app crashing app crash device page',
'firmware update stuck update hang recovery mode update failed',
'since last update app white screen app not opening android bug device settings',
'app sync data not updating step count not syncing firmware issue'],
'Account & Login': [
'OTP not coming login code never arrives unable log in account locked',
'site says sent code phone disagrees login issue account unlocked password reset',
'cannot sign in login registration phone number update authentication'],
'Warranty & Repair': [
'claim number RMA anyone alive there warranty claim status wty claim status',
'service centre took device now silence no update on repair repair status follow up',
'warranty repair RMA status QC report repair completed shipped back'],
'Product Enquiry': [
'will this survive shower waterproof water resistance pre sales query compatibility',
'dad old Nokia will watch app run compatible TV iPhone compatibility query',
'product specifications spec sheet shared compatibility info product enquiry'],
'Cancellation & Order Changes': [
'want cancel order cancel button greyed out cancellation request',
'please cancel ordered by mistake son ordered without asking please reverse',
'cancel order cancelled before dispatch already shipped advised RTO return',
'change delivery address modify order before dispatch'],
'Hardware & Controls': [
'screen unresponsive display hard reset touch not responding',
'have to tap ten times for one swipe to register touchscreen issue',
'button broken device will not power on hardware controls unresponsive'],
}
STOP = set('the a an is are was were this that my your our i me you it in on at to of for and but with from has have had been not no please dear hi hello team thanks regards kindly product order purchased issue tried expected customer cx says reported reached contact states ticket raised informed closed consent confirmed checked advised done resolved'.split())

def clean(s):
    s = str(s or '').lower().replace('\\n',' ')
    s = re.sub(r'\b(?:vr|tk|c|a)\d[\w-]*\b',' ',s)
    s = re.sub(r'\d+',' ',s)
    return ' '.join(re.findall(r'[a-z]+',s))

def features(s):
    words = [w for w in clean(s).split() if w not in STOP and len(w)>1]
    c=Counter('w:'+w for w in words)
    c.update('b:'+a+' '+b for a,b in zip(words,words[1:]))
    for w in words:
        padded='^'+w+'$'
        c.update('c:'+padded[i:i+3] for i in range(len(padded)-2))
    return c

def load_model():
    docs=[(category,text) for category,texts in SYNTHETIC.items() for text in texts]
    counts=[features(text) for _,text in docs];df=Counter()
    for c in counts: df.update(c.keys())
    idf={k:math.log((len(docs)+1)/(v+1))+1 for k,v in df.items()}
    def vector(c):
        v={k:(1+math.log(n))*idf[k]*(.35 if k.startswith('c:') else 1) for k,n in c.items() if k in idf}
        norm=math.sqrt(sum(n*n for n in v.values()))
        return {k:n/norm for k,n in v.items()} if norm else {}
    return {'idf':idf,'vectors':[(cat,text,vector(c)) for (cat,text),c in zip(docs,counts)],'vector':vector,'examples':len(docs)}

def classify(text,model=None):
    model=model or load_model();v=model['vector'](features(text));scores=defaultdict(float);best={}
    for cat,example,proto in model['vectors']:
        score=sum(n*proto.get(k,0) for k,n in v.items())
        if score>scores[cat]: scores[cat]=score;best[cat]=example
    ranking=sorted(scores.items(),key=lambda t:(-t[1],t[0]))
    if not ranking: return {'category':'Needs review','suggested_category':'Needs review','score':0.,'margin':0.,'evidence':''}
    cat,score=ranking[0];margin=score-(ranking[1][1] if len(ranking)>1 else 0)
    accepted=score>=.27 and margin>=.035
    return {'category':cat if accepted else 'Needs review','suggested_category':cat,'score':round(score,4),'margin':round(margin,4),'evidence':best.get(cat,'')}

def parse_time(s):
    try:return datetime.fromisoformat(str(s)) if s else None
    except (ValueError,TypeError):return None

def resolution_time(r):
    value=parse_time(r.get('resolved_at'))
    return value+timedelta(hours=5,minutes=30) if value and r.get('source_system')=='legacy_fd' else value

def roster_team(agent_id,when,roster):
    if not when:return 'Unknown'
    hits=[r for r in roster if r['agent_id']==agent_id and (not r.get('from_date') or when.date()>=datetime.fromisoformat(r['from_date']).date()) and (not r.get('to_date') or when.date()<=datetime.fromisoformat(r['to_date']).date())]
    return hits[0]['team'] if len(hits)==1 else 'Unknown'

def read_csv(path):
    with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def business_case(opportunities,total,avoidance=.5):
    rate=opportunities/total if total else 0
    return {'opportunities':opportunities,'quarter_tickets':total,'opportunity_rate':rate,'avoidance_assumption':avoidance,'transfer_cost_inr':305,'observed_quarter_target_inr':opportunities*avoidance*305,'vireo_weekly_tickets_assumption':650,'at_vireo_quarter_tickets':650*13,'at_vireo_quarter_target_inr':650*13*rate*avoidance*305,'observed_quarter_full_potential_inr':opportunities*305}

if __name__=='__main__':
    print(json.dumps(classify('Payment successful but order not delivered'),indent=2))
