# Fictional artifact example

All source text and drafts in this directory are hand-authored fictional teaching material. They describe no real person, judgment, clinical event, or research participant. The example illustrates the artifact format, attribution boundaries, and citation allocation only.

No model ran, no semantic audit was performed, and no empirical score is claimed. Accordingly, `roles` is empty and both semantic-audit flags are false. A real execution also persists its prompts and audit history; this small fixture contains neither and is not a completed pipeline run.

From the repository root:

```sh
python lens-workflow/scripts/validate_artifacts.py lens-workflow/assets/synthetic-case
```

The validator should report structural PASS. To see a failure, copy the example to a temporary workspace and change a draft citation to `[CH_99]`. A copied passage with a valid but semantically wrong citation might still pass; reviewing source support is a separate responsibility.
