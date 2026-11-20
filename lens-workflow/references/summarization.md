# Five-section summarization

## Classification and planning

Create a case classification, anonymized fact index, source inventory and textual case digest. Use the inventory for navigation but consult source text when allocating ambiguous material. Preserve stable source IDs.

The planner assigns `chunk_ids`, source-linked `fact_ids`, critical evidence, detail level, target characters, and a paragraph plan for each section. Adapt budgets to source length and complexity rather than imposing the same output length on every case. Keep the disposition concise; allocate reasoning detail according to what the court actually explains. Record the budget policy.

| Section | Include | Keep elsewhere |
|---|---|---|
| facts | Background, clinical chronology, prosecution allegations and procedural origin, with attribution | Defense accounts, expert conclusions and court findings |
| defense | Defendant and counsel positions; admissions or denials | The court's acceptance/rejection of those positions |
| opinions | Attributed expert or professional assessments, including disagreement and qualifications | The court's reasons for accepting or rejecting them |
| verdict | Disposition, relevant sentence and procedural status if supported | The substantive reasoning for the result |
| reasoning | Court findings, evidence assessment, legal analysis and qualified causal reasoning | Unattributed recycling of prosecution or defense claims |

The five headings do not create evidence. If a section has no supported content, state that narrowly rather than filling it with a plausible account. Do not conflate the absence of a conviction with proof that a medical act was appropriate.

## Build each section prompt

Preserve the following 13 logical blocks. A block can explicitly be inapplicable; do not silently drop an evidence constraint.

1. Section identity and output filename.
2. Section-specific instruction.
3. Included scope.
4. Excluded scope.
5. Alias map needed by that role.
6. Structural template appropriate to the case.
7. Style guidance or an authorized/synthetic example, labelled as such.
8. Paragraph guidance and evidence allocation.
9. Anonymized fact cards.
10. Critical evidence and qualifications to preserve.
11. Allowed source IDs, source locations and inventory descriptions.
12. Writing rules: Traditional Chinese, neutral attribution, terminology, citation syntax and numeric preservation.
13. Output contract and verification instructions.

Source descriptions are not substitutes for source text. A writer must read the cited passages before drafting. Prefer no more than two citation markers per sentence when sufficient; if more evidence is needed, split the sentence without changing meaning. A citation should support the particular assertion, not merely concern the same case.

Write each section separately. Long reasoning may be split according to the paragraph plan; its concluding paragraph must be consistent with the completed reasoning paragraphs and cited sources. Record whether generation was serial, parallel, or split. Never hide a failed role by fabricating its output.

## Check, audit and revise

Run implemented deterministic checks first: file/schema validity, permitted source IDs, complete sections, known fact IDs, configured length limits, and implemented alias/numeric/terminology checks. Record the coverage of the checks. The bundled validator covers only a subset.

Then audit all five sections against the source, plan and critical evidence. Return explicit tickets with target section, severity, problem type, anchor, source IDs, requested fix and constraints. Independently check attribution, scope, chronological consistency, missing material and source support. Do not infer these properties from a valid citation ID.

Default revision policy:

- Any CRITICAL/HIGH/MEDIUM ticket triggers targeted revision.
- Group tickets by section; process them in severity order.
- Retain unticketed sections. Use only the ticket's allowed evidence; if evidence is insufficient, mark the ticket unresolved.
- Fix an erroneous citation when justified by its ticket; do not preserve a known-wrong citation merely to keep the text unchanged.
- Save original drafts and each revision; do not overwrite the audit history.
- After revision 1, rerun structural checks and audit again when the loop continues.
- After revision 2, rerun structural checks and assemble. Record that no third semantic audit was performed, unless a separately authorized additional review is conducted and labelled separately.

Assemble Facts → Defense → Opinions → Verdict → Reasoning. Report unresolved tickets, the stop reason, and the limits of the final verification. This workflow supports initial source review; it does not replace accountable professional judgment.
