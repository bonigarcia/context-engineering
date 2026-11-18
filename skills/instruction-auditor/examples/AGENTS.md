# AGENTS.md

Guidance for coding agents working on the Acme storefront, a Node.js web application. Run every command from the repository root.

## Build commands

- Install dependencies: `npm ci`
- Run the development server: `npm run dev` (serves on http://localhost:3000)
- Run the unit tests: `npm test`
- Run the end-to-end tests: start the development server with `npm run dev` in another terminal, then run `npm run test:e2e`

## Project layout

- `src/server/`: Express routes and middleware
- `src/client/`: React components
- `src/shared/`: types and helpers used by both sides
- `tests/unit/` and `tests/e2e/`: test suites, mirroring the `src/` structure

## Code style

- Indent with tabs.
- Use single quotes for strings in JavaScript and TypeScript.
- Write clean, high-quality code.
- Prefer named exports over default exports.

## Formatting

- Use 2-space indentation in every source file.
- Keep lines under 100 characters.

## Working rules

- Never make mistakes.
- Do not commit directly to `main`. Open a pull request.
- Add or update unit tests for every change in `src/`.

## Releasing a new version

1. Make sure you are on the `main` branch.
2. Pull the latest changes with `git pull`.
3. Run `npm ci`.
4. Run `npm test` and stop if any test fails.
5. Start the development server with `npm run dev`, run `npm run test:e2e`, and stop if any test fails.
6. Open `CHANGELOG.md`.
7. Move the entries under "Unreleased" to a new section named after the version.
8. Add today's date to the new section.
9. Update the `version` field in `package.json`.
10. Run `npm install` to update `package-lock.json`.
11. Commit with the message `chore: release vX.Y.Z`.
12. Create a tag named `vX.Y.Z`.
13. Push the commit and the tag.
14. Open the releases page on GitHub and create a release from the tag.
15. Paste the new changelog section into the release notes.
