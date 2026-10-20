import csv,json,random,datetime,pathlib,collections
ROOT=pathlib.Path(__file__).resolve().parents[1]
(ROOT/'data').mkdir(exist_ok=True)
random.seed(20261020)
stages=['Prospecting','Qualification','Proposal','Negotiation','Closed Won','Closed Lost']
owners=['Jordan Lee','Taylor Morgan','Alex Chen','Sam Rivera','Casey Patel','Morgan Blake']
segments=['Fleet Telematics','Industrial IoT','Healthcare Devices','Smart Logistics','Connected Retail']
rows=[]
for i in range(1,121):
 stage=random.choices(stages,[12,19,32,25,18,14])[0]
 arr=random.randrange(12,260)*1000
 close=datetime.date(2026,10,20)+datetime.timedelta(days=random.randint(-60,100))
 probability={'Prospecting':10,'Qualification':25,'Proposal':50,'Negotiation':75,'Closed Won':100,'Closed Lost':0}[stage]
 row=dict(opportunity_id=f'KPC-{i:04d}',account=f'Synthetic Account {i:03d}',segment=random.choice(segments),owner=random.choice(owners),stage=stage,close_date=str(close),estimated_arr_cad=str(arr),contract_arr_cad=str(arr if stage=='Closed Won' else ''),probability_pct=str(probability),last_updated=str(datetime.date(2026,10,20)-datetime.timedelta(days=random.randint(0,45))),next_step=random.choice(['Confirm scope','Review proposal','Customer follow-up','Validate commercial terms']),approval_status='Approved' if stage in ['Closed Won','Closed Lost'] else random.choice(['Pending','Approved']),data_origin='Synthetic fixture')
 if i%9==0:row['close_date']='2026-09-15'
 if i%11==0:row['next_step']=''
 if i%13==0:row['estimated_arr_cad']=''
 if i%17==0:row['probability_pct']='90'
 if i%19==0:row['owner']=''
 if i%23==0 and stage=='Closed Won':row['contract_arr_cad']=str(arr+5000)
 rows.append(row)
FIELDS=list(rows[0])
def evaluate(row,as_of=datetime.date(2026,10,20)):
 issues=[]
 def add(code,priority,owner,action):issues.append(dict(code=code,priority=priority,action_owner=owner,action=action))
 if not row['owner'].strip():add('MISSING_OWNER','High','Sales Operations','Assign opportunity owner')
 if not row['next_step'].strip() and row['stage'] not in ('Closed Won','Closed Lost'):add('MISSING_NEXT_STEP','Medium','Opportunity owner','Enter a specific next action')
 try: value=int(row['estimated_arr_cad']);assert value>=0
 except (ValueError,AssertionError):add('INVALID_ARR','High','Revenue Operations','Verify estimated annualized revenue against commercial source')
 expected={'Prospecting':10,'Qualification':25,'Proposal':50,'Negotiation':75,'Closed Won':100,'Closed Lost':0}.get(row['stage'])
 if expected is None or row['probability_pct']!=str(expected):add('STAGE_PROBABILITY_MISMATCH','Medium','Opportunity owner','Confirm stage and probability assumptions')
 if row['stage'] not in ('Closed Won','Closed Lost') and datetime.date.fromisoformat(row['close_date'])<as_of:add('PAST_DUE_CLOSE','Medium','Opportunity owner','Confirm realistic close date')
 if row['stage']=='Closed Won':
  try: valid=int(row['contract_arr_cad'])==int(row['estimated_arr_cad'])
  except ValueError:valid=False
  if not valid:add('WON_VALUE_MISMATCH','High','Revenue Operations','Reconcile won contract value with estimated ARR')
  if row['approval_status']!='Approved':add('APPROVAL_PENDING','High','Deal Desk','Verify commercial approval before finalizing')
 order={'High':0,'Medium':1,'Low':2}
 issues.sort(key=lambda x:(order[x['priority']],x['code']))
 return {'status':'Needs review' if issues else 'Pass','issues':issues,'next_owner':issues[0]['action_owner'] if issues else 'None','next_action':issues[0]['action'] if issues else 'No action required'}
def main():
 with (ROOT/'data/opportunities.csv').open('w',newline='',encoding='utf8') as f:
  w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
 results=[dict(**r,**evaluate(r)) for r in rows]
 counts=collections.Counter(j['code'] for r in results for j in r['issues'])
 valid_open=[r for r in results if r['status']=='Pass' and r['stage'] not in ('Closed Won','Closed Lost')]
 reported=sum(int(r['estimated_arr_cad']) for r in rows if r['stage'] not in ('Closed Won','Closed Lost') and r['estimated_arr_cad'].isdigit())
 verified=sum(int(r['estimated_arr_cad']) for r in valid_open)
 summary=dict(records=len(rows),review=sum(r['status']=='Needs review' for r in results),passed=sum(r['status']=='Pass' for r in results),reported_open_arr_cad=reported,validated_open_arr_cad=verified,flags=dict(sorted(counts.items())),as_of='2026-10-20',method='Illustrative strict pass-only subset; not a revised forecast or KORE internal metric')
 (ROOT/'data/results.json').write_text(json.dumps({'summary':summary,'records':results},indent=2),encoding='utf8')
 print(summary)
if __name__=='__main__': main()
