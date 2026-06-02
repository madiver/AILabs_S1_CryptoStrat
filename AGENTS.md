# Agent Instructions

This file defines generic engineering guidance for coding agents working in this repository. It is intentionally reusable and avoids project-specific assumptions until the project direction, stack, and conventions are established.

## Engineering Standards

- Prefer production-ready, maintainable fixes over temporary or development-only shortcuts.
- Read and understand the existing code before changing it.
- Follow existing project patterns, frameworks, and conventions.
- Keep changes small, incremental, and reversible.
- Resolve root causes instead of masking defects with superficial workarounds.
- Add abstractions only when they reduce real complexity or match an established pattern.
- For projects using languages with dependency isolation, set up a virtual environment or equivalent isolation mechanism as part of initial project setup. Use the project's chosen tooling, such as `uv` for Python, `npm` or `pnpm` for Node.js, and `bundler` for Ruby.

## Repository Boundaries

- Preserve module, package, and repository boundaries.
- Keep app-specific logic out of shared libraries.
- Keep backend, frontend, infrastructure, and tooling concerns separated unless the project already uses a different pattern.
- Do not introduce cross-layer dependencies without a clear reason.

## Security And Privacy

- Do not hardcode secrets, tokens, credentials, API keys, or private URLs.
- Use the project-approved secrets and configuration mechanism.
- Do not log sensitive values.
- Diagnostics, exports, and debug tools should be allowlist-based and avoid sensitive data.
- Treat authentication, authorization, payment, identity, and data-retention changes as high-risk.

## Git Policy

- Do not run `git commit`, `git push`, `git merge`, `git rebase`, branch creation, or destructive git commands unless explicitly requested in the current task.
- Never revert user changes unless explicitly instructed.
- Check worktree status before broad edits.
- If unrelated changes exist, leave them alone.

## Testing And Validation

- Use the repository's existing test runner, package manager, virtual environment, or build tooling.
- Add or update tests for behavior changes.
- Run focused tests first, then broader tests when risk justifies it.
- If tests cannot be run, explain why and identify residual risk.
- Validate supported runtime or packaging behavior before calling work complete when relevant.

## Issue And PR Workflow

- When work is tied to issue tracking, reference the issue.
- Issue titles should describe the problem plainly.
- Issue bodies should include: Summary, Impact, Evidence, Proposed fix, and Acceptance criteria.
- PR descriptions should include root cause, solution summary, linked issues, and tests run.
- Use closing keywords like `Fixes #123` only when the PR fully resolves the issue.

## UI/UX Work

- Follow the existing design system and UI patterns.
- Keep layouts simple, deterministic, accessible, and testable.
- Reuse established components before creating new ones.
- Persist only normalized user settings or state.
- Avoid one-off UI wiring unless explicitly justified.
- Validate responsive behavior or supported desktop platforms when relevant.

## Documentation

- Prefer updating canonical documentation over scattering notes.
- Document commands, architecture decisions, and recurring pitfalls only when they help future work.
- Keep project-specific notes separate from generic rules.

## Project-Specific Notes

- Tech stack: TypeScript/Node.js and Python.
- Dependency management and virtual environment setup: Use `npm` for Node.js dependencies and `uv` for Python. Run `npm install` to restore Node dependencies and `uv sync` to create or update `.venv`.
- Common commands: `npm run typecheck`, `npm run check:node`, `uv run python --version`, `uv pip list`.
- Architecture boundaries: To be defined.
- Testing notes: To be defined.
- Deployment/packaging notes: To be defined.
- Known pitfalls: To be defined.
