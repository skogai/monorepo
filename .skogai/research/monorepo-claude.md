Starting the research now: I'll look at what's actually standard for monorepo tooling, searchable markdown/RAG, and ticket tracking as of late 2026.

Here's what the research says. Many of the monorepo and tracker comparisons are SEO blog posts, so I leaned on the Stack Overflow survey as the hard adoption data. That survey is the 2025 edition, the latest I found.

**Baseline (near-universal)**
- GitHub is the most used code documentation and collaboration tool at 81%, followed by Jira at 46% and GitLab at 36%.
- Docker jumped 17 points to 71.1% usage, which makes it close to universal.
- Markdown remains the most admired documentation tool, and GitHub replaced Jira as the most desired collaboration tool.

**Monorepo structure**
- pnpm workspaces has become the default baseline for JavaScript monorepos.
- The most common production setup is pnpm for installs plus Turborepo for task orchestration and caching. Nx fits better when the repo is polyglot.
- Lerna is effectively legacy.
- These tools are JavaScript/TypeScript-centric. For a non-JS monorepo, Nx or Moon are the polyglot options.

**Searchable markdown / RAG**
- This is the least settled category. No single standard exists, and the field is mostly new local-first tools.
- qmd is a lightweight RAG component for local Markdown, with a CLI, SDK, and MCP server so agents can search before acting.
- Many others expose the same shape: markdown in, hybrid semantic + keyword search, MCP out (raglike.md, brain.md, various Qdrant/Ollama servers).
- The emerging convention around the docs themselves is Git + Markdown plus machine-readable layers such as llms.txt and MCP servers. llms.txt was proposed in September 2024 and is now an informal standard.
- Plain `grep`/`rg` remains the baseline for exact-match search.

**Tickets**
- Linear has displaced Jira at modern tech companies founded after roughly 2018, while Jira persists at enterprises committed to the Atlassian stack.
- GitHub Issues is built into the repo and links issues to PRs and commits. GitHub Projects is included with GitHub plans.
- Notion works as a ticket tracker but is a weaker fit: its GitHub integration is basic compared with Linear and Jira.
- For "generic and always works," GitHub Issues is the only option that adds no extra account or service.

**Docs workflow**
- Docs-as-code is the default for engineering teams at companies like Cloudflare, Stripe, and GitLab. The setup is markdown with frontmatter in Git, plus a static site generator.
- For small teams the suggested generators are VitePress or Starlight. MkDocs is another common choice.
- Architecture Decision Records (ADRs) are a standard companion, using a Context/Decision/Consequences template with statuses like proposed, accepted, deprecated, superseded. I found this in a single repo's docs rather than a survey, so treat it as a pattern, not a measured adoption figure.

**Verification** (one line, prints weekly npm downloads for turbo, nx, and pnpm; success is three lines of output, each with a number):

`for p in turbo nx pnpm; do curl -s https://api.npmjs.org/downloads/point/last-week/$p | jq -r '"\(.package) \(.downloads)"'; done`

Next question: is the monorepo's main language JavaScript/TypeScript, or is it polyglot?

Sources:
- [Stack Overflow 2025 Developer Survey](https://survey.stackoverflow.co/2025/)
- [Stack Overflow survey press summary](https://www.hpcwire.com/bigdatawire/this-just-in/stack-overflows-2025-developer-survey-reveals-trust-in-ai-at-an-all-time-low/)
- [Stack Overflow survey highlights](https://1000software.substack.com/p/highlights-from-the-stack-overflow)
- [Best Monorepo Tools 2026](https://devtoollab.com/blog/best-monorepo-management-tools)
- [How to Pick a Monorepo Tool in 2026](https://dev.to/yobox/how-to-pick-a-monorepo-tool-in-2026-kko)
- [qmd overview](https://knightli.com/en/2026/05/01/qmd-markdown-search-for-ai-agents/)
- [Docs-as-Code 2.0](https://www.drexplain.com/press/articles/docs_as_code_2_0_a_new_standard_for_ai_ready_user_documentation/)
- [Docs-as-Code in 2026](https://unmarkdown.com/blog/docs-as-code-2026)
- [Docs-as-code tools compared](https://clickhelp.com/clickhelp-technical-writing-blog/docs-as-code-tools/)
- [Jira vs Linear for product managers](https://resumegeni.com/blog/jira-vs-linear-for-product-managers)
- [Linear vs Jira vs Notion](https://dev.to/_6638a39c349d7e9c85ee20/linear-vs-jira-vs-notion-best-project-management-tool-for-developers-2026-1ma9)
- [Top 10 issue tracking tools](https://www.rajeshkumar.xyz/blog/?p=1463)
- [Jira alternatives comparison](https://inventivehq.com/blog/best-project-management-tools-jira-alternatives)
- [Documentation transformation summary (ADR example)](https://glama.ai/mcp/servers/@dylanmarriner/MCP-server/blob/d9961c1620825d604a398471304b8a5d32793ae0/ENTERPRISE_TRANSFORMATION_SUMMARY.md)
