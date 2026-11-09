# Monorepo Strategy & Content Proposal (Gemini)

This proposal synthesizes the architectural requirements for the `skogai/monorepo`, building on the industry survey data compiled in [monorepo-claude.md](file:///.skogai/research/monorepo-claude.md) and the pragmatic defaults outlined in [monorepo-codex.md](file:///.skogai/research/monorepo-codex.md).

---

## 1. Executive Summary & Guiding Principles

The primary mission of the SkogAI monorepo is to serve as a **unified, AI-native development environment** where human engineers and autonomous agents (Claude, Codex, Gemini) collaborate seamlessly.

To achieve this without falling into monorepo bloat or tooling gridlock, the monorepo should adhere to four principles:
1. **Zero Hidden State / Fresh-Clone Guarantee:** Any agent or engineer must be able to clone the repo, run a single bootstrap command, and execute tests or start services locally.
2. **Polyglot Simplicity with Single Lockfiles:** Python is primary (managed via `uv` workspaces), with clean boundaries for TypeScript (`pnpm`), shell scripts, and containers.
3. **Docs & Agents as First-Class Citizens:** Agent prompts, personas, evaluation benchmarks, and documentation live alongside the code they operate on.
4. **Local-First Search with Machine-Readable Discovery:** Exact-match tools (`ripgrep`), lightweight local vector search (`qmd`/SQLite vector), and `llms.txt` ensure agents can orient themselves instantly without high retrieval latency.

---

## 2. Monorepo Scope: What Belongs Inside vs. Outside

A clear boundary prevents monorepos from becoming dumping grounds.

```
┌────────────────────────────────────────────────────────────────────────┐
│                          IN MONOREPO                                   │
│                                                                        │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐  │
│  │   AI & Agents    │  │  Apps & Services │  │   Shared Packages    │  │
│  │ .skogai/, mcps/, │  │  FastAPI, bots,  │  │ py-core, ts-types,   │  │
│  │ prompts, evals   │  │  dashboards      │  │ db-models, schemas   │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────┘  │
│                                                                        │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐  │
│  │ Developer Tools  │  │   Docs & ADRs    │  │    Infrastructure    │  │
│  │ bin/, scripts/,  │  │ MkDocs, guides,  │  │ docker-compose,      │  │
│  │ Taskfile, mise   │  │ architecture     │  │ GitHub Actions CI    │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
                               ▲
                      Keep Separate / External
                               ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         OUT OF MONOREPO                                │
│  - Raw / large AI training weights or datasets (>50MB -> S3/GCS)       │
│  - Unencrypted API keys and production secrets (use fnox / 1Password)  │
│  - Isolated external client deliverables with distinct licensing       │
│  - Heavy ephemeral runtime logs or transient cache files               │
└────────────────────────────────────────────────────────────────────────┘
```

### In the Monorepo:
- **Autonomous Agents & MCPs (`mcps/`, `.skogai/`):** Model Context Protocol servers, agent prompts, skills, and regression evals.
- **Core Deployable Services (`apps/`):** Backend APIs (FastAPI), web interfaces, Discord/Slack integrations, and data ingestion workers.
- **Shared Domain Libraries (`packages/`):** Shared database schemas, API clients, authentication utilities, and LLM abstraction layers.
- **Developer Tooling & Wrappers (`bin/`, `scripts/`):** Unified agent launcher scripts (`bin/claude`, `bin/gemini`, `bin/codex`), setup hooks, and encryption utilities.
- **Living Documentation & ADRs (`docs/`):** Architecture decision records, operational runbooks, and API contracts.

### Outside the Monorepo:
- **Large binary blobs & model weights:** Store in object storage (S3/Cloud Storage) with pointers or fetch scripts.
- **Production secrets & plain tokens:** Store secrets encrypted via `fnox`/GPG/age or pulled at runtime via environment managers.
- **Ephemeral scratch/artifacts:** Strictly gitignored.

---

## 3. Recommended Directory Blueprint

```
skogai/
├── .github/
│   ├── workflows/             # CI matrix: lint, test, docker smoke tests
│   └── pull_request_template.md
├── .skogai/                   # Agent context, research spikes & personas
│   ├── research/              # Agent comparative research & design specs
│   ├── prompts/               # Version-controlled system prompts & directives
│   └── evals/                 # Benchmark prompts and regression assertions
├── apps/                      # Deployable applications & services
│   ├── api/                   # Core Python FastAPI service
│   └── web/                   # Web interface / frontend dashboard (when needed)
├── mcps/                      # Model Context Protocol servers
│   ├── postgres-mcp/          # Database inspection & query MCP
│   └── search-mcp/            # Vector / knowledge retrieval MCP
├── packages/                  # Shared libraries across applications
│   ├── py-core/               # Shared Python types, db models, logging, LLM client
│   └── ts-types/              # Shared TypeScript definitions (if fullstack)
├── docs/                      # Documentation-as-Code
│   ├── adrs/                  # Architecture Decision Records (Context/Decision/Status)
│   ├── architecture/          # High-level architecture and data flows
│   └── guides/                # Developer onboarding, quickstarts
├── bin/                       # Agent and CLI launcher scripts (bin/claude, bin/gemini)
├── scripts/                   # Bootstrapping, secret hydration (fnox), DB migrations
├── docker-compose.yml         # Local dependencies (Postgres + pgvector, Redis)
├── mise.toml                  # Pinned tool versions (Python, uv, Node, pnpm, Task)
├── pyproject.toml             # Root uv workspace configuration
├── Taskfile.yml               # Unified polyglot task runner
├── llms.txt                   # High-density repo guide for agent consumption
├── README.md                  # Fresh-clone contract & quickstart
└── TODO.md                    # Immediate tactical backlog
```

---

## 4. Key Toolchain & Technology Choices

| Layer | Recommended Choice | Rationale |
|---|---|---|
| **Runtime & Tool Management** | **`mise` (`mise.toml`)** | Standardizes Python, uv, Node, and CLI tools in one file. Replaces pyenv/nvm/asdf. Perfect for `TODO.md` bootstrap. |
| **Python Workspace** | **`uv` workspaces** (`pyproject.toml`) | Instant resolution, single `uv.lock`, seamless sharing of local package dependencies (`apps/api` depends on `packages/py-core`). |
| **Node / TS Workspace** | **`pnpm` + Turborepo** | Zero-copy hard links, fast caching. Only introduced when UI apps are added. |
| **Task Orchestration** | **`Taskfile` (`go-task`)** | Language-agnostic commands (`task dev`, `task test`, `task lint`). Self-documenting and easier for agents than Makefiles. |
| **Database & Vector RAG** | **PostgreSQL + `pgvector`** | Dual-purpose: transactional data + semantic search. Zero extra infrastructure overhead locally (via Docker Compose). |
| **Knowledge Base** | **MkDocs Material + `llms.txt`** | Fast offline search, native Markdown rendering, Git-tracked ADRs, and machine-readable `llms.txt` for agents. |
| **Secrets Management** | **`fnox` + `.env.example`** | Secure encrypted dotfiles/keys, keeping tokens out of git history while allowing automated hydration. |
| **Issue Tracking** | **GitHub Issues + Projects** | Tight integration with PRs, automated status transitions on merge, no cross-tool synchronization overhead. |

---

## 5. Decision Framework: "Should this live in the monorepo?"

Use this 4-point rubric whenever considering whether a new project belongs in the repo:

1. **Atomic Refactoring:** Will changes to this component frequently require synchronized changes to another component or shared schema? *(If yes → Monorepo)*
2. **Context Sharing for Agents:** Does an agent working on this feature need immediate access to shared models, docs, or prompt definitions? *(If yes → Monorepo)*
3. **Deployment Independence:** Can this service be deployed independently via Docker or CI without breaking others? *(Monorepo supports this via path-filtered CI)*
4. **Secret Isolation:** Does this component require access to restricted keys that should not be visible to general contributors? *(If separate credentials cannot be scoped via CI secrets → consider external)*

---

## 6. Phased Implementation Roadmap

1. **Phase 1: Foundation (Day 1)**
   - Add root `mise.toml` pinning Python, `uv`, and `task`.
   - Configure root `pyproject.toml` with `[tool.uv.workspace]` pointing to `apps/*` and `packages/*`.
   - Setup `Taskfile.yml` with basic `test`, `lint`, and `check` targets.
   - Formalize `TODO.md` items (`fnox` encryption & bootstrapping).

2. **Phase 2: Knowledge & Agent Setup (Week 1)**
   - Add `docs/adrs/` with ADR-0001 (Monorepo Architecture Decision).
   - Generate `llms.txt` at repo root describing repository structure and conventions.
   - Establish `.skogai/prompts/` and `.skogai/evals/` standards.

3. **Phase 3: Service Scaffolding & CI (Week 2)**
   - Add `docker-compose.yml` for Postgres 16 with `pgvector`.
   - Add GitHub Actions CI workflow running `uv run ruff check` and `uv run pytest`.
