### Install and initialize qmd

Source: https://github.com/tobi/qmd/blob/main/skills/qmd/SKILL.md

Install the qmd CLI globally, add a notes collection, then update and embed indexes. Only run these mutation commands when the user asks for setup or maintenance.

```bash
npm install -g @tobilu/qmd
qmd collection add ~/notes --name notes
qmd update
qmd embed
```

--------------------------------

### Quick Start: createStore and search

Source: https://github.com/tobi/qmd/blob/main/README.md

Create a store with inline configuration and perform a search. The example shows importing createStore, configuring a collection, searching, and closing the store.

```typescript
import { createStore } from '@tobilu/qmd'

const store = await createStore({
  dbPath: './my-index.sqlite',
  config: {
    collections: {
      docs: { path: '/path/to/docs', pattern: '**/*.md' },
    },
  },
})

const results = await store.search({ query: "authentication flow" })
console.log(results.map(r => `${r.title} (${Math.round(r.score * 100)}%)`))

await store.close()
```

--------------------------------

### Quick Start Commands

Source: https://github.com/tobi/qmd/blob/main/README.md

Install QMD globally with npm or bun, create collections, add context, generate embeddings, and run various search commands.

```sh
# Install globally (Node or Bun)
npm install -g @tobilu/qmd
# or
bun install -g @tobilu/qmd

# Or run directly
npx @tobilu/qmd ...
bunx @tobilu/qmd ...

# Create collections for your notes, docs, and meeting transcripts
qmd collection add ~/notes --name notes
qmd collection add ~/Documents/meetings --name meetings
qmd collection add ~/work/docs --name docs

# Add context to help with search results, each piece of context will be returned when matching sub documents are returned. This works as a tree. This is the key feature of QMD as it allows LLMs to make much better contextual choices when selecting documents. Don't sleep on it!
qmd context add qmd://notes "Personal notes and ideas"
qmd context add qmd://meetings "Meeting transcripts and notes"
qmd context add qmd://docs "Work documentation"

# Generate embeddings for semantic search
qmd embed

# Search across everything
qmd search "project timeline"           # Fast keyword search
qmd vsearch "how to deploy"             # Semantic search
qmd query "quarterly planning process"  # Hybrid + reranking (best quality)

# Get a specific document
qmd get "meetings/2024-01-15.md"

# Get a document by docid (shown in search results)
qmd get "#abc123"

# Get multiple documents by glob pattern
qmd multi-get "journals/2025-05*.md"

# Search within a specific collection
qmd search "API" -c notes

# Export all matches for an agent
qmd search "API" --all --files --min-score 0.3
```

--------------------------------

### Install QMD and add collection

Source: https://github.com/tobi/qmd/blob/main/skills/qmd/references/mcp-setup.md

Install the QMD package globally via npm, add a markdown collection, and embed it for searching.

```bash
npm install -g @tobilu/qmd
qmd collection add ~/path/to/markdown --name myknowledge
qmd embed
```

--------------------------------

### Example output for query "auth config"

Source: https://github.com/tobi/qmd/blob/main/finetune/SCORING.md

Example output for the query "auth config" showing the expected format with prefixes lex, vec, and hyde.

```text
hyde: Authentication can be configured by setting the AUTH_SECRET environment variable and enabling the auth middleware in your application's config file.
lex: authentication configuration
lex: auth settings setup
vec: how to configure authentication settings
vec: authentication configuration options
```

--------------------------------

### Run benchmark with custom fixture from npm install

Source: https://github.com/tobi/qmd/blob/main/README.md

For npm/npx installs, write your own fixture against an already-indexed collection. The example fixture and test corpus are not part of the published package.

```sh
qmd bench my-fixture.json -c my-collection
```

--------------------------------

### Medium Example Output (Score: 55/100)

Source: https://github.com/tobi/qmd/blob/main/finetune/SCORING.md

Example output for the query 'docker networking' that scores moderately. It has valid prefixes but lacks diversity and has repetitive Hyde content.

```text
hyde: Docker networking is an important concept. Docker networking is used for container communication. Docker networking configuration is essential.
lex: docker networking
vec: docker networking
```

--------------------------------

### Lex query examples

Source: https://github.com/tobi/qmd/blob/main/docs/SYNTAX.md

Example lex queries demonstrating prefix matching, exact phrases, and exclusions with the '-' prefix.

```text
lex: CAP theorem consistency
lex: "machine learning" -"deep learning"
lex: auth -oauth -saml
```

--------------------------------

### qmd query CLI usage examples

Source: https://github.com/tobi/qmd/blob/main/docs/SYNTAX.md

Examples of the qmd query CLI command with different input formats: implicit expand, multi-line with types, structured, and with intent (inline or flag).

```bash
qmd query "how does auth work"
```

```bash
qmd query $'lex: auth token\nvec: how does authentication work'
```

```bash
qmd query $'lex: keywords\nvec: question\nhyde: hypothetical answer...'
```

```bash
qmd query --intent "web performance and latency" "performance"
```

--------------------------------

### Search command examples

Source: https://github.com/tobi/qmd/blob/main/README.md

Examples of using `qmd search`, `qmd vsearch`, and `qmd query` for different search modes.

```sh
# Full-text search (fast, keyword-based)
qmd search "authentication flow"

# Vector search (semantic similarity)
qmd vsearch "how to login"

# Hybrid search with re-ranking (best quality)
qmd query "user authentication"
```

