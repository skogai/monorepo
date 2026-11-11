---
type: Reference
title: Open Knowledge capabilities
tags: [openknowledge, operations]
---

# Open Knowledge capabilities

This bundle targets upstream Open Knowledge 0.13.0 and OKF 0.2. Current upstream main has additional lifecycle commands (`check`, `review`, `publish`, `upgrade`) absent from this installed version. Use version-matched help before upgrading. Upstream: https://github.com/openknowledge-sh/openknowledge/tree/v0.13.0

## Local workflows

Run from the repository root. Prefix commands with `mise exec github:openknowledge-sh/openknowledge@0.13.0 --` to select the pinned release.

| Feature | Command |
| --- | --- |
| Validation | `openknowledge validate wiki` |
| Search with evidence | `openknowledge search wiki "fresh checkout"` |
| Exact reading | `openknowledge get wiki/index.md` |
| Structure | `openknowledge list wiki` |
| Local browser | `openknowledge view wiki` |
| Risk audit | `openknowledge audit wiki --baseline .openknowledge/audit-sources.json` |
| Retrieval regression | `openknowledge eval run .openknowledge/evals/knowledge.yaml wiki` |
| Typed claim validation | `openknowledge claims validate --path wiki` |
| Hybrid retrieval | `openknowledge query hybrid --text "mise setup" wiki` |
| Static viewer | `openknowledge export html --out wiki-site wiki` |
| Portable archive | `openknowledge export tar --out wiki-exports/wiki.tar.gz wiki` |
| JSON | `openknowledge export json --out wiki-exports/wiki.json wiki` |
| Relationship graph | `openknowledge export graph --out wiki-exports/graph.json wiki` |
| RDF | `openknowledge export rdf --out wiki-exports/wiki.nq wiki` |
| Parsed syntax | `openknowledge ast wiki` |
| Read-only MCP | `openknowledge mcp wiki` |

Create `wiki-exports` before exporting. Generated exports are ignored. Viewer output is enabled for local builds; no hosting or public deployment is configured. Review all bundled content before sharing an archive or site.

For an MCP client, use command `mise`, arguments `exec`, `github:openknowledge-sh/openknowledge@0.13.0`, `--`, `openknowledge`, `mcp`, and the absolute path to this checkout's `wiki`. Set its working directory to the checkout. No client configuration is installed automatically.

## Governance and advanced features

The GitHub workflow validates the bundle and runs repository-specific retrieval cases on pull requests and master pushes. Its upstream action is pinned to the v0.13.0 commit. Local checks do not prove the hosted workflow has passed.

Pages carry source provenance. Typed claims are optional: use `claims suggest`, review proposals, then `claims apply`. Do not mark claims verified without authoritative evidence or actual human approval. `evidence pin` can capture source bytes and bind their digest to a document's source ID. Use only reviewed source files; pinned artifacts may contain their full content.

SPARQL and Datalog require meaningful typed semantic facts; the current narrative wiki does not invent a graph of verified assertions. `quality report` and `audit --usage` become informative after real usage exists. Registry/connect/disconnect manage external knowledge sources and modify local connection state; no external sources are registered here.

Agent jobs, observation, model-backed review, runtime hosting, deployment and scheduled maintenance require runtime/provider configuration and operating choices. They are available through `agent`, `automation`, and setup profiles, but are not running services in this PR. The generated daily maintenance job was removed because no model provider or maintenance service is configured. The user can explore each command's `--help` without activating it.

[Maintenance workflow](workflow.md) · [Home](index.md)
