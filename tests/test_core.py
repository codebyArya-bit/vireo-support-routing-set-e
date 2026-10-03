import unittest
from datetime import datetime
from src.core import parse_time, resolution_time, roster_team, classify, load_model, business_case

class CoreTests(unittest.TestCase):
    def test_legacy_resolution_is_utc(self):
        r={'resolved_at':'2025-03-01 04:30','source_system':'legacy_fd'}
        self.assertEqual(resolution_time(r),datetime(2025,3,1,10))
        r['source_system']='helpdesk'
        self.assertEqual(resolution_time(r),datetime(2025,3,1,4,30))
    def test_missing_timestamp(self):
        self.assertIsNone(parse_time(''))
        self.assertIsNone(parse_time('invalid'))
    def test_dated_roster_and_ambiguity(self):
        rows=[{'agent_id':'A1','team':'Billing','from_date':'2025-01-01','to_date':'2025-02-01'}, {'agent_id':'A1','team':'Logistics','from_date':'2025-02-02','to_date':''}]
        self.assertEqual(roster_team('A1',datetime(2025,2,3),rows),'Logistics')
        self.assertEqual(roster_team('A1',datetime(2025,1,12),rows),'Billing')
        self.assertEqual(roster_team('A1',datetime(2024,1,12),rows),'Unknown')
        self.assertEqual(roster_team('A1',datetime(2025,2,3),rows+rows),'Unknown')
    def test_ambiguous_and_unseen_text(self):
        m=load_model()
        self.assertEqual(classify('',m)['category'],'Needs review')
        self.assertEqual(classify('asdf qwerty purple banana',m)['category'],'Needs review')
    def test_payment_vs_delivery_and_refund(self):
        m=load_model()
        self.assertEqual(classify('Payment successful but order not delivered',m)['suggested_category'],'Delivery & Shipping')
        self.assertEqual(classify('Money debited but order not showing',m)['suggested_category'],'Billing & Payments')
        self.assertEqual(classify('Still waiting for my refund',m)['suggested_category'],'Returns & Refunds')
    def test_savings_arithmetic(self):
        b=business_case(100,1000,.5)
        self.assertEqual(b['observed_quarter_target_inr'],15250)
        self.assertEqual(b['at_vireo_quarter_target_inr'],128862.5)

if __name__=='__main__': unittest.main()
