# AI in the Lab - Episode 1: Crypto Trading Dashboard

> A real-time crypto trading dashboard built end-to-end with AI as a thinking partner. Built live in 90 minutes on June 2, 2026.

This repository is the working artifact from Episode 1 of AI in the Lab, a live show about how to use AI as an active engineering partner inside a workflow that can build complex software end-to-end.

The point of the project isn't crypto. It's the workflow.

The dashboard streams real-time market data from Coinbase via WebSocket, renders candlestick charts for BTC-USD, ETH-USD, and SOL-USD, and is built using a methodology that treats AI as a thinking partner rather than an autocomplete. The 90-minute broadcast covers a 10-turn concept conversation that produces a project roadmap, spec-kit's structured workflow (constitution -> spec -> plan -> tasks -> implement), and roughly 82 autonomous implementation tasks executed by the AI agent while bounded by captured documents.

Every decision is captured as a markdown artifact in this repo. Six months from now, someone trying to understand why the code is shaped this way can trace every choice back to the conversation that produced it. That auditability is what separates this approach from prompt-and-pray.

This README, the project structure, and the running code are built up live during the broadcast.

## Phase 1 run instructions

Install dependencies:

```bash
npm install
uv sync
```

Run the backend:

```bash
uv run uvicorn main:app --app-dir backend/src --reload --host 127.0.0.1 --port 8000
```

Run the frontend in another terminal:

```bash
npm run dev
```

Open the Vite URL, typically http://127.0.0.1:5173.

Validate the build:

```bash
uv run pytest backend/tests
npm run typecheck
npm run test
npm run test:e2e
```

## About the show

AI in the Lab is part of Frontier Tech, a regular series on AI-orchestrated software engineering. AI in the Lab features live solo builds. Frontier Tech features conversation episodes with co-host Tim Romanowski. Schedule and upcoming episodes at https://adviceforge.com/frontier-tech

## Disclaimers

**Educational only. Not investment advice.** This is a Phase 1 build, market-data-only. There is no authentication, no persistence, and no live trading. Do not use this code as the basis for any real trading decision.

The tools used in this build are Codex and spec-kit, but the methodology works with Claude Code, Cursor, and other frontier coding agents.

## License

MIT
