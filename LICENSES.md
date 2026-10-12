# Licences

| Part | Licence | Notes |
| --- | --- | --- |
| `scripts/` | MIT (`scripts/LICENSE`) | Two small standard-library Python scripts written by Riviera |
| `data/` results and the Markdown files | CC BY 4.0 (`LICENSE-data.txt`) | Riviera's own counts, classifications and explanatory text. Reuse and cite with attribution to Riviera, and link to this repository |

## What these licences do not cover

The licences above apply only to material Riviera wrote. They do not relicense anything that belongs to the API providers.

- **No specification text is included.** The scripts download each document from its owner's URL and do not store it here.
- **Identifiers.** `data/operations.csv` lists each operation's HTTP method and path, and where a tool was produced, a name derived from the operation's identifier. These are facts needed to say which operation is meant. They are the providers' identifiers and are not claimed by Riviera.
- **Provider licences.** The licence of each source is recorded per document in `data/documents.json` (`licence_as_recorded`): Svix, Resend and Intercom publish theirs under MIT, Novu is recorded as MIT, and for Unkey and Formbricks GitHub reports no single licence for the repository. Whatever a provider's licence says continues to apply to its document.
- **Trademarks.** Provider and product names are used only to identify the documents analysed.

If you are a provider named here and want a row, a name or a link removed or corrected, open an issue or write to hello@riviera.so.
