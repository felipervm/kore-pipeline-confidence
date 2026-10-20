# Pipeline Confidence: definitions and review model

Independent fictional work sample by Felipe Mattos. No KORE internal systems were inspected. Intended improvements are hypotheses for a shadow pilot, not measured outcomes.

## Original fixture preserved

`src/build.py` preserves the original generator, seed 20261020 and fixed as-of date 20 October 2026. It produces 120 fictional opportunities, 57 requiring review and 63 passing all controls. A record may trigger multiple exceptions. Synthetic names are not customers or employees.

Original reported numeric open annualized value: CAD 10,803,000. Strict pass-only open subset: CAD 5,376,000. Neither is a probability-weighted forecast or KORE eARR. The difference is not financial impact, lost revenue or a revenue-risk estimate. Zero passes the original simplified numeric check. Invalid values are excluded from numeric sums; closed stages are excluded from both open-value measures. Legacy `estimated_arr_cad`/`contract_arr_cad` names do not establish an accounting ARR or company eARR definition.

## Seven controls, original semantics

1. MISSING_OWNER: blank seller; Sales Operations.
2. MISSING_NEXT_STEP: blank next step for open stage; Opportunity owner.
3. INVALID_ARR: unparsable or negative integer annualized value; Revenue Operations.
4. STAGE_PROBABILITY_MISMATCH: unknown stage or probability string different from the fictional stage default; Opportunity owner.
5. PAST_DUE_CLOSE: open close date before the fixed as-of date; Opportunity owner.
6. WON_VALUE_MISMATCH: Closed Won integer values disagree or cannot be parsed; Revenue Operations.
7. APPROVAL_PENDING: Closed Won lacks Approved commercial status; Deal Desk. This control has zero examples in the original fixture and a dedicated test. Open Pending records are not flagged by this rule.

Illustrative stage probabilities: Prospecting 10, Qualification 25, Proposal 50, Negotiation 75, Closed Won 100, Closed Lost 0. These are assumptions, not KORE policy or Salesforce defaults. High priority precedes Medium, then rule codes are sorted alphabetically. The queue shows the first proposed action; its inspector shows every issue, owner and action.

## Human workflow

The walkthrough compares the source record with a proposed review approach. It does not change or resolve anything. A responsible function is proposed, rather than a claim that the person has accepted a task. Source records, totals and flags remain unchanged. Review events carry `requiresHumanReview:true` and `executed:false`. No Salesforce/Gemini or external API connection exists.

The queue defaults to records requiring review. Status, rule, stage and text filters affect only displayed rows and CSV. Whole-fixture summary cards remain fixed. CSV exports include field headers and quote embedded quotes. An empty selection exports headers only.

## Verification and limits

Run `python src/build.py`, `python -m unittest discover -s tests -v`, `python src/render.py`, `node --check engine.js`, `node --check app.js`. The 12 original Python tests are preserved; two additional tests verify browser/Python equality over all records and relevant boundary cases, dormant approval handling, priority order and non-mutation.

This is a bounded demonstration using well-formed source fields. It is not a general CRM schema validator: malformed dates/types, duplicate identifiers, permissions, history, integrations, audit events and production incident handling would need separate requirements and controls. A passing record means only that these seven controls did not flag it.

Brand context: [KORE official website](https://www.korewireless.com/). Candidate experience and target-role responsibilities come from the candidate-provided context. The page does not assert the vacancy remains open or imply remote-from-abroad eligibility.
