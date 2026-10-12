# What this study does not show

- **Prevalence.** Thirteen documents in two sets, chosen. Nothing here says how common a cause is across APIs, or what share of any company's operations would convert. The SaaS cohort was chosen by criteria fixed in advance from a pool of twelve providers we already knew, which skews toward developer-facing companies whose documents may be better maintained than the average. The exploratory set was chosen to show causes.
- **A ranking of converters.** The importer is Riviera's and is strict on purpose. A converter that guesses (picks the first server, drops fields it does not understand, accepts optional bodies) would show higher counts and carry its guesses. Compare numbers only with that in mind.
- **Working tools.** Whether a generated tool executes correctly against the real API is not measured. No provider API was called.
- **Agent behaviour.** Whether a model selects a generated tool, or fills its arguments correctly, is not measured. No model was called.
- **Why operations stop beyond the first cause.** Only the first cause per operation is recorded.
- **Diagnostic edits.** They are mechanical and can be wrong for a real document (for example, dropping a constraint written beside a `$ref`, or choosing the first of two servers). They show a ceiling for editing, not what a developer can import.
- **Discord.** The Discord figures cover its first 200 operations in the importer's own order. That slice is not a sample. Discord's `REF_LIMIT` counts depend on operation order.
- **OpenAI.** The OpenAI document was too large to analyze and is not in any conversion figure.
- **Time.** Documents change. These ran on 10 and 11 October 2026 against the hashes in `data/documents.json`. Providers may have corrected their documents since.
- **The protocol.** The unsupported constructs are limits of this importer. They are not limits of OpenAPI, and the MCP specification's treatment of tool schemas has been changing (see SEP-2106 in the MCP specification repository). Numbers that depend on those limits will change when the importer does.
