import unittest,csv,tempfile,json,shutil
from pathlib import Path
from src.analysis import run
ROOT=Path(__file__).resolve().parents[1]

class AnalysisTests(unittest.TestCase):
    def test_reconciliation_window_and_missing_transfers(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp)/'data';shutil.copytree(ROOT/'demo-data',d)
            with open(d/'tickets.csv') as f:rows=list(csv.DictReader(f));fields=list(rows[0])
            rows[0]['transfers']=''
            old=dict(rows[1]);old['ticket_id']='OLD';old['created_at']='2024-12-31 23:59';rows.append(old)
            rows[2]['resolved_at']='2026-01-01 00:00'
            with open(d/'tickets.csv','w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
            out=Path(tmp)/'out';s=run(d,out)
            self.assertEqual(s['tickets'],12)
            self.assertEqual(s['diagnostics']['outside_window'],1)
            self.assertEqual(s['diagnostics']['unknown_transfers'],1)
            self.assertEqual(s['diagnostics']['invalid_resolution_chronology'],1)
            self.assertEqual(s['business_case']['opportunities'],0)
            with open(out/'monthly_breakdown.csv') as f:monthly=list(csv.DictReader(f))
            for basis in set(r['basis'] for r in monthly):self.assertEqual(sum(int(r['tickets']) for r in monthly if r['basis']==basis),12)
            with open(out/'classified_tickets_PRIVATE.csv') as f:enriched=list(csv.DictReader(f))
            self.assertEqual(enriched[0]['transfers_known'],'')
            self.assertEqual(enriched[2]['resolution_hours'],'')
            self.assertNotIn('customer_message',json.dumps(json.loads((out/'summary.json').read_text())))
    def test_duplicate_ticket_id_does_not_inflate_totals(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp)/'data';shutil.copytree(ROOT/'demo-data',d)
            with open(d/'tickets.csv') as f:rows=list(csv.DictReader(f));fields=list(rows[0])
            rows.append(dict(rows[0]))
            with open(d/'tickets.csv','w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
            s=run(d,Path(tmp)/'out')
            self.assertEqual(s['tickets'],12)
            self.assertEqual(s['diagnostics']['duplicate_ticket_id_rows'],1)
            self.assertEqual(s['business_case']['opportunities'],1)

if __name__=='__main__':unittest.main()
