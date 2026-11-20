# Source preparation and structured extraction

1. Preserve an immutable copy of the authorized original judgment and its source identifier. Record any normalization separately. Assign stable `CH_XX` IDs to contiguous passages; keep their order and, where available, original character offsets.
2. Extract document coordinates such as court, date, case identifier, defendants and disposition. Separate deterministic extraction candidates from semantic confirmation.
3. Build an entity map before resolving arguments that refer to those entities. Distinguish defendants, patients, institutions, counsel, experts and the court. Do not infer identity across ambiguous aliases.
4. Separate prosecution allegations, defense arguments, expert assessments and court findings. Each extracted item retains its speaker/role, source IDs and a source quote or span. A conflict between sources remains visible.
5. Build the clinical/event timeline, including uncertainty and competing descriptions. Distinguish an event date from the date it was reported or assessed. Do not invent chronology to fill gaps.
6. Align evidence quotes to the source. Run exact matching first; flag fuzzy or ambiguous matches rather than treating them as established. For unresolved items, inspect a focused excerpt, revise only from evidence, then expand to the full source if needed. Bound this grounding repair to two passes and record remaining unresolved items.
7. Check cross-field consistency, disposition, attribution and medical interventions where relevant. Save source-linked records; do not label them independently validated ground truth.
8. Create the alias map and anonymized working view. Validate replacements, including institutional and contextual identifiers. Keep the mapping private. A lexical name check does not prove irreversible anonymization.

The portable `case_record.json` stores only the source-linked fields needed for downstream navigation. More detailed extraction schemas may be retained by an implementation. Do not flatten distinct defendants or expert opinions into one undifferentiated record.

No original case corpus or third-party expert summary is included in this repository. Users supply data under their own access and redistribution permissions.
