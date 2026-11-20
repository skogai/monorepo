# nelson

nelson is a claude code skill for coordinating agent work using royal navy terminology. it provides an eight-step operational framework: sailing orders, the estimate, battle plan, form the squadron, get permission to sail, quarterdeck rhythm, action stations, and stand down.

## project structure

```
.claude-plugin/
  plugin.json             — plugin manifest
  marketplace.json        — marketplace definition (self-hosted)
settings.json             — plugin default settings (enables agent teams)
skills/nelson/
  skill.md                — main entrypoint (what claude reads)
  references/             — supporting docs loaded on demand
    action-stations.md      — risk tier definitions (station 0–3)
    admiralty-templates/     — one file per template, loaded on demand
      damage-report.md        — json template for hull integrity damage reports
      turnover-brief.md       — handover brief for relief on station
    commendations.md        — recognition signals & graduated correction
    crew-roles.md           — crew role definitions, ship names & sizing rules
    damage-control/         — one file per procedure, loaded on demand
      comms-failure.md        — agent team infrastructure failure recovery
      crew-overrun.md         — ship crew consuming disproportionate resources
      escalation.md           — issue exceeds current authority or needs clarification
      hull-integrity.md       — threshold definitions & squadron readiness board
      man-overboard.md        — stuck agent replacement procedure
      partial-rollback.md     — completed task found faulty, other tasks sound
      relief-on-station.md    — planned ship replacement for context exhaustion
      scuttle-and-reform.md   — mission cannot succeed, abort and reform
      session-hygiene.md      — clean start procedure for new sessions
      session-resumption.md   — resuming an interrupted session
    model-selection.md      — cost-optimized model assignment for agents
    royal-marines.md        — royal marines deployment rules & specialisations
    squadron-composition.md — mode selection & team sizing rules
    structured-data.md      — structured fleet data capture reference
    tool-mapping.md         — nelson-to-claude code tool reference
    standing-orders/        — one file per anti-pattern, loaded on demand
  scripts/                  — skill-specific scripts
    nelson-data.py            — structured data capture for nelson missions
    nelson_conflict_scan.py   — pre-flight conflict scan for battle plans
    test_nelson_conflict_scan.py — python tests for nelson_conflict_scan.py
    test_nelson_data.py       — python tests for nelson-data.py
agents/                   — agent interface definitions
demos/                    — example applications built with nelson
scripts/                  — maintenance & utility scripts
  check-references.sh       — cross-reference validation for documentation links
  count-tokens.py           — token counter for hull integrity damage reports
```