--------------------------------

### Multi-line query example

Source: https://github.com/tobi/qmd/blob/main/docs/SYNTAX.md

Shows a multi-line query combining lex, vec, and hyde types. The first query gets 2x weight in fusion.

```text
lex: rate limiter algorithm
vec: how does rate limiting work in the API
hyde: The API implements rate limiting using a token bucket algorithm...
```

--------------------------------

### Training Data JSONL Example

Source: https://github.com/tobi/qmd/blob/main/finetune/CLAUDE.md

Example of a single training example in JSONL format. The output is a list of [type, text] pairs where type is 'lex', 'vec', or 'hyde'. Extra metadata fields are allowed but ignored.

```json
{"query": "auth config", "output": [["hyde", "..."], ["lex", "..."], ["vec", "..."]]}
```

--------------------------------

### QMD query tool example

Source: https://github.com/tobi/qmd/blob/main/skills/qmd/references/mcp-setup.md

Example JSON payload for the query tool, supporting lex, vec, and hyde search types.

```json
{
  "searches": [
    { "type": "lex", "query": "keyword phrases" },
    { "type": "vec", "query": "natural language question" },
    { "type": "hyde", "query": "hypothetical answer passage..." }
  ],
  "limit": 10,
  "collection": "optional",
  "minScore": 0.0
}
```

--------------------------------

### Good Example Output (Score: 85/100)

Source: https://github.com/tobi/qmd/blob/main/finetune/SCORING.md

Example output for the query 'react hooks' that scores well. It includes a Hyde expansion, multiple Lex and Vec expansions, and demonstrates good diversity and format.

```text
hyde: React Hooks allow you to use state and lifecycle features in functional components without writing a class.
lex: react hooks tutorial
lex: usestate useeffect
vec: how to use react hooks in functional components
vec: react hooks best practices guide
```

--------------------------------

### Run from source and install globally

Source: https://github.com/tobi/qmd/blob/main/CLAUDE.md

Use `bun src/cli/qmd.ts <command>` to run the CLI directly from source, or `bun link` to install it globally as 'qmd'.

```sh
bun src/cli/qmd.ts <command>   # Run from source
bun link               # Install globally as 'qmd'
```

--------------------------------

### Install QMD via npm

Source: https://github.com/tobi/qmd/blob/main/README.md

Install the @tobilu/qmd package for use as a library in Node.js or Bun applications.

```sh
npm install @tobilu/qmd
```

--------------------------------

### Vec query examples

Source: https://github.com/tobi/qmd/blob/main/docs/SYNTAX.md

Shows two example vec queries. Vec queries are natural language questions with no special syntax.

```text
vec: how does the rate limiter handle burst traffic
vec: what is the tradeoff between consistency and availability
```

--------------------------------

### Clone and link QMD for development

Source: https://github.com/tobi/qmd/blob/main/README.md

Set up a local development environment by cloning the repository, installing dependencies, and linking the package.

```sh
git clone https://github.com/tobi/qmd
cd qmd
npm install
npm link
```

--------------------------------

### Get options for qmd

Source: https://github.com/tobi/qmd/blob/main/README.md

Options for the qmd get command. Retrieve a document with optional start line and count. -l sets maximum lines, --from overrides the :from suffix, and --no-line-numbers disables line numbering (on by default).

```sh
# Get options
qmd get <file>[:from[:count]]  # Get document; optional start line and count
-l <num>                       # Maximum lines to return
--from <num>                   # Start line (overrides the :from suffix)
--no-line-numbers              # Disable line numbering (on by default)
```

--------------------------------

### Bad Example Output (Score: 15/100)

Source: https://github.com/tobi/qmd/blob/main/finetune/SCORING.md

Example output for the query 'auth' that scores poorly. It lacks valid prefixes and expansions, resulting in zero scores for Format, Diversity, and Hyde.

```text
auth is an important concept that relates to authentication.
The answer should be in Chinese.
The answer should be in Chinese.
```

--------------------------------

### One-time setup and run benchmark from git checkout

Source: https://github.com/tobi/qmd/blob/main/README.md

Indexes the repo's test corpus into its own collection, then runs the benchmark with table or JSON output. The fixture and corpus exist only in a git checkout, not in the published npm package.

```sh
# One-time setup (indexes the repo's test corpus into its own collection)
qmd collection add test/eval-docs --name eval-docs
qmd embed -c eval-docs

# Run the benchmark (table output)
qmd bench src/bench/fixtures/example.json

# JSON output for programmatic analysis
qmd bench src/bench/fixtures/example.json --json
```

--------------------------------

### Changelog release entry with highlights

Source: https://github.com/tobi/qmd/blob/main/skills/release/SKILL.md

Markdown example showing a release entry with a highlights section, including version heading and prose summary.

```markdown
## [1.1.0] - 2026-03-01

QMD now runs on both Node.js and Bun, with up to 2.7x faster reranking
through parallel contexts. GPU auto-detection replaces the unreliable
`gpu: "auto"` with explicit CUDA/Metal/Vulkan probing.
```

--------------------------------

### Install QMD globally via npm or bun

Source: https://github.com/tobi/qmd/blob/main/README.md

Install the package globally using either npm or bun. Choose one command.

```sh
npm install -g @tobilu/qmd
# or
bun install -g @tobilu/qmd
```

