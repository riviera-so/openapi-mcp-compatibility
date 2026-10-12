#!/usr/bin/env python3
"""Check that the published data files agree with each other.

This does NOT re-run any importer. It recomputes the headline totals from
data/results.csv and data/operations.csv and compares them with
data/totals.json and with the manifest, so a reader can see the numbers in the
README follow from the rows, and that no row was edited by hand.

Usage: python3 scripts/check_data.py
"""
import csv
import json
import pathlib
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def main() -> int:
    errors = []
    documents = {d["id"]: d for d in json.loads((DATA / "documents.json").read_text())["documents"]}
    rows = list(csv.DictReader((DATA / "results.csv").open()))
    ops = list(csv.DictReader((DATA / "operations.csv").open()))
    totals = json.loads((DATA / "totals.json").read_text())

    per_cell_ops = {}
    for op in ops:
        per_cell_ops.setdefault(op["cell_id"], []).append(op)

    for row in rows:
        cell_ops = per_cell_ops.get(row["cell_id"], [])
        identified = int(row["operations_identified"])
        converted = int(row["converted"])
        if len(cell_ops) != identified:
            errors.append(f"{row['cell_id']}: {len(cell_ops)} operation rows, {identified} identified")
        if sum(1 for o in cell_ops if o["status"] != "unsupported") != converted and identified:
            errors.append(f"{row['cell_id']}: converted count does not match operation rows")
        causes = Counter(o["first_cause_code"] for o in cell_ops if o["first_cause_code"])
        if causes != Counter(json.loads(row["first_cause_counts"])):
            errors.append(f"{row['cell_id']}: first-cause counts do not match operation rows")
        if row["document"] not in documents:
            errors.append(f"{row['cell_id']}: unknown document {row['document']}")

    for set_name, scenarios in totals.items():
        for scenario, expected in scenarios.items():
            sel = [r for r in rows if r["set"] == set_name and r["scenario"] == scenario]
            got = {
                "documents": len(sel),
                "accepted": sum(r["document_accepted"] == "yes" for r in sel),
                "documents_with_tools": sum(int(r["converted"]) > 0 for r in sel),
                "operations_in_document": sum(int(r["operations_in_document"]) for r in sel),
                "operations_identified": sum(int(r["operations_identified"]) for r in sel),
                "converted": sum(int(r["converted"]) for r in sel),
            }
            if got != expected:
                errors.append(f"{set_name} / {scenario}: recomputed {got}, recorded {expected}")
            # The denominator is what the importer actually looked at. A document that
            # was refused or not analyzable still has operations, but none were examined.
            print(f"{set_name:<12} {scenario:<24} {got['converted']} of {got['operations_identified']} examined operations became tools, in {got['documents_with_tools']} of {got['documents']} documents ({got['operations_in_document']} operations in the documents)")

    # The first cause of every operation that did not convert, in the seven SaaS
    # documents after the preparation Riviera's documentation asks for.
    saas = Counter()
    for row in rows:
        if row["set"] == "saas-cohort" and row["scenario"] == "documented-preparation":
            saas.update(json.loads(row["first_cause_counts"]))
    print(f"\nFirst causes, seven SaaS documents, {sum(saas.values())} operations did not convert:")
    for code, count in saas.most_common():
        print(f"  {code:<24} {count}")

    if errors:
        print("\n".join(errors))
        return 1
    print("Data files are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
