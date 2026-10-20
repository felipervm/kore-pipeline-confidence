import copy,json,pathlib,subprocess,unittest,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from build import evaluate

class BrowserParity(unittest.TestCase):
    def browser(self,rows):
        script="const e=require('./engine');let s='';process.stdin.on('data',d=>s+=d);process.stdin.on('end',()=>{const rows=JSON.parse(s),before=JSON.stringify(rows);const output={results:rows.map(e.evaluate),metrics:e.summarize(rows)};if(before!==JSON.stringify(rows))throw Error('Source changed');process.stdout.write(JSON.stringify(output));});"
        run=subprocess.run(['node','-e',script],cwd=ROOT,input=json.dumps(rows),text=True,encoding='utf-8',capture_output=True,check=True)
        return json.loads(run.stdout)
    def test_original_fixture_and_metrics_match_browser(self):
        data=json.loads((ROOT/'data/results.json').read_text(encoding='utf-8'))
        out=self.browser(data['records'])
        self.assertEqual(out['results'],[evaluate(r) for r in data['records']])
        m=out['metrics'];s=data['summary']
        self.assertEqual([m['total'],m['review'],m['passed'],m['reported'],m['strict']],[s['records'],s['review'],s['passed'],s['reported_open_arr_cad'],s['validated_open_arr_cad']])
        self.assertEqual({k:v for k,v in m['counts'].items() if v},s['flags'])
    def test_boundaries_dormant_approval_and_priority_match(self):
        data=json.loads((ROOT/'data/results.json').read_text(encoding='utf-8'))
        base=next(r for r in data['records'] if r['status']=='Pass' and r['stage']=='Proposal')
        cases=[]
        for value in ['0','-1','','25000','1.5',' 25000 ']:cases.append({**base,'estimated_arr_cad':value})
        for date in ['2026-10-19','2026-10-20','2026-10-21']:cases.append({**base,'close_date':date})
        cases.append({**base,'stage':'Closed Won','probability_pct':'100','estimated_arr_cad':'25000','contract_arr_cad':'25000','approval_status':'Pending'})
        cases.append({**base,'owner':'  ','next_step':'','estimated_arr_cad':'','close_date':'2026-09-01'})
        before=copy.deepcopy(cases);out=self.browser(cases)
        self.assertEqual(out['results'],[evaluate(r) for r in cases]);self.assertEqual(cases,before)
        self.assertIn('APPROVAL_PENDING',[i['code'] for i in out['results'][-2]['issues']])