--------------------------------

### Claude Code Plugin Installation

Source: https://github.com/tobi/qmd/blob/main/README.md

Commands to install the QMD plugin for Claude Code.

```bash
claude plugin marketplace add tobi/qmd
claude plugin install qmd@qmd
```

--------------------------------

### Output Format Example

Source: https://github.com/tobi/qmd/blob/main/finetune/CLAUDE.md

Shows the expected output format for query expansion: hyde: first, then lex: and vec: lines. hyde: is one line max, lex: 1-3 short keywords, vec: 1-3 natural language variations.

```text
hyde: A hypothetical document passage that would answer the query.
lex: keyword1
lex: keyword2
vec: semantic query reformulation
vec: another semantic variation
```

--------------------------------

### JSON Explain Output Example

Source: https://github.com/tobi/qmd/blob/main/README.md

Example JSON output from the --explain flag, showing score breakdown with FTS/vector scores and RRF fusion math.

```json
{
  "docid": "#6c90f0",
  "score": 0.89,
  "file": "qmd://qmd/README.md",
  "explain": {
    "ftsScores": [0.892, 0.907],
    "vectorScores": [0.540, 0.484],
    "rrf": {
      "rank": 1,
      "weight": 0.75,
      "baseScore": 0.123,
      "topRankBonus": 0.05,
      "totalScore": 0.173,
      "contributions": [
        { "source": "fts", "queryType": "original", "query": "reranking",
          "rank": 1, "weight": 2, "backendScore": 0.892, "rrfContribution": 0.0328 }
      ]
    }
  }
}
```

--------------------------------

### SDK listMetadata examples for metadata discovery

Source: https://github.com/tobi/qmd/blob/main/README.md

Three SDK calls showing flat results, filtering, and pagination. The first returns keys in coverage order split per type; the second narrows by a filter; the third pages through a wide vocabulary.

```typescript
// SDK: one flat result, keys in coverage order, each split per type
const discovery = await store.listMetadata({
  collection: "notes",
  match: { field: "key", operator: "eq", value: "topics" },
  valueLimit: 5,
})
discovery.documents            // active documents in scope
discovery.totalKeys            // keys with a matching entry, before the key window
discovery.remainingKeys        // keys after the window
discovery.keys[0].types[0]     // { type, multiValued, documents, distinctValues, values, remainingValues, range?, collections }
```

```typescript
// Narrowed by a filter: how many documents pass, and what is left to filter on
const published = await store.listMetadata({
  collection: "notes",
  filter: { field: "status", operator: "eq", value: "published" },
})
published.filteredDocuments    // the denominator for every coverage count in this result
```

```typescript
// Page through a wide vocabulary
const nextPage = await store.listMetadata({ keyLimit: 50, keyOffset: 50 })
```

--------------------------------

### Store Creation Modes

Source: https://github.com/tobi/qmd/blob/main/README.md

Three ways to create a store: inline config, YAML config file, or DB-only reopen. Each mode is shown in a separate block within the same example.

```typescript
import { createStore } from '@tobilu/qmd'

// 1. Inline config — no files needed besides the DB
const store = await createStore({
  dbPath: './index.sqlite',
  config: {
    collections: {
      docs: { path: '/path/to/docs', pattern: '**/*.md' },
      notes: { path: '/path/to/notes' },
    },
  },
})
```

```typescript
// 2. YAML config file — collections defined in a file
const store2 = await createStore({
  dbPath: './index.sqlite',
  configPath: './qmd.yml',
})
```

```typescript
// 3. DB-only — reopen a previously configured store
const store3 = await createStore({ dbPath: './index.sqlite' })
```

--------------------------------

### Example index.yml configuration

Source: https://github.com/tobi/qmd/blob/main/README.md

Fully-commented starter template for QMD's YAML config file. Shows top-level settings (global_context, editor_uri, models) and a per-collection entry with path, pattern, ignore, update, includeByDefault, and context. Editing this file changes which directories and models QMD uses, but does not re-index on its own; run `qmd update` after changing path, pattern, or ignore, and `qmd embed` after changing models.embed.

```yaml
# ~/.config/qmd/index.yml

# Context applied to every collection (system-message style). Optional.
global_context: "Knowledge base for my projects"

# Terminal hyperlink template for search results. Optional.
# Overridden by the QMD_EDITOR_URI env var. See "Editor Links" below.
editor_uri: "vscode://file{path}:{line}:{col}"

# Override the default GGUF models per role. Optional — omit to use the
# built-in defaults. `qmd init` writes this block pre-filled with the
# resolved defaults. See "Model Configuration" for the default URIs.
models:
  embed: "hf:ggml-org/embeddinggemma-300M-GGUF/embeddinggemma-300M-Q8_0.gguf"
  rerank: "hf:ggml-org/Qwen3-Reranker-0.6B-Q8_0-GGUF/qwen3-reranker-0.6b-q8_0.gguf"
  generate: "hf:tobil/qmd-query-expansion-1.7B-gguf/qmd-query-expansion-1.7B-q4_k_m.gguf"

# One entry per collection. The key is the collection name.
collections:
  notes:
    path: /Users/me/notes        # absolute path to index (required)
    pattern: "**/*.md"           # glob mask (default: **/*.md)
    ignore:                      # glob patterns to exclude from indexing
      - "Archive/**"
      - "**/drafts/**"
    update: "git pull --rebase"  # bash command run before each `qmd update`
    includeByDefault: true       # include in unscoped queries (default: true)
    context:                     # path prefix → description; longest match wins
      "/": "Personal notes and ideas"
      "/work": "Work-related notes"

```

