# Model adaptation

The workflow is reusable even when a historical model endpoint is unavailable. Availability, behavioral equivalence, and experimental reproducibility are different questions.

## Assign capabilities to roles

| Role | Needed capabilities |
|---|---|
| Extraction | Read long judgments, separate speakers/roles, return structured records with evidence anchors |
| Planner | Allocate evidence across sections; retain chronology and critical qualifications |
| Prompt builder | Read the plan and assemble a complete section instruction without introducing facts |
| Writer | Produce Traditional Chinese, obey section boundaries, cite supplied chunk IDs |
| Auditor | Compare drafts to sources; identify attribution, scope, chronology and omission problems |
| Reviser | Make ticket-scoped changes and preserve supported content |
| Evaluator, if requested | Follow an explicit reference/source/rubric protocol independent of generation inputs |

Separate models are optional. A single capable model can serve multiple roles in separate contexts. This is an adaptation and must be described as such. The auditor should receive the source and draft artifacts, not a request to defend the writer's choices. Different models do not guarantee independent errors.

## Record the actual run

Store the provider, exact model ID returned by the endpoint where possible, role, execution date, relevant settings, prompt version, workflow version, retry count, and any response truncation. If the provider does not expose an immutable model version, record that limitation. Never manufacture a version identifier.

Check access with the user's authorized settings before a substantive run. Do not install services, purchase credits, or send a legal document to a new provider without authorization. If a configured model is unavailable, stop that role and report the failure. Use a replacement only within the user's authorized model choices, and record the change.

## Validate an adaptation

Start with authorized or synthetic inputs. Inspect whether the replacement obeys output schemas, separates the five sections, preserves quoted evidence and numeric qualifications, produces resolvable citations, and performs local rather than uncontrolled revisions. A format check alone is insufficient.

If comparing against the paper, use an explicitly matched dataset, prompt contract, settings, and evaluation protocol. Without those conditions, label results as a new configuration. Do not reuse the paper's effect sizes, P values, or human-preference results as evidence for a replacement model.

The user has reported that some historical models are no longer accessible in their environment. This release neither verifies global endpoint retirement nor promises bitwise or performance-equivalent reproduction.
