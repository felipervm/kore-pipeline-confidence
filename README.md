# Pipeline Confidence — KORE Sales Operations work sample

Independent project by Felipe Mattos. Fictional opportunities, illustrative policies and no affiliation with KORE.

A business-first demonstration of seller support: inspect an unclear record, explain each control, propose an accountable function and make the next action reviewable. The page uses KORE's official logo, globe imagery, Aptos Display headings, Inter body text, navy and orange. Felipe's supplied photo appears in the closing introduction.

## Run and verify

```sh
python src/build.py
python -m unittest discover -s tests -v
python src/render.py
node --check engine.js
node --check app.js
python -m http.server 8000
```

Open localhost:8000. The generated page loads local scripts and embedded fixture data without an API. Python 3 and Node are needed for the full checks. CI runs these checks on main.

## Preserved original fixture

- 120 fictional opportunities; 57 require review; 63 pass the seven controls.
- CAD 10,803,000 reported numeric open annualized value.
- CAD 5,376,000 strict pass-only open-value subset.
- Original seed and as-of: 20261020 / 20 October 2026.

These are not KORE metrics, eARR, forecast corrections, lost revenue or measured gains. The original generator and 12 tests are preserved. Two additional tests compare the browser engine against Python over all 120 records and boundary cases, including the dormant approval rule and source preservation.

## Interface

Current-record versus proposed-approach walkthrough; dynamic whole-fixture counts and values; status/rule/stage/search filters; filtered CSV; keyboard-accessible inspection dialog; seven expandable control definitions with links into the queue; proposed seller enablement and 30-day shadow pilot.

Source observations are never changed. All proposed actions require human review; no Salesforce, Gemini or production integration exists. See [definitions and limitations](docs/method.md) and [candidate-provided context](PROJECT_CONTEXT.md).

Files: `src/build.py` builds CSV/results; `src/render.py` renders `index.html` from `src/template.html` and emits `data.js`; `engine.js` mirrors the original rules; `app.js` handles presentation; `styles.css` defines the responsive layout.

[Live page](https://felipervm.github.io/kore-pipeline-confidence/) · [LinkedIn](https://www.linkedin.com/in/felipervm/) · felipervm22@gmail.com