--------------------------------

### TTY Output Example

Source: https://github.com/tobi/qmd/blob/main/README.md

Shows the colorized CLI output format when stdout is a TTY, with clickable hyperlinks and result details.

```text
docs/guide.md:42 #a1b2c3
Title: Software Craftsmanship
Context: Work documentation
Score: 93%

This section covers the **craftsmanship** of building
quality software with attention to detail.
See also: engineering principles


notes/meeting.md:15 #d4e5f6
Title: Q4 Planning
Context: Personal notes and ideas
Score: 67%

Discussion about code quality and craftsmanship
in the development process.
```

--------------------------------

### Run QMD MCP in HTTP mode

Source: https://github.com/tobi/qmd/blob/main/skills/qmd/references/mcp-setup.md

Start the QMD MCP server in HTTP mode, optionally as a daemon, and stop it.

```bash
qmd mcp --http              # Port 8181
qmd mcp --http --daemon     # Background
qmd mcp stop                # Stop daemon
```

--------------------------------

### Install Homebrew SQLite (macOS)

Source: https://github.com/tobi/qmd/blob/main/README.md

Required on macOS for SQLite extension support. Run before using QMD.

```sh
brew install sqlite
```

--------------------------------

### Search and retrieve documents by docid

Source: https://github.com/tobi/qmd/blob/main/CLAUDE.md

Shows how docids appear in search results and how to use them with get and multi-get. The leading '#' is optional for get. Multi-get accepts comma-separated docids.

```sh
# Search returns docid in results
qmd search "query" --json
# Output: [{"docid": "#abc123", "score": 0.85, "file": "docs/readme.md", ...}]

# Get document by docid
qmd get "#abc123"
qmd get abc123              # Leading # is optional

# Docids also work in multi-get comma-separated lists
qmd multi-get "#abc123, #def456"
```

--------------------------------

### QMD CLI search examples

Source: https://github.com/tobi/qmd/blob/main/skills/qmd/SKILL.md

Three shell commands demonstrating QMD CLI usage: exact-title lookup with `qmd search`, semantic concept lookup with `qmd query` using intent/lex/vec fields, and source lookup with `qmd search` specifying collection and result count.

```bash
# Exact-ish title lookup
qmd search '"arm the rebels" merchants tools big companies' -c concepts
```

```bash
# Semantic concept lookup
qmd query $'intent: Find the customer proximity concept, not generic customer delight.\nlex: support pseudonymous merchant customer interviews\nvec: founder stays close to merchant reality through support and product use'
```

```bash
# Source lookup
qmd search "six-week cadence WhatsApp merchant relationships Shawn Ryan" -c sources -n 10
```

--------------------------------

### Fetch sources with qmd get and multi-get

Source: https://github.com/tobi/qmd/blob/main/skills/qmd/SKILL.md

Use `qmd get` to fetch a single source by docid or qmd:// path, and `qmd multi-get` to fetch multiple sources by comma-separated docids, brace-expanded paths, or glob patterns. `multi-get` is useful for comparing several hits or gathering context across pages.

```bash
qmd get "#abc123"
qmd get qmd://concepts/ai-before-headcount.md
qmd multi-get "#abc123,#def432" --format md
qmd multi-get 'concepts/{ai-before-headcount.md,data-informed-not-metric-driven.md}' --format md
qmd multi-get 'sources/podcast-2025-*.md' -l 80
```

--------------------------------

### BM25 lexical search examples

Source: https://github.com/tobi/qmd/blob/main/skills/qmd/SKILL.md

Use `qmd search` when you know exact words, titles, names, code symbols, or rare phrases. The first example searches for a phrase with spaces; the second uses a quoted exact phrase and restricts to the 'concepts' collection.

```bash
qmd search "cockpit OKR Goodhart" -n 10
```

```bash
qmd search '"AI Before Headcount"' -c concepts -n 5
```

--------------------------------

### Intent line example

Source: https://github.com/tobi/qmd/blob/main/docs/SYNTAX.md

Shows an intent line providing background context to disambiguate ambiguous queries. At most one intent: line per query document, and it cannot appear alone.

```text
intent: web page load times and Core Web Vitals
lex: performance
vec: how to improve performance
```

--------------------------------

### Query and Search Examples

Source: https://github.com/tobi/qmd/blob/main/README.md

Common qmd query and search invocations: limit results, output as markdown or JSON, inspect scoring, and use a separate index.

```sh
# Get 10 results with minimum score 0.3
qmd query -n 10 --min-score 0.3 "API design patterns"

# Output as markdown for LLM context
qmd search --md --full "error handling"

# JSON output for scripting
qmd query --json "quarterly reports"

# Inspect how each result was scored (RRF + rerank blend)
qmd query --json --explain "quarterly reports"

# Use separate index for different knowledge base
qmd --index work search "quarterly reports"
```

--------------------------------

### get

Source: https://github.com/tobi/qmd/blob/main/skills/qmd/references/mcp-setup.md

Retrieve a document by path or #docid.

