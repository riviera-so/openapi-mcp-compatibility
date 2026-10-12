#!/usr/bin/env python3
"""Fetch each public OpenAPI document listed in data/documents.json and check it.

Needs only Python 3.9+ and an internet connection. YAML documents need PyYAML
(`pip install pyyaml`); without it they are hashed and sized but their
operations are not counted.

What it checks, per document:
  1. The SHA-256 of the downloaded bytes matches the recorded value.
  2. The byte count matches.
  3. The operation count matches. An operation is any of get, put, post,
     delete, options, head, patch or trace under `paths` (path keys starting
     with "x-" are ignored), which is how the study counted.

A document whose hash differs is reported and NOT counted: the study's results
describe the recorded bytes, not whatever the URL serves today. Two documents
(the Swagger Petstore demos) are live servers and are not pinned to a commit,
so a mismatch there means the provider changed the document.

Usage:
    python3 scripts/verify_documents.py            # all 13 documents
    python3 scripts/verify_documents.py svix novu  # some of them
"""
import hashlib
import json
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
METHODS = ("get", "put", "post", "delete", "options", "head", "patch", "trace")


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "openapi-mcp-compatibility-research/verify"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def parse(raw: bytes, fmt: str):
    text = raw.decode("utf-8")
    if fmt == "json" or text.lstrip().startswith("{"):
        return json.loads(text)
    try:
        import yaml  # type: ignore
    except ImportError:
        return None
    return yaml.safe_load(text)


def count_operations(document) -> int:
    paths = (document or {}).get("paths") or {}
    total = 0
    for key, item in paths.items():
        if str(key).startswith("x-") or not isinstance(item, dict):
            continue
        total += sum(1 for method in METHODS if item.get(method))
    return total


def main(argv) -> int:
    manifest = json.loads((ROOT / "data" / "documents.json").read_text())["documents"]
    wanted = set(argv)
    failures = 0
    for doc in manifest:
        if wanted and doc["id"] not in wanted:
            continue
        try:
            raw = fetch(doc["source_url"])
        except Exception as error:  # network, 404, TLS
            print(f"{doc['id']:<18} FETCH FAILED  {error}")
            failures += 1
            continue
        digest = hashlib.sha256(raw).hexdigest()
        if digest != doc["sha256"]:
            print(f"{doc['id']:<18} HASH DIFFERS  recorded {doc['sha256'][:12]}, now {digest[:12]} ({len(raw)} bytes). Not counted.")
            failures += 1
            continue
        problems = []
        if len(raw) != doc["bytes"]:
            problems.append(f"bytes {len(raw)} != {doc['bytes']}")
        parsed = parse(raw, doc["format"])
        note = ""
        if parsed is None:
            note = "operations not counted (install pyyaml)"
        else:
            operations = count_operations(parsed)
            if operations != doc["operations_in_document"]:
                problems.append(f"operations {operations} != {doc['operations_in_document']}")
            else:
                note = f"{operations} operations"
        status = "OK " if not problems else "BAD"
        print(f"{doc['id']:<18} {status} sha256 matches, {len(raw)} bytes, {note} {'; '.join(problems)}".rstrip())
        failures += bool(problems)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
