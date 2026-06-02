<!--
Sync Impact Report
Version change: template -> 1.0.0
Modified principles:
- Placeholder Principle 1 -> I. Auditability Is A Product Requirement
- Placeholder Principle 2 -> II. Backend Authority For Trading Decisions
- Placeholder Principle 3 -> III. Execution Starts Disabled And Proves Itself
- Placeholder Principle 4 -> IV. Realtime Data Must Be Explicitly Validated
- Placeholder Principle 5 -> V. Clear Boundaries Over Clever Coupling
Added sections:
- Architecture And Technology Constraints
- Development Workflow And Quality Gates
Removed sections:
- None; placeholder sections were replaced with concrete project sections.
Templates requiring updates:
- ✅ updated: .specify/templates/plan-template.md
- ✅ updated: .specify/templates/spec-template.md
- ✅ updated: .specify/templates/tasks-template.md
- ⚠ not applicable: .specify/templates/commands/*.md does not exist in this install
Runtime guidance reviewed:
- ✅ reviewed: README.md
- ✅ reviewed: docs/ROADMAP.md
- ✅ updated: AGENTS.md
Follow-up TODOs:
- None
-->
# AI in the Lab - Episode 1: Crypto Trading Dashboard Constitution

## Core Principles

### I. Auditability Is A Product Requirement

Every material product, architecture, strategy, risk, and implementation decision MUST
be captured in a durable repository artifact. Strategy decisions, risk decisions,
orders, fills, rejected actions, connection events, and execution errors MUST be
represented as structured events that can be reviewed after the fact. The rationale is
that this project demonstrates an AI-assisted engineering workflow where future readers
must be able to trace system behavior back to the documents and conversations that
produced it.

### II. Backend Authority For Trading Decisions

The Python backend MUST be the only layer that evaluates strategy logic, signs Coinbase
requests, enforces risk limits, submits orders, cancels orders, and reconciles balances,
orders, and fills. The TypeScript frontend MAY display state and request user intent,
but it MUST NOT hold exchange credentials or bypass backend risk gates. This prevents UI
state, browser compromise, or client-side bugs from becoming direct trading authority.

### III. Execution Starts Disabled And Proves Itself

Live trading MUST be disabled by default. New execution-related work MUST progress
through market-data-only behavior, then paper execution, then live execution only after
explicit configuration, visible UI mode display, risk controls, and an emergency stop
exist. Any feature that can affect real orders or account balances MUST document the
operator action required to enable it. The rationale is that this is educational
software and not investment advice or a ready-to-run trading product.

### IV. Realtime Data Must Be Explicitly Validated

Market data ingestion, candle construction, chart updates, strategy inputs, and
execution reconciliation MUST define their data source, timestamp convention, ordering
assumption, reconnect behavior, and stale-data behavior. Features computed from market
data MUST be causal: data from bar or event t MAY only influence decisions at t or later
when that data would be observable in production. The rationale is that trading software
fails quietly when data alignment, latency, or feed recovery is treated as incidental.

### V. Clear Boundaries Over Clever Coupling

Market data, candle aggregation, strategy evaluation, risk gating, execution, persistence,
and UI rendering MUST remain separable modules with explicit contracts. Shared schemas
SHOULD be used for events exchanged between backend and frontend. The TradingView
Lightweight Charts integration MUST be isolated behind frontend chart components rather
than spread through application state. This keeps the project understandable during the
live build and reduces later risk when paper execution becomes live execution.

## Architecture And Technology Constraints

- The frontend stack is TypeScript on Node.js and MUST use TradingView Lightweight
  Charts for candlestick rendering.
- The backend stack is Python and MUST use dependency isolation through `uv`.
- Coinbase integration MUST target Coinbase Advanced Trade API surfaces for market data,
  account data, and order management.
- Coinbase API keys, secrets, JWT material, and private account data MUST NOT be stored
  in source control, frontend code, browser storage, logs, screenshots, or generated
  artifacts.
- Initial product symbols are `BTC-USD`, `ETH-USD`, and `SOL-USD` unless a later spec
  explicitly changes scope.
- Initial chart intervals are `1m`, `5m`, `15m`, and `1h` unless a later spec explicitly
  changes scope.
- The system MUST expose mode clearly as market-data-only, paper trading, or live
  trading whenever execution state is visible.

## Development Workflow And Quality Gates

- Every feature spec MUST include user-testable scenarios, safety constraints, and
  auditability requirements when the feature touches market data, strategy, risk,
  execution, persistence, credentials, or user-facing trading state.
- Every implementation plan MUST pass a Constitution Check before design work starts and
  again after design artifacts are produced.
- Tasks MUST include explicit validation work for market-data parsing, candle
  construction, risk gates, execution state transitions, and frontend chart behavior
  whenever those areas are in scope.
- Tests MAY be deferred only for static documentation changes. Any deferred validation
  MUST be called out in the plan and final report with residual risk.
- Before any live execution path is implemented, the project MUST have a documented paper
  execution path, configured risk limits, an emergency stop, and reconciliation tests.
- Changes that touch authentication, authorization, Coinbase credentials, order
  submission, cancellation, account balances, persistence, or risk limits are high-risk
  and MUST receive focused validation before they are considered complete.

## Governance

This constitution supersedes conflicting project guidance. Amendments MUST be made by
editing this file, updating the Sync Impact Report, and validating dependent Spec Kit
templates and runtime guidance files. Amendments require a documented rationale in the
commit or accompanying project artifact.

Versioning follows semantic versioning:

- MAJOR versions remove or redefine existing governance principles in a way that changes
  prior compliance expectations.
- MINOR versions add new principles, sections, or materially expanded governance.
- PATCH versions clarify wording, fix errors, or make non-semantic refinements.

Compliance review is required during `/speckit-plan`, `/speckit-tasks`, and
`/speckit-implement` workflows. Constitution conflicts are blocking issues unless the
constitution is explicitly amended first.

**Version**: 1.0.0 | **Ratified**: 2026-06-02 | **Last Amended**: 2026-06-02