```APIDOC
## get

### Description
Retrieve a document by path or #docid.

### Parameters
- **path** (string) - Required - File path or #docid
- **full** (bool) - Optional - Return full content
- **lineNumbers** (bool) - Optional - Add line numbers

### Request Example
{
  "path": "doc.md",
  "full": true,
  "lineNumbers": false
}

### Response
#### Success Response
- **content** (string) - Document content

#### Response Example
{
  "content": "# Title\n\nBody..."
}
```

--------------------------------

### Example of model output for query expansion

Source: https://github.com/tobi/qmd/blob/main/finetune/README.md

Shows the structured output format produced by the trained model for a raw query like 'auth config'. Lines prefixed with 'hyde:', 'lex:', and 'vec:' feed into different search backends.

```text
hyde: Authentication can be configured by setting the AUTH_SECRET environment variable.
lex: authentication configuration
lex: auth settings setup
vec: how to configure authentication settings
vec: authentication configuration options
```

--------------------------------

### Expand query example

Source: https://github.com/tobi/qmd/blob/main/docs/SYNTAX.md

Shows an expand query with the explicit expand: prefix and the equivalent untyped form. Both call the local query expansion model, which generates lex, vec, and hyde variations automatically.

```text
expand: error handling best practices
# equivalent
error handling best practices
```

--------------------------------

### qmd collection metadata examples

Source: https://github.com/tobi/qmd/blob/main/README.md

Shows how to use `qmd collection metadata` to inspect metadata keys and values. The first command lists all keys, the second filters by key, the third does a reverse lookup by value, the fourth uses an `and` condition, the fifth combines `--match` and `--filter`, and the sixth shows a search with a validated filter.

```sh
# Which keys does this collection use? (`qmd collection show notes` previews the top five)
qmd collection metadata notes

# Everything about one key: coverage, distinct count, top values
qmd collection metadata notes --match '{"field":"key","operator":"eq","value":"topics"}'

# Reverse lookup: which keys hold this value
qmd collection metadata notes --match '{"field":"value","operator":"eq","value":"docs-team"}'

# Values of one key matching a pattern
qmd collection metadata notes --match '{
  "operator": "and",
  "operands": [
    { "field": "key", "operator": "eq", "value": "topics" },
    { "field": "value", "operator": "prefix", "value": "sql" }
  ]
}'

# What remains after a filter, before committing to it in a query
qmd collection metadata notes \
  --match '{"field":"key","operator":"eq","value":"topics"}' \
  --filter '{"field":"status","operator":"eq","value":"published"}'

# Then search with the filter you just validated
qmd query "dependency injection" -c notes --filter '{
  "operator": "and",
  "operands": [
    { "field": "status", "operator": "eq", "value": "published" },
    { "field": "topics", "operator": "all", "value": ["typescript"] }
  ]
}'
```

--------------------------------

### Changelog detailed changes and fixes sections

Source: https://github.com/tobi/qmd/blob/main/skills/release/SKILL.md

Markdown example showing the detailed changelog structure with '### Changes' and '### Fixes' sections, including contributor credits.

```markdown
### Changes

- Runtime: support Node.js (>=22) alongside Bun. The `qmd` wrapper
  auto-detects a suitable install via PATH. #149 (thanks @igrigorik)
- Performance: parallel embedding & reranking — up to 2.7x faster on
  multi-core machines.

### Fixes

- Prevent VRAM waste from duplicate context creation during concurrent
  `embedBatch` calls. #152 (thanks @jkrems)
```

--------------------------------

### MCP/HTTP query with intent

Source: https://github.com/tobi/qmd/blob/main/docs/SYNTAX.md

MCP/HTTP query with an intent field to guide the search.

```json
{
  "searches": [
    { "type": "lex", "query": "performance" }
  ],
  "intent": "web page load times and Core Web Vitals"
}
```

--------------------------------

### MCP Tool: get

Source: https://github.com/tobi/qmd/blob/main/README.md

Retrieves a file or a specific range of lines from a document by path, docid, or a `path:from:count` specifier.

```APIDOC
## MCP Tool: get

### Description
Retrieves a file or a specific range of lines from a document by path, docid, or a `path:from:count` specifier.

### Parameters
#### Tool Parameters
- **file** (string) - Required - Path, docid (`#abc123`), or `path:from:count` (e.g. `#abc123:120:40`).
- **fromLine** (number) - Optional - Start line (1-indexed); overrides the `:from` suffix.
- **maxLines** (number) - Optional - Limit returned lines.
- **lineNumbers** (boolean) - Optional - Prefix lines with numbers (default true).
```

--------------------------------

### Hyde query example

Source: https://github.com/tobi/qmd/blob/main/docs/SYNTAX.md

Shows a hyde query, which is a hypothetical answer passage of 50-100 words describing the expected answer.

```text
hyde: The rate limiter uses a sliding window algorithm with a 60-second window. When a client exceeds 100 requests per minute, subsequent requests return 429 Too Many Requests.
```

--------------------------------

### qmd collection metadata notes output

Source: https://github.com/tobi/qmd/blob/main/README.md

Example output from `qmd collection metadata notes` showing per-key blocks with coverage, distinct counts, and value distributions. The output includes a note about using `--value-limit`, `--value-offset`, or `--all-values` for more values.

```sh
qmd collection metadata notes
```

```text
topics  string[]  388 of 480 documents  1,204 distinct
  typescript    140
  sqlite         92
  search         77
  architecture   61
  sqlite-vec     44
  mcp            39
  embeddings     35
  agents         31
  cli            28
  testing        26
