# What happens when you turn public OpenAPI documents into MCP tools

The data behind [OpenAPI to MCP: what converts cleanly, what doesn't, and why](https://riviera.so/guides/openapi-to-mcp-conversion), published by [Riviera](https://riviera.so). We ran Riviera's own OpenAPI importer, as released to production on 11 October 2026, over thirteen public OpenAPI documents and recorded, for every operation, whether it became a tool and, if not, the first thing that stopped it.

**Disclosure:** Riviera sells a product that does this conversion, and the importer measured here is Riviera's. It is deliberately strict: it makes a tool only when it can call the operation exactly as the document describes it. A converter with different goals would show different numbers. These results describe this importer on these documents. They are not a ranking of converters and not a statement about OpenAPI documents in general.

## What you can verify, and what you have to take on trust

| | Independently verifiable with this repository | Depends on Riviera's private importer |
| --- | --- | --- |
| What | That the 13 documents are the bytes we name (URL, SHA-256, size, OpenAPI version, operation count), and that the data files agree with each other and with the totals | Which operations became tools, the first cause for each that did not, and every count derived from them |
| How | `python3 scripts/verify_documents.py` and `python3 scripts/check_data.py` | Not reproducible here. You can read the results, compare them with your own converter's output on the same pinned bytes, and check them for internal consistency |
| Files | `data/documents.json`, the scripts | `data/results.csv`, `data/operations.csv`, `data/diagnostics.csv`, `data/totals.json` |

The importer is not published. Treat its outputs as a vendor's measurement of its own product.

## Headline numbers

Two sets of documents, never added together. Recomputed from the CSV files by `scripts/check_data.py`.

| Set | Documents | Accepted as published | Operations that became tools, after the preparation Riviera's documentation asks for |
| --- | --- | --- | --- |
| Seven SaaS API documents, chosen by written criteria before the importer was run | 7 | 6 of 7 (the seventh is 1.1 MB, over the 1 MiB limit, and was accepted once whitespace was removed) | 124 of 538 operations (23 percent), in 3 of 7 documents |
| Six exploratory documents, chosen to show causes | 6 | 4 of 6 | 0 of 282 operations in the 5 documents that could be analyzed (0 of 82 operations in the 4 analyzed as published) |

Most of the 124 are not finished tools: 3 need nothing, and 121 still need an ordinary decision in the product, such as a credential. None of this says a generated tool executes correctly against the real API, or that a model chooses and fills it in correctly. **No provider's API was called and no model was called.**

## What you can reproduce without anything from Riviera

Python 3.9+ and an internet connection. `pip install pyyaml` for the YAML documents.

```
python3 scripts/verify_documents.py   # fetch all 13 documents, check each SHA-256, byte count and operation count
python3 scripts/check_data.py         # check the CSV files agree with each other and with the totals above
```

What this lets you check independently: that the documents we name are the bytes we analyzed (hashes), how big they are, which OpenAPI version they declare, and how many operations they contain. Eleven of the thirteen URLs name a commit and cannot change. The two Swagger Petstore documents come from live demo servers, so a hash mismatch there means the provider changed the document.

## What you cannot reproduce from this repository

The per-operation outcomes in `data/operations.csv` and the counts in `data/results.csv` were produced by Riviera's importer, which is **not published here**. Without it you can read the results, compare them with what your own converter does on the same pinned documents, and check them for internal consistency, but you cannot regenerate them. `METHOD.md` describes the importer's rules and what each reason code means, which is enough to write a compatible implementation and compare, not to run ours.

## How the corpus was selected

Thirteen public documents in two sets that are never added together. Seven SaaS API documents (Svix, Unkey, Novu, Resend, Formbricks, Intercom, Dropbox Sign) were chosen by written criteria fixed before the importer ran, from a pool of twelve providers. Six exploratory documents (Swagger Petstore 3.0 and 3.1, SendGrid, Twilio Verify, Discord, OpenAI) were chosen on purpose to show different causes. The five candidates that were not selected, with the reason for each, are in `data/candidates-not-selected.json`. `METHOD.md` has the criteria.

## Why this is not a representative sample

Thirteen chosen documents say which causes exist, not how common they are. The pool came from providers we already knew publish a specification, which skews toward developer-facing companies. Nothing here estimates what share of any company's API would convert. `LIMITS.md` lists everything the study does not show.

## Acceptance, conversion and execution are different things

1. **Document acceptance:** the importer read the document and reported on its operations, or refused it whole (for example, over its 1 MiB size limit).
2. **Operation conversion:** an operation can be called exactly as the document describes it, so a tool definition exists.
3. **Execution:** calling that tool against the real API returns the right result, and a model chooses and fills it in correctly.

This study measures 1 and 2. It does not measure 3. No provider's API and no model was called.

## The complete guide

The write-up with the full tables, the reasons and what to fix in your own document: [OpenAPI to MCP: what converts cleanly, what doesn't, and why](https://riviera.so/guides/openapi-to-mcp-conversion).

## To cite

Riviera, "What happens when you turn public OpenAPI documents into MCP tools", data and method, 11 October 2026. https://riviera.so/guides/openapi-to-mcp-conversion

## Files

| Path | What it is |
| --- | --- |
| `data/documents.json` | The 13 documents: provider, pinned URL, SHA-256, bytes, format, OpenAPI version, operation count, declared authentication, licence as recorded |
| `data/results.csv` | One row per document and scenario (as published, after documented preparation): accepted or refused, operations examined, converted, excluded, first-cause counts |
| `data/operations.csv` | One row per operation examined: method and path, whether it became a tool, the first reason code if not |
| `data/diagnostics.csv` | The same counts after mechanical what-if edits to the document. These are diagnostics of what an edit would unlock. They are never what ordinary onboarding looks like |
| `data/totals.json` | The headline totals above |
| `METHOD.md` | How documents were chosen, the three scenarios, what was counted, what the importer accepts |
| `CODES.md` | What each first-cause code means |
| `LIMITS.md` | What this study does not show |
| `scripts/` | The two scripts above. They import nothing from Riviera |
| `LICENSES.md`, `LICENSE-data.txt`, `scripts/LICENSE` | Licences and what they do not cover |

`cell_id` values such as `icp/svix/A` and `corpus1/...` are the labels of Riviera's analysis runs (`A` is as published, `B` is documented preparation, `C` is a diagnostic edit). They carry no other meaning.

## What is not here

No specification text, no importer source, no credentials, no customer data. Only identifiers (HTTP method and path, which are facts about each API), URLs, hashes, counts and Riviera's reason codes.

## Licence

Riviera's own results and text: CC BY 4.0. The two scripts: MIT. Nothing here relicenses the providers' documents or identifiers. See `LICENSES.md`.
