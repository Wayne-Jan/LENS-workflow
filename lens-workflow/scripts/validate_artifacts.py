#!/usr/bin/env python3
"""Validate portable LENS artifacts; no model calls or semantic correctness claims."""
import argparse
import json
import re
from pathlib import Path

SECTIONS = ("facts", "defense", "opinions", "verdict", "reasoning")


def validate(root):
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    def read(name):
        try:
            value = json.loads((root / name).read_text(encoding="utf-8"))
            if not isinstance(value, dict):
                raise ValueError("expected an object")
            return value
        except (OSError, ValueError) as exc:
            errors.append(f"{name}: {exc}")
            return {}

    def string(value):
        return isinstance(value, str) and bool(value.strip())

    def refs(value, allowed, label, nonempty=False):
        if not isinstance(value, list) or not all(string(x) for x in value):
            errors.append(f"{label}: expected a list of nonempty strings")
            return set()
        check(not nonempty or bool(value), f"{label}: empty evidence list")
        check(len(value) == len(set(value)), f"{label}: duplicate IDs")
        check(set(value) <= allowed, f"{label}: unknown or unallocated IDs")
        return set(value)

    source = read("chunks.json")
    check(source.get("schema_version") == 1, "chunks: schema_version must be 1")
    case_id = source.get("case_id")
    check(string(case_id), "chunks: missing case_id")
    check(type(source.get("synthetic")) is bool, "chunks: synthetic must be boolean")
    chunks = source.get("chunks", [])
    if not isinstance(chunks, list):
        errors.append("chunks: expected an array")
        chunks = []
    check(bool(chunks), "chunks: empty source")
    ids = set()
    for chunk in chunks:
        if not isinstance(chunk, dict):
            errors.append("chunks: chunk must be an object")
            continue
        cid = chunk.get("id")
        if not isinstance(cid, str) or not re.fullmatch(r"CH_[0-9]+", cid):
            errors.append("chunks: invalid chunk ID")
            continue
        check(cid not in ids, f"chunks: duplicate {cid}")
        ids.add(cid)
        check(string(chunk.get("text")), f"chunks: empty text for {cid}")

    record, classify, plan, manifest = [read(n + ".json") for n in
                                       ("case_record", "classify", "plan", "run_manifest")]
    for name, obj in (("case_record", record), ("classify", classify),
                      ("plan", plan), ("run_manifest", manifest)):
        check(obj.get("case_id") == case_id, f"{name}: case_id mismatch")
    facts = record.get("facts")
    if not isinstance(facts, list):
        errors.append("case_record: facts must be an array")
        facts = []
    fact_ids = set()
    for fact in facts:
        if not isinstance(fact, dict):
            errors.append("case_record: fact must be an object")
            continue
        for field in ("id", "speaker", "text"):
            check(string(fact.get(field)), f"case_record: missing {field}")
        fid = fact.get("id")
        if string(fid):
            check(fid not in fact_ids, "case_record: duplicate fact ID")
            fact_ids.add(fid)
        refs(fact.get("source_ids"), ids, "case_record source_ids", True)
    inventory = refs(classify.get("source_ids"), ids, "classify source_ids")
    check(inventory == ids, "classify: incomplete source inventory")
    for field in ("case_type", "digest"):
        check(string(classify.get(field)), f"classify: missing {field}")
    check(isinstance(classify.get("aliases"), dict), "classify: aliases must be an object")
    sections = plan.get("sections")
    if not isinstance(sections, dict):
        errors.append("plan: sections must be an object")
        sections = {}
    check(set(sections) == set(SECTIONS), "plan: exactly five named sections required")
    for name in SECTIONS:
        section = sections.get(name, {})
        if not isinstance(section, dict):
            errors.append(f"plan {name}: expected an object")
            section = {}
        budget = section.get("budget_chars")
        check(type(budget) is int and budget > 0, f"plan {name}: invalid budget_chars")
        allocated = refs(section.get("allowed_source_ids"), ids, f"plan {name} allocation")
        refs(section.get("critical_source_ids"), allocated, f"plan {name} critical IDs")
        try:
            draft = (root / "sections" / (name + ".txt")).read_text(encoding="utf-8")
            check(bool(draft.strip()), f"section {name}: empty draft")
            cited = set(re.findall(r"\[(CH_[^\]\s]+)\]", draft))
            check(cited <= allocated, f"section {name}: unknown or unallocated citation")
        except OSError as exc:
            errors.append(f"section {name}: {exc}")

    check(manifest.get("kind") in ("executed_run", "hand_authored_example"), "manifest: invalid kind")
    check(string(manifest.get("workflow_version")), "manifest: missing workflow_version")
    check(isinstance(manifest.get("roles"), dict), "manifest: roles must be an object")
    rounds = manifest.get("revision_rounds")
    check(type(rounds) is int and 0 <= rounds <= 2, "manifest: revision_rounds must be 0..2")
    for field in ("semantic_audit_performed", "semantic_reaudit_after_final_revision"):
        check(type(manifest.get(field)) is bool, f"manifest: {field} must be boolean")
    for field in ("unresolved_ticket_ids", "limitations"):
        values = manifest.get(field)
        check(isinstance(values, list) and all(string(v) for v in values), f"manifest: invalid {field}")
    audit_files = sorted(root.glob("audit_round_*.json"))
    check(not manifest.get("semantic_audit_performed") or bool(audit_files), "manifest: claimed audit lacks artifact")
    ticket_ids = set()
    for path in audit_files:
        audit = read(path.name)
        audit_round = audit.get("round")
        check(type(audit_round) is int and audit_round in (1, 2), f"{path.name}: invalid round")
        check(path.name == f"audit_round_{audit_round}.json", f"{path.name}: round/name mismatch")
        tickets = audit.get("tickets")
        if not isinstance(tickets, list):
            errors.append(f"{path.name}: tickets must be an array")
            continue
        local_ids = set()
        for ticket in tickets:
            if not isinstance(ticket, dict):
                errors.append(f"{path.name}: ticket must be an object")
                continue
            for field in ("id", "anchor", "issue", "requested_fix"):
                check(string(ticket.get(field)), f"{path.name}: missing ticket {field}")
            tid = ticket.get("id")
            if string(tid):
                check(tid not in local_ids, f"{path.name}: duplicate ticket ID")
                local_ids.add(tid)
                ticket_ids.add(tid)
            check(ticket.get("section") in SECTIONS, f"{path.name}: invalid section")
            check(ticket.get("severity") in ("CRITICAL", "HIGH", "MEDIUM", "LOW"), f"{path.name}: invalid severity")
            refs(ticket.get("source_ids"), ids, f"{path.name} ticket source_ids")
    unresolved = manifest.get("unresolved_ticket_ids")
    if isinstance(unresolved, list) and all(string(v) for v in unresolved):
        check(set(unresolved) <= ticket_ids, "manifest: unresolved ticket not present in audit history")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    errors = validate(parser.parse_args().workspace)
    for error in errors:
        print(f"FAIL: {error}")
    if not errors:
        print("PASS: structural checks only; semantic source support has not been verified.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