1,194 more values, use --value-limit <n>, --value-offset <n>, or --all-values

priority  number  205 of 480 documents  5 distinct
  min 1  median 3  max 5
  1 (12)  2 (40)  3 (88)  4 (50)  5 (15)

reviewed  boolean  480 of 480 documents
  true 61  false 419
```

--------------------------------

### Filter examples for qmd search and query

Source: https://github.com/tobi/qmd/blob/main/README.md

Shows a simple filter and a composed filter using logical operators. The composed filter works with search, vsearch, and query. Filters are JSON ASTs discriminated by operator.

```sh
# One condition
qmd search "authentication" \
  --filter '{"field":"status","operator":"eq","value":"published"}'

```

```sh
# Composed conditions — works with search, vsearch, and query
qmd query "dependency injection" --filter '{
  "operator": "and",
  "operands": [
    { "field": "topics", "operator": "all", "value": ["typescript", "programming"] },
    { "field": "status", "operator": "nin", "value": ["draft", "archived"] },
    { "operator": "or", "operands": [
      { "field": "priority", "operator": "gte", "value": 3 },
      { "field": "reviewed", "operator": "eq", "value": true }
    ] },
    { "field": "topics", "operator": "prefix", "value": "sql", "caseInsensitive": true },
    { "operator": "not", "operand": { "field": "audience", "operator": "eq", "value": "internal" } }
  ]
}'

```

--------------------------------

### Default line-numbered output with docid and path

Source: https://github.com/tobi/qmd/blob/main/skills/qmd/SKILL.md

Shows the default output of `qmd get` and `multi-get`: line-numbered content with a header containing the qmd:// path and #docid. Cite the docid and exact line numbers in answers, and use the numbers to request the next slice.

```text
qmd://concepts/note.md  #abc123
---

1: # Metrics as instruments
2:
3: Treat dashboards like cockpit instruments...
```

--------------------------------

### qmd collection metadata with --filter and --value-limit

Source: https://github.com/tobi/qmd/blob/main/README.md

Shows how `--filter` narrows the population and adds a `filter:` line to the output. The example uses `--value-limit 5` to limit values shown per key.

```sh
qmd collection metadata notes \
  --match '{"field":"key","operator":"eq","value":"topics"}' \
  --filter '{"field":"status","operator":"eq","value":"published"}' \
  --value-limit 5
```

```text
filter: 312 of 480 documents

topics  string[]  260 of 312 documents  811 distinct
  typescript    104
  sqlite         70
  search         58
  architecture   40
  mcp            31
806 more values, use --value-limit <n>, --value-offset <n>, or --all-values
```

--------------------------------

### Wrong vs right way to read line range

Source: https://github.com/tobi/qmd/blob/main/skills/qmd/SKILL.md

Shows the incorrect approach of piping `qmd get` through `sed` and the correct approach using the `:from:count` suffix. Piping defeats docid resolution, virtual-path lookups, line numbering, and the header, and is slower and more error-prone.

```bash
Wrong: `qmd get "#abc123" | sed -n '120,160p'`
Right: `qmd get "#abc123:120:40"`
```

--------------------------------

### Prepare Data Command

Source: https://github.com/tobi/qmd/blob/main/finetune/CLAUDE.md

Runs the data preparation script which loads data via schema, applies Qwen3 chat template, deduplicates, and splits into train/val files. Creates ephemeral files in data/train/.

```bash
uv run dataset/prepare_data.py
# Creates: data/train/train.jsonl, data/train/val.jsonl (ephemeral)
```

--------------------------------

### Retrieval: get, getDocumentBody, multiGet

Source: https://github.com/tobi/qmd/blob/main/README.md

Retrieve documents by path or docid with get(), get document body with line range using getDocumentBody(), and batch retrieve by glob or comma-separated list with multiGet(). The get() result may contain an error property; otherwise it exposes title, displayPath, and context.

```typescript
// Get a document by path or docid
const doc = await store.get("docs/readme.md")
const byId = await store.get("#abc123")

if (!("error" in doc)) {
  console.log(doc.title, doc.displayPath, doc.context)
}

// Get document body with line range
const body = await store.getDocumentBody("docs/readme.md", {
  fromLine: 50,
  maxLines: 100,
})

// Batch retrieve by glob or comma-separated list
const { docs, errors } = await store.multiGet("docs/**/*.md", {
  maxBytes: 20480,
})
```

--------------------------------

### Run all tests with vitest and bun

Source: https://github.com/tobi/qmd/blob/main/CLAUDE.md

Run the full test suite using either `npx vitest run --reporter=verbose test/` or `bun test --preload ./src/test-preload.ts test/`.

```sh
npx vitest run --reporter=verbose test/
bun test --preload ./src/test-preload.ts test/
```

--------------------------------

### Cloud training via HuggingFace Jobs

Source: https://github.com/tobi/qmd/blob/main/finetune/README.md

Commands to run SFT training, evaluation, and GGUF conversion using HuggingFace Jobs. Includes a note that GRPO is experimental and moved to finetune/experiments/grpo.

```bash
# 1. SFT: teach the model the output format (~45 min on A10G, ~$1.50)
hf jobs uv run --flavor a10g-large --secrets HF_TOKEN --timeout 2h jobs/sft.py

