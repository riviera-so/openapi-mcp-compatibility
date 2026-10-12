# Method

## What was measured

For each document, three things, kept apart:

1. **Document acceptance.** Did the importer read the document and report on its operations, or refuse it whole (for example because it is over 1 MiB)?
2. **Operation conversion.** Can this operation be called exactly as the document describes it? An operation that can becomes a tool definition: a name, a description, an input schema and a request mapping.
3. **First cause.** For an operation that does not convert, the first thing that blocked it. The importer records only the first cause, so an operation with two problems is counted once, for whichever it met first. Counts of causes therefore understate how many causes exist.

Not measured: whether a generated tool works against the real API, or whether a model selects and fills it correctly. No provider API and no model was called.

## Two document sets

- **SaaS cohort (7).** Svix, Unkey, Novu, Resend, Formbricks, Intercom, Dropbox Sign. Chosen by written criteria fixed before the importer was run on any of them: published by the provider in a public repository or at an official URL and fetchable without an account; the customer-facing REST API of a B2B SaaS product; 10 to 200 operations; OpenAPI 3.x; declares an HTTP bearer or header API key scheme; not in the exploratory set. Seven of twelve candidates met them, and all seven are in. The pool was twelve providers we already knew published a specification, mostly developer-facing, so it is not a random sample and a company's own API may be less carefully described. The five not selected are listed in `data/candidates-not-selected.json` with the reason: Cal.com (no security scheme declared), FusionAuth (347 operations), Lago (217), Clerk Backend API (221), Front Core API (246). They were not analyzed.
- **Exploratory set (6).** Swagger Petstore 3.0 and 3.1, SendGrid Mail v3, Twilio Verify v2, Discord HTTP API v10, OpenAI API. Chosen on purpose to cover different OpenAPI versions, sizes, authentication declarations and input problems. It says which causes exist, not how often.

The totals of the two sets are never added together.

## Three scenarios

| Scenario | Input | What it can show |
| --- | --- | --- |
| `as-published` | The exact bytes, unchanged | What a developer experiences who pastes the document and imports it |
| `documented-preparation` | Only the preparation Riviera's documentation asks for: remove whitespace from a document whose only problem is size, keep the first 200 operations of a document that has more. The content is not edited | The ordinary onboarding outcome |
| `diagnostic` | Mechanical what-if edits: declare one absolute server, drop `webhooks`, drop fields written beside a `$ref`, optionally remove every authentication requirement, each alone and together | An estimate of what an edit would unlock. Never ordinary onboarding, and the authentication-removed variants are not usable imports |

## Counting operations

An operation is any of `get`, `put`, `post`, `delete`, `options`, `head`, `patch` or `trace` under `paths`, ignoring path keys that start with `x-`. `scripts/verify_documents.py` implements exactly this. (The selection criteria for the SaaS cohort counted five methods, so a few documents had slightly lower counts at selection time. The results use the eight-method count.)

## What the importer does, in short

Riviera's importer creates a tool only when it can reproduce the call exactly. It reads JSON or YAML 1.2, one document, up to 1 MiB and 200 operations. It can call APIs with no authentication, a header API key, an HTTP bearer token, OAuth client credentials or per-user OAuth. It needs one absolute server URL. It supports required JSON request bodies on write methods, one JSON object response per success status, and a fixed list of schema keywords. It does not support `nullable`, type unions, `oneOf`, `anyOf` or `allOf`, optional request bodies, regional or alternative servers, HTTP Basic, or recursive schemas. These are limits of this importer, chosen to avoid guessing, and not limits of the OpenAPI format or of MCP. The product documentation lists them: [Importing an API](https://riviera.so/docs/importing-an-api).

## Reproducibility, stated precisely

| Claim | Reproducible with this repository alone? |
| --- | --- |
| The documents are the ones named, with these bytes | Yes (`verify_documents.py`) |
| Each document's size, version and operation count | Yes (`verify_documents.py`) |
| The CSV files and totals agree with each other | Yes (`check_data.py`) |
| Which operations converted and why not | **No.** Needs Riviera's importer. You can compare with your own implementation |
| That the numbers are those of the production release | **No.** Riviera states it; Riviera records the importer revision internally and does not publish it |

## Recorded context

Recorded on 11 October 2026 with Node 24.15.0 on a clean working tree, at an importer revision whose source is identical to the production release of that day. The importer was not changed to produce these numbers. Earlier revisions produced different numbers (for example, before YAML support five of the seven SaaS documents could not be read at all), and those are kept in Riviera's records but are not part of this repository.
