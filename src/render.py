from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'data/results.json').read_text(encoding='utf-8'))
rules=[
 {'id':'PAST_DUE_CLOSE','name':'Close date needs review','owner':'Opportunity owner','action':'Confirm a realistic close date.','definition':'An open opportunity has a close date before 20 October 2026.'},
 {'id':'MISSING_NEXT_STEP','name':'Next step is missing','owner':'Opportunity owner','action':'Record a specific seller next action.','definition':'An open opportunity has an empty or whitespace-only next step.'},
 {'id':'INVALID_ARR','name':'Annualized value is invalid','owner':'Revenue Operations','action':'Verify the value against its commercial source.','definition':'The illustrative value cannot be parsed as an integer or is negative. Zero is allowed in this original simplified model. Legacy ARR field name; not KORE eARR.'},
 {'id':'STAGE_PROBABILITY_MISMATCH','name':'Stage and probability disagree','owner':'Opportunity owner','action':'Confirm stage and probability assumptions.','definition':'Probability does not match the demo defaults: Prospecting 10%, Qualification 25%, Proposal 50%, Negotiation 75%, Closed Won 100%, Closed Lost 0%.'},
 {'id':'MISSING_OWNER','name':'Seller owner is missing','owner':'Sales Operations','action':'Confirm and assign the responsible seller.','definition':'Opportunity owner is empty or whitespace-only.'},
 {'id':'WON_VALUE_MISMATCH','name':'Won value needs reconciliation','owner':'Revenue Operations','action':'Reconcile won contract annual value and estimated annualized value.','definition':'A Closed Won record has unequal integer contract/opportunity values, or either cannot be parsed as an integer.'},
 {'id':'APPROVAL_PENDING','name':'Won approval requires review','owner':'Deal Desk','action':'Verify commercial approval before finalizing.','definition':'A Closed Won record does not have Approved commercial status. Pending approvals on open records are not flagged by this model.'}
]
spec={'asOf':'2026-10-20','rules':rules,'currency':'CAD'}
(ROOT/'data.js').write_text('window.PipelineData='+json.dumps(data['records'],separators=(',',':'))+';\nwindow.PipelineSpec='+json.dumps(spec,separators=(',',':'))+';\n',encoding='utf-8')
(ROOT/'index.html').write_text((ROOT/'src/template.html').read_text(encoding='utf-8'),encoding='utf-8')
print('Rendered',len(data['records']),'original synthetic records')