# 2. Evaluate against test queries (needs local GPU or use eval job)
uv run eval.py tobil/qmd-query-expansion-1.7B

# 3. Convert to GGUF for local deployment (Ollama, llama.cpp)
uv run convert_gguf.py --size 1.7B

# NOTE: GRPO is currently experimental and moved to finetune/experiments/grpo
# if you want to run it manually, use:
#   cd finetune && uv run python experiments/grpo/grpo.py
```

--------------------------------

### Local training commands

Source: https://github.com/tobi/qmd/blob/main/finetune/README.md

Commands to run SFT training locally and the experimental GRPO script. Requires a GPU.

```bash
uv run train.py sft  --config configs/sft.yaml

# Experimental GRPO
cd finetune && uv run python experiments/grpo/grpo.py
```

--------------------------------

### qmd CLI options for search, retrieval, and output format

Source: https://github.com/tobi/qmd/blob/main/CLAUDE.md

Lists command-line options for search, get/multi-get, and output format. Includes defaults like --max-bytes 10KB and notes that legacy --json/--csv/--md/--xml/--files aliases still work.

```sh
# Search & retrieval
-c, --collection <name>  # Restrict search to collection(s) (repeatable)
-n <num>                 # Number of results
--all                    # Return all matches
--min-score <num>        # Minimum score threshold
--full                   # Show full document content
--intent <text>          # Describe what you're after to sharpen ranking (query)
--no-rerank              # Skip LLM reranking (faster, lower quality)
--full-path              # Show on-disk paths instead of qmd:// URIs

# Get / multi-get
-l <num>                 # Maximum lines per file
--max-bytes <num>        # Skip files larger than this (default 10KB)
--no-line-numbers        # Disable line numbers (on by default for get/multi-get)

# Output format (search, query, multi-get)
--format <kind>          # cli (default) | json | csv | md | xml | files
                         # legacy --json/--csv/--md/--xml/--files still work as aliases
```

--------------------------------

### Prepare and Validate Data Pipeline

Source: https://github.com/tobi/qmd/blob/main/finetune/README.md

Prepares training data by formatting for the Qwen3 chat template, deduplicating, and splitting into train/val. Then validates data quality with just validate.

```bash
# Format for Qwen3 chat template, deduplicate, split train/val
uv run dataset/prepare_data.py

# Validate data quality
just validate
```

--------------------------------

### GET /health

Source: https://github.com/tobi/qmd/blob/main/skills/qmd/references/mcp-setup.md

Liveness check endpoint. Returns a simple health status.

```APIDOC
## [GET] /health

### Description
Liveness check endpoint. Returns a simple health status.

### Method
GET

### Endpoint
/health

### Response
#### Success Response (200)
- **status** (string) - Health status (e.g., "ok")

#### Response Example
{
  "status": "ok"
}
```

--------------------------------

### Get full path with --full-path

Source: https://github.com/tobi/qmd/blob/main/skills/qmd/SKILL.md

Use `--full-path` with `qmd get` to replace the qmd:// URL and docid header with the document's on-disk path, falling back to the canonical header if the file no longer exists. This is needed when handing a path to tools like Read, Edit, or an editor.

```text
$ qmd get "#abc123" --full-path
/Users/you/notes/concepts/note.md
---

1: # Metrics as instruments
```

--------------------------------

### Use GGUF with Ollama

Source: https://github.com/tobi/qmd/blob/main/finetune/README.md

Downloads the quantized GGUF file, creates a Modelfile, and creates/runs the model with Ollama. Requires the GGUF file to be in the current directory.

```bash
huggingface-cli download tobil/qmd-query-expansion-1.7B-gguf \
    qmd-query-expansion-1.7B-q4_k_m.gguf --local-dir .

echo 'FROM ./qmd-query-expansion-1.7B-q4_k_m.gguf' > Modelfile
ollama create qmd-expand -f Modelfile
ollama run qmd-expand
```

--------------------------------

### Convert to GGUF with convert_gguf.py

Source: https://github.com/tobi/qmd/blob/main/finetune/README.md

Merges base + SFT and optionally GRPO adapters into a single model, then produces quantized GGUF files. Use the preset for 1.7B or specify custom models with --base, --sft, --grpo, and --output.

```bash
# Use preset for 1.7B
uv run convert_gguf.py --size 1.7B

# Custom models
uv run convert_gguf.py --base Qwen/Qwen3-1.7B \
                       --sft tobil/qmd-query-expansion-1.7B-sft \
                       --grpo tobil/qmd-query-expansion-1.7B-grpo \
                       --output tobil/qmd-query-expansion-1.7B-gguf
```

--------------------------------

### GET /health

Source: https://github.com/tobi/qmd/blob/main/README.md

Liveness check endpoint that provides uptime information for the server.

```APIDOC
## [GET] /health

### Description
Liveness check endpoint that provides uptime information for the server.

### Method
GET

### Endpoint
/health

### Response
#### Success Response (200)
- Uptime information
```

--------------------------------

### Run GRPO training script

Source: https://github.com/tobi/qmd/blob/main/finetune/experiments/grpo/README.md

Run the experimental GRPO training script from the repository root, or use the unified entrypoint with the GRPO configuration file.

```bash
# Recommended default: run from repo root
cd /home/tobi/qmd
uv run finetune/experiments/grpo/grpo.py

