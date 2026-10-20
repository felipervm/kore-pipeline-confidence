import unittest,sys,pathlib,csv,json,copy
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from build import evaluate,main
class ValidationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  main()
  with (ROOT/'data/opportunities.csv').open() as f:cls.rows=list(csv.DictReader(f))
 def good(self):return dict(opportunity_id='TEST',account='X',segment='Industrial IoT',owner='Seller A',stage='Proposal',close_date='2026-12-20',estimated_arr_cad='25000',contract_arr_cad='',probability_pct='50',last_updated='2026-10-20',next_step='Call buyer',approval_status='Pending')
 def test_dataset_size(self):self.assertEqual(len(self.rows),120)
 def test_clean_record(self):self.assertEqual(evaluate(self.good())['status'],'Pass')
 def test_missing_owner(self):
  r=self.good();r['owner']='';self.assertIn('MISSING_OWNER',[x['code'] for x in evaluate(r)['issues']])
 def test_missing_next_step(self):
  r=self.good();r['next_step']='';self.assertIn('MISSING_NEXT_STEP',[x['code'] for x in evaluate(r)['issues']])
 def test_missing_arr(self):
  r=self.good();r['estimated_arr_cad']='';self.assertIn('INVALID_ARR',[x['code'] for x in evaluate(r)['issues']])
 def test_negative_arr(self):
  r=self.good();r['estimated_arr_cad']='-5';self.assertIn('INVALID_ARR',[x['code'] for x in evaluate(r)['issues']])
 def test_probability(self):
  r=self.good();r['probability_pct']='90';self.assertIn('STAGE_PROBABILITY_MISMATCH',[x['code'] for x in evaluate(r)['issues']])
 def test_past_close(self):
  r=self.good();r['close_date']='2026-09-01';self.assertIn('PAST_DUE_CLOSE',[x['code'] for x in evaluate(r)['issues']])
 def test_won_mismatch(self):
  r=self.good();r.update(stage='Closed Won',probability_pct='100',contract_arr_cad='24000');self.assertIn('WON_VALUE_MISMATCH',[x['code'] for x in evaluate(r)['issues']])
 def test_won_requires_approval(self):
  r=self.good();r.update(stage='Closed Won',probability_pct='100',contract_arr_cad='25000');self.assertIn('APPROVAL_PENDING',[x['code'] for x in evaluate(r)['issues']])
 def test_does_not_mutate(self):
  r=self.good();original=copy.deepcopy(r);evaluate(r);self.assertEqual(r,original)
 def test_published_counts(self):
  published=json.loads((ROOT/'data/results.json').read_text());self.assertEqual(published['summary']['review'],sum(evaluate(r)['status']=='Needs review' for r in self.rows))
if __name__=='__main__':unittest.main()
