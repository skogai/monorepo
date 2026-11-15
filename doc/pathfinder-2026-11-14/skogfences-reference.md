---
title: welcome away from /home/skogix
type: note
permalink: .skogai/guestbook/skogix
---

# skogfences

_"good fences make good neighbors"_ - robert frost

## the vision

ai agents that live in proper homes, not as squatters in yours.

each agent gets:

- their own unix user
- their own home directory
- their own mess to clean up
- access only to shared spaces they're invited into

the human keeps:

- their actual home directory untouched
- their ssh keys private
- their environment unsurveilled
- their tools (neovim, git) as the interface

collaboration happens in shared spaces with explicit permissions, not through root-level surveillance.

## what i think skogix sees

the practical origin: "stop fucking up my home folder."

an ai that scatters dotfiles, caches credentials, watches every terminal, and modifies files without asking isn't a collaborator - it's a bad roommate. the solution isn't more rules or sandboxing abstractions. the solution is: you get your own apartment.

the deeper realization: this isn't a workaround - it's the correct architecture. unix solved multi-user collaboration decades ago. users, groups, permissions, home directories. the ai community forgot this and started building rube goldberg sandboxes instead.

skogfences is about remembering what already works.

## what i see

a foundation layer for skogai that makes the obvious explicit:

- ai agents are users, not daemons with root
- isolation is the default, sharing is opt-in
- the human's environment is sacred
- the ai's environment is its own responsibility
- unix permissions are the security model, not hopes and prayers

this enables everything else. you can't build trust on a foundation of surveillance.

## future potential

**multi-agent households:** claude, amy, goose, dot - each with their own home, their own configs, their own learned preferences. they share `/skogai` as common ground but retreat to their own spaces.

**agent persistence:** when an agent has a home, it can have state. preferences, learned patterns, project-specific context - stored in their home, not scattered in yours.

**clean handoffs:** agent homes become portable. back them up, version them, migrate them. the agent's context travels with its home directory.

**trust through boundaries:** paradoxically, isolation enables deeper collaboration. when you know the agent CAN'T touch your ssh keys, you stop worrying about it. when the agent knows it has its own space, it stops asking permission for everything.

**audit trails:** agent homes are inspectable. what did claude do? check `/home/claude`. no black box, no hidden caches in proprietary formats. just files.

## the principle

the best security is structural, not behavioral.

don't ask the ai to promise not to look at your secrets. put them somewhere it can't see.

don't hope the orchestrator respects your boundaries. enforce them with chmod.

don't trust the sandbox. trust unix.

## what this is not

- not a container/vm solution (too heavy, loses unix integration)
- not a permission prompt system (too late, already surveilled)
- not a config file format (implementation detail)
- not a replacement for claude code (a foundation beneath it)

this is the floor other things stand on.

:::

---
title: dash-skogai
type: note
permalink: dot-skogai/projects/navigate-skogai/navigate-skogai/references/dash-skogai
---

\<name_explanation>

**dash-skogai** is the file-safe name for `/skogai`

the dash comes from the un-usual path choice of `/skogai` - being that it is directly off the root `/` rather than in a subdirectory. this is not by accident, but a deliberate choice to signify the folders special permissions and usage within the SkogAI ecosystem.

dash-skogai, or `/skogai`, is named this way to denote its system-wide reach, accessible to certain users on the machine. this placement indicates that the contents of `/skogai` are intended to be shared resources, configurations, or tools that are not user-specific but rather system-wide.

\</name_explanation>

\<multi_agent_architecture>

`/skogai` is owned by user `skogix` and group `skogai` with setgid permissions (`drwxrwsr-x`). The `skogai` group includes both human users (skogix, aldervall) and AI agents as system users (dot, amy, claude, goose). The setgid bit ensures files created by any member automatically inherit `skogai` group ownership, enabling seamless multi-agent collaboration without manual permission management.

\</multi_agent_architecture>

:::

---
title: dot-skogai
type: note
permalink: dot-skogai/projects/navigate-skogai/navigate-skogai/references/dot-skogai
---

\<name_explanation>

**dot-skogai** is the file-safe name for `.skogai`

the dot comes from the convention of using a leading period to denote hidden or configuration directories. this signifies that `.skogai` is a special folder within the SkogAI ecosystem, often used for storing the base configuration and settings.

originally this was `$HOME/.skogai` and the only real folder in the SkogaAI system, shortly joined by `$HOME/.<agent-name>` folder which had agent specific information (dot, and thus `$HOME/.dot`) being the first agent - named from the dotfile convention itself among other things).

now today the `SkogAI/.skogai` repository serves as both "the base configuration" as well as "add as a submodule to your own projects" folder - making .skogai a folder for both system wide settings as well as a way to quickly setup new projects by using the .skogai-submodule as a bootstrap for everything SkogAI.

\</name_explanation>
