from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'data/results.json').read_text())
raw=(root/'src/template.html').read_text(encoding='utf8')
(root/'index.html').write_text(raw.replace('/*DATA_PAYLOAD*/',json.dumps(data,separators=(',',':')).replace('</','<\\/')),encoding='utf8')
print('Generated index.html with',len(data['records']),'synthetic records')
