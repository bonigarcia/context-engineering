import test from "node:test";
import assert from "node:assert/strict";

import { filterSkills, githubUrl, manualInstallCommand } from "../js/skills-core.mjs";

const SKILLS = [
  {
    name: "tool-reviewer",
    description: "Reviews tool definitions.",
    chapter: "4",
    chapterTitle: "Tools in AI agents",
    input: "Function-calling tool schemas or an MCP server",
    output: "Findings on tool names",
    path: "skills/tool-reviewer",
  },
  {
    name: "eval-builder",
    description: "Builds evaluation sets.",
    chapter: "8",
    chapterTitle: "Evaluation and observability",
    input: "A description of an agent",
    output: "Evaluation cases",
    path: "skills/eval-builder",
  },
];

test("filterSkills matches the input field case-insensitively", () => {
  assert.deepEqual(filterSkills(SKILLS, "mcp").map((s) => s.name), ["tool-reviewer"]);
});

test("filterSkills matches the chapter title", () => {
  assert.deepEqual(filterSkills(SKILLS, "observability").map((s) => s.name), ["eval-builder"]);
});

test("filterSkills with an empty query returns all skills", () => {
  assert.equal(filterSkills(SKILLS, "  ").length, 2);
});

test("githubUrl points to the skill folder on the main branch", () => {
  assert.equal(
    githubUrl(SKILLS[0]),
    "https://github.com/bonigarcia/context-engineering/tree/main/skills/tool-reviewer",
  );
});

test("manualInstallCommand copies the skill into the target folder", () => {
  assert.equal(
    manualInstallCommand(SKILLS[0], "claude"),
    "mkdir -p .claude/skills && cp -r context-engineering/skills/tool-reviewer .claude/skills/",
  );
  assert.equal(
    manualInstallCommand(SKILLS[0], "agents"),
    "mkdir -p .agents/skills && cp -r context-engineering/skills/tool-reviewer .agents/skills/",
  );
  assert.equal(
    manualInstallCommand(SKILLS[0], "cursor"),
    "mkdir -p .cursor/skills && cp -r context-engineering/skills/tool-reviewer .cursor/skills/",
  );
});

test("manualInstallCommand rejects an unknown target", () => {
  assert.throws(() => manualInstallCommand(SKILLS[0], "vim"), /unknown target/);
});