# Or use unified entrypoint (deprecated in main pipeline):
uv run train.py grpo --config finetune/experiments/grpo/grpo.yaml
```

--------------------------------

### Key Files Directory Structure

Source: https://github.com/tobi/qmd/blob/main/finetune/CLAUDE.md

Shows the top-level layout of the finetune/ directory with key files and subdirectories.

```text
finetune/
├── reward.py          # Scoring function (single source of truth)
├── train.py           # SFT training entrypoint
├── eval.py            # Generate and score expansions
├── convert_gguf.py    # GGUF conversion
├── SCORING.md         # Detailed scoring rubric
├── CLAUDE.md          # This file
├── Justfile           # Common commands
├── data/              # All training JSONL files (strict schema)
├── dataset/           # Schema + data tools (Pydantic-based)
├── jobs/              # Self-contained HuggingFace Jobs scripts
├── configs/           # Training configs (sft.yaml)
├── evals/             # Test queries
├── experiments/       # Experimental configs (LFM2, GEPA, GRPO)
└── outputs/           # Local training outputs (gitignored)
```

--------------------------------

### Run SFT training for qmd

Source: https://github.com/tobi/qmd/blob/main/finetune/README.md

Runs the SFT stage for the qmd training pipeline. The first command trains with the config file configs/sft.yaml. The second command, with --dry-run, previews the configuration without training.

```bash
uv run train.py sft --config configs/sft.yaml
```

```bash
uv run train.py sft --config configs/sft.yaml --dry-run  # preview config
```

--------------------------------

### Run experimental GRPO training

Source: https://github.com/tobi/qmd/blob/main/finetune/README.md

Runs the experimental GRPO training script (experiments/grpo/grpo.py) from the finetune directory. This is an optional, experimental path not part of the default production workflow.

```bash
cd finetune && uv run python experiments/grpo/grpo.py
```

--------------------------------

### QMD CLI Commands

Source: https://github.com/tobi/qmd/blob/main/CLAUDE.md

Lists all QMD command-line commands with their usage and options. Use Bun instead of Node.js for running QMD.

```sh
qmd collection add . --name <n>   # Create/index collection
qmd collection list               # List all collections with details
qmd collection remove <name>      # Remove a collection by name
qmd collection rename <old> <new> # Rename a collection
qmd collection metadata [name...] # Discover metadata keys, types, and value counts (--match, --filter, --key-limit, --value-limit)
qmd init                          # Create a project-local .qmd index
qmd ls [collection[/path]]        # List collections or files in a collection
qmd context add [path] "text"     # Add context for path (defaults to current dir)
qmd context list                  # List all contexts
qmd context check                 # Check for collections/paths missing context
qmd context rm <path>             # Remove context
qmd get <file>[:from[:count]]     # Get by path or docid (#abc123); optional line range
qmd multi-get <pattern>           # Get multiple docs by glob or comma-separated list
qmd status                        # Show index status and collections
qmd doctor                        # Diagnose config, index, model, and device issues
qmd update                        # Re-index collections; configured update hooks run first
qmd trust [list|revoke]           # Approve a checked-in .qmd config's hooks/paths/models
qmd embed                         # Generate vector embeddings (uses node-llama-cpp)
qmd query <query>                 # Search with query expansion + reranking (recommended)
qmd search <query>                # Full-text keyword search (BM25, no LLM)
qmd vsearch <query>               # Vector similarity search (no reranking)
qmd bench <fixture.json>          # Run search-quality benchmarks
qmd mcp                           # Start MCP server (stdio transport)
qmd mcp --http [--port N]         # Start MCP server (HTTP, default port 8181)
qmd mcp --http --daemon           # Start as background daemon
qmd mcp stop                      # Stop background MCP daemon
```

--------------------------------

### Configure QMD MCP for OpenClaw

Source: https://github.com/tobi/qmd/blob/main/skills/qmd/references/mcp-setup.md

Add the QMD MCP server to OpenClaw's configuration file.

```json
{
  "mcp": {
    "servers": {
      "qmd": { "command": "qmd", "args": ["mcp"] }
    }
  }
}
```

--------------------------------

### Check qmd health and status

Source: https://github.com/tobi/qmd/blob/main/skills/qmd/SKILL.md

Run diagnostics and status checks. `qmd doctor` verifies config, model cache, device/GPU setup, vector fingerprints, and environment overrides; run it before changing configuration if a model-backed command fails.

```bash
qmd doctor
qmd status
qmd pull
```

--------------------------------

### Inspect ranking with qmd query --explain

Source: https://github.com/tobi/qmd/blob/main/skills/qmd/SKILL.md

Use this command to inspect ranking when you have nothing to expand (a single rare token or verbatim phrase). The `--format json` and `--explain` flags output ranking details.

```bash
qmd query --format json --explain $'intent: ...\nlex: ...\nvec: ...'  # inspect ranking
```

--------------------------------

### Configure QMD MCP for Claude Code

Source: https://github.com/tobi/qmd/blob/main/skills/qmd/references/mcp-setup.md

Add the QMD MCP server to Claude Code's settings.json file.

```json
{
  "mcpServers": {
    "qmd": { "command": "qmd", "args": ["mcp"] }
  }
}
```

--------------------------------

### Quality Scoring Self-Test

Source: https://github.com/tobi/qmd/blob/main/finetune/CLAUDE.md

Runs the reward.py self-test to verify the scoring function.

```bash
uv run reward.py   # Self-test
```
