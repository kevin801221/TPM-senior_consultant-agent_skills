# Local Thinking Workbench Implementation Plan

**Goal:** Turn the existing method library into a personal, local web application using the owner's Codex or Claude Code subscription.
**Architecture:** React and assistant-ui provide a guided brief and conversation. A loopback-only Node service validates task boundaries, loads exactly one technique, invokes an installed CLI, and normalizes JSONL responses. The browser stores brief/history locally; credentials remain with the CLI.
**Tech Stack:** React, assistant-ui LocalRuntime, Vite, Node HTTP and child_process, node:test.

## Decision

Local personal use selected by the user. Use assistant-ui for the custom CLI backend. CopilotKit remains an alternative for future shared agent/UI state; a fully custom chat duplicates state/cancellation logic.
Initial tasks: [#44](../../references/techniques/044-problem-slicing.md) problem framing, [#31](../../references/techniques/031-executive-critique.md) proposal critique, [#37](../../references/techniques/037-validation-test.md) validation. Required brief: decision, evidence, constraints. Produce a decision-oriented document; follow-ups remain in that task. No external tools or implementation workflow in this version.

## Tasks

1. Write failing contracts in app/tests/core.test.mjs: reject missing brief/unsupported task/provider; load only selected method; normalize both CLI streams and errors; remove API credential overrides.
2. Implement app/server/core.mjs and verify node --test app/tests/core.test.mjs.
3. Implement app/server/index.mjs: localhost host/origin/token validation, bounded requests, one active run, cancel/disconnect/timeouts, auth status, static frontend.
4. Implement app/src/App.jsx and app/src/style.css: three task choices, bounded input, provider status, assistant-ui conversation, local history, Markdown download and visible error/cancellation.
5. Run npm run check, existing Python integrity tests, browser QA and a real Codex request. Claude live verification requires renewing its expired login.
6. Document npm install / npm run build / npm start and limitations in app/README.md. Keep existing 56 method files unchanged.

## Verification

Use core contract tests plus HTTP tests for malicious origin, invalid brief, process errors, cancellation and concurrency. Run a real CLI through the HTTP path separately; never present fixture output as live output. Browser QA covers form validation, starting a task, responsive layout and error presentation.
