# Portable artifact contracts (version 1)

Use UTF-8 JSON and text. These contracts describe this portable adaptation, not the historical execution engine. Resolve paths inside the authorized case workspace. Do not store credentials in artifacts.

## Source and case preparation

- `chunks.json`: object with `schema_version: 1`, `case_id`, `synthetic` (boolean), and a nonempty `chunks` array. Each chunk has a unique `id` matching `CH_[0-9]+` and nonempty `text`. Keep original ordering. Add source offsets and document provenance when available; do not fabricate them.
- `case_record.json`: object with matching `case_id` and `facts` array. Each fact has unique `id`, `speaker`, `text`, and nonempty `source_ids`. Speakers distinguish prosecution, defense, expert, and court. Facts are attributed extraction candidates, not verified ground truth. Additional fields may record exact spans, alignment status, dates, entities, and unresolved ambiguity.
- `classify.json`: object with matching `case_id`, `case_type`, `digest`, `source_ids` (the complete inventory), and `aliases` (object). Publish no private alias mapping. An example may use an empty mapping because all source names are already fictional aliases.

## Plan and drafts

`plan.json` contains matching `case_id` and `sections`, an object with exactly these keys in assembly order:

1. `facts`: facts and prosecution allegations
2. `defense`: defense position
3. `opinions`: expert opinions
4. `verdict`: disposition
5. `reasoning`: judicial reasoning

Each section contains `budget_chars` (positive integer), `allowed_source_ids` (array), and `critical_source_ids` (a subset of allowed IDs). These are planning targets, not evidence of actual coverage. A paragraph-level evidence plan may be added. An empty source allocation is permitted only for an explicitly absent section; do not invent missing content.

Persist the 13-block section prompts as `prompts/SECTION.md` during an actual run. Persist nonempty drafts as `sections/SECTION.txt`. Cite allocated chunks as `[CH_01]`; combine multiple citations by repeating the notation. A statement explaining that evidence is absent must be phrased narrowly. The validator checks citation IDs and allocation, not whether each factual clause has a citation or whether it is entailed.

## Audit and loop state

An actual semantic audit writes `audit_round_N.json`, with integer `round` (1 or 2), `tickets` array and, preferably, reviewer identity and checked artifact versions. Each ticket has unique `id`, a valid `section`, `severity` (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`), `anchor`, `issue`, `source_ids`, and `requested_fix`. Preserve resolved and unresolved states in history rather than overwriting the original ticket. A ticket may have an empty source list for a formatting defect; evidence-related tickets must identify their relevant passages.

`run_manifest.json` contains:

- `case_id`, `kind` (`executed_run` or `hand_authored_example`), and `workflow_version`.
- `roles`: object recording the actual model/provider/date/settings for roles that ran. For the hand-authored example, this is empty. Never label an example as an executed run.
- `revision_rounds`: integer from 0 to 2.
- `semantic_audit_performed`: boolean, and `semantic_reaudit_after_final_revision`: boolean.
- `unresolved_ticket_ids`: array and `limitations`: array of strings.

An executed run also records stage completion, prompt versions, checked file versions, validator commands/results, and any skipped checks. If revision 2 is reached, the default flow performs a structural recheck and assembly without another semantic audit. Record this limit. An explicit extension is a different protocol and must be labelled accordingly.

## Validation boundary

The bundled script checks required portable files, basic field types, case IDs, source references, five-section coverage, citation allocation, and revision limits. It does not execute models, assemble summaries, validate the 13 prompt blocks, enforce prose budgets, infer attribution, test anonymity, or certify semantic audits. Optional audit files are checked structurally when present; a run claiming an audit must include one. Successful structural validation never means a judgment or summary is correct.
