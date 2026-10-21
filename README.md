# Greth Offensive

Greth Offensive is a micro-modular, stigmergic offensive security orchestration framework inspired by the swarm-based design of Pentest Swarm AI, but built around LangGraph + LiteLLM and a Python-first execution model.

Core principles:
- shared blackboard state instead of brittle linear execution
- event-driven agents with explicit trigger predicates
- micro-modular subsystems for recon, offense, defense, verification, and reporting
- structured findings and pheromone-based prioritization
- operator-friendly TUI and scriptable automation

## Repository layout

- `greth/agents/` — specialist agents by function
- `greth/core/` — blackboard, scheduler, graph orchestration, config, models
- `greth/tools/` — external execution adapters and tool wrappers
- `greth/helpers/` — utility helpers and validation
- `greth/llm/` — LiteLLM and LangGraph integration
- `greth/tui/` — terminal UI / monitoring
- `greth/main.py` — entrypoint

## Quick start

```bash
uv sync
uv run greth --help
```

## Example

```bash
uv run greth --target https://example.com --mode recon
```

## Architecture

The framework uses a tiny swarm loop:

1. a target is registered on the blackboard
2. reconnaissance agents enrich the surface
3. triage filters, ranks, and deduplicates findings
4. offense agents build exploitation paths
5. verification agents confirm the signal
6. reporting agents summarize the campaign

This creates a stigmergic pattern where findings influence downstream actions through shared state instead of centralized sequential planning.
