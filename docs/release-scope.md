# Release scope

This repository publishes the **reusable LENS workflow**, with replaceable model-role assignments. It is a portable documentation adaptation prepared on 20 November 2026 from the project's extraction, summarization, planner, prompt-builder, auditor, reviser, section-template and style contracts.

## Preserved

- Stable source chunks and source-linked case representations.
- Distinct prosecution, defense, expert and court roles.
- Evidence planning before generation, five section boundaries and 13 logical prompt blocks.
- Deterministic checks separated from semantic auditing.
- Explicit section-addressed repair tickets, local revision and a two-round bound.
- Separation of reference coverage, source support, rubric judgments and practitioner preferences.

## Adapted for portability

- No fixed provider/model names, cloud endpoint assumptions, machine paths or private orchestration extensions.
- One host-neutral skill entry point with role instructions; serial role execution is allowed where parallel agents are unavailable.
- A small, explicitly versioned portable JSON contract rather than a claim that this is the complete historical `master.json`/runtime format.
- A limited structural validator, not a replacement for all original deterministic tools.
- A hand-authored fictional example instead of copyrighted expert-reference excerpts or real case data.
- Citation corrections may be performed when justified by an explicit ticket, rather than retaining an erroneous citation under a blanket preservation rule.

## Not claimed

This release does not claim identical prompts, runtime behavior, model availability, outputs, statistical results or effectiveness to the historical experiments. It is not a clinical or legal decision system. It is not the original full execution engine. A source ID resolving successfully does not establish entailment or correct attribution.

No manuscript, submission forms, real judgments, expert-authored summaries, participant data, API keys or private filesystem paths are included. No claim of journal acceptance is made.

## Publication statements

Any manuscript availability statement should identify this as a workflow skill and specify its actual contents. It must not state that all experimental code and data are publicly available on the strength of this repository alone. Access to additional underlying research code/data, if required for review or replication, must be addressed separately and accurately by the authors.
