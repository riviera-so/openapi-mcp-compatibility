# First-cause codes

Each operation that did not become a tool carries one code: the first thing that stopped it. These are the codes that occur in `data/operations.csv`, with what each means in Riviera's importer and where the fix belongs. "Your document" means a change that makes the document more accurate. "A limit" means the importer does not map the construct today, so editing the document would change what it promises instead of making it clearer.

| Code | Rows in `operations.csv` (an operation appears once per scenario) | What it means | Where the fix belongs |
| --- | --- | --- | --- |
| `SERVER_REQUIRED` | 306 | No single absolute server address to call: none declared, a relative one, or several alternatives such as regions | Your document if none is declared. Otherwise a limit: alternatives are not supported |
| `REF_SIBLINGS` | 217 | Fields written beside a `$ref`, allowed in OpenAPI 3.1. The importer cannot tell which of the two wins | Your document, by moving the fields into the referenced definition |
| `SECURITY_ALTERNATIVES` | 158 | Several authentication options per operation | Your document, by declaring the one an agent should use |
| `SECURITY_UNSUPPORTED` | 120 | Authentication the importer does not supply: HTTP Basic, a key in a cookie | A limit |
| `SCHEMA_TYPE` | 118 | A schema without one explicit, non-null type: `nullable`, type arrays, unions, inferred types | A limit |
| `SCHEMA_UNSUPPORTED` | 70 | A schema keyword outside the supported list, such as `oneOf` or `anyOf` | A limit |
| `BODY_OPTIONAL` | 68 | A request body that does not say `required: true` | Your document, if the body really is required. Otherwise a limit |
| `CONTRACT_INCOMPATIBLE` | 41 | Catch-all for a path or parameter mapping the importer cannot make safely (all 41 in this data are in the first 200 operations of the Discord document) | Depends. The importer's own message says which |
| `REF_MISSING` | 16 | A local reference that points at nothing | Your document |
| `MEDIA_UNSUPPORTED` | 5 | A body or response that is not `application/json` alone | Your document where you can offer JSON alone. Otherwise a limit |
| `METHOD_UNSUPPORTED` | 4 | A method other than GET, POST, PUT, PATCH or DELETE | A limit |
| `RESPONSE_VARIANTS` | 3 | Success responses with different schemas | Your document if one schema can describe them. Otherwise a limit |
| `REF_CYCLE` | 3 | A schema that refers back to itself, which has no finite input schema | A limit |
| `REF_LIMIT` | 2 | References expanded past a budget shared across the whole document. In a large document this depends on operation order and says little about any single operation | A product behavior, not a property of the operation |
| `PARAMETER_STYLE` | 2 | A query array not sent as repeated fields | Your document if the API accepts repeated fields. Otherwise a limit |

Document-level refusals appear in `data/results.csv` in the `refusal_code` column. Here only `DOCUMENT_LIMIT` occurs: the document is over 1 MiB, nested too deeply or has too many nodes. That is an input restriction, not a verdict on the API.

The full list of codes and fixes is in Riviera's documentation: [Importing an API](https://riviera.so/docs/importing-an-api).

## A note on the counts

The importer records one code per operation, the first it meets, so these counts show the first wall, not everything behind it. The `diagnostics.csv` file exists because of that: it shows what is left after a first cause is removed by a mechanical edit.
