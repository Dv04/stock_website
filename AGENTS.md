# Repository Guidelines

## Project Structure & Module Organization
Keep all application code inside `src/`, grouped by feature (e.g., `src/portfolio`, `src/market-data`). Shared UI and utilities belong in `src/components` and `src/lib`. Place static assets in `public/` and configuration files (linting, formatting, environment samples) at the repo root. End-to-end scripts or data import helpers should live under `scripts/`. When you add tests, mirror the production structure inside `tests/` so every feature directory has a matching test directory.

## Build, Test, and Development Commands
Run `npm install` once to set up dependencies. Use `npm run dev` for a hot-reloading development server and confirm UI changes before committing. Execute `npm run build` to produce the optimized production bundle; run it locally before tagging a release. Guard quality with `npm test`, which should execute unit and integration suites, and `npm run lint` to catch style or type issues early. Keep all scripts defined in `package.json` so they are discoverable by new contributors.

## Coding Style & Naming Conventions
Default to TypeScript with 2-space indentation and trailing commas where valid. Name React components in PascalCase (`MarketSummaryCard.tsx`) and hooks/utilities in camelCase (`useQuoteFeed.ts`). Co-locate styles (CSS modules or styled components) with their owning component. Keep filenames singular unless the file exports a collection. Ensure `eslint` and `prettier` configs in the repo root stay in sync; run both before opening a PR.

## Testing Guidelines
Write unit tests with Jest or Vitest and integration/UI coverage with Playwright or Testing Library. Follow the `*.test.ts` naming pattern inside `tests/` or `__tests__` directories so tooling can auto-discover suites. Target at least 80% line coverage for critical data services (pricing, orders) and add regression tests for bug fixes. Use `npm test -- --watch` during development and `npm test -- --coverage` before merging.

## Commit & Pull Request Guidelines
Use Conventional Commits (`feat: add quote ticker widget`) to keep history searchable and release automation simple. Each commit should be scoped to one logical change and pass tests locally. Pull requests need a concise summary, screenshots or GIFs for UI changes, links to tracking issues, and a checklist confirming lint/tests were run. Request review from at least one maintainer and address feedback with follow-up commits rather than force-pushing over history.

## Security & Configuration Tips
Never commit real API keys. Store secrets in `.env.local` (gitignored) and document required variables in `.env.example`. Review third-party dependencies quarterly; pin versions that touch authentication or payments. When handling market data websockets, validate payloads and guard against rate-limit breaches before merging.
