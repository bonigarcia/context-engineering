const REPO_URL = "https://github.com/bonigarcia/context-engineering";

export const INSTALL_TARGETS = {
  claude: { label: "Claude Code", folder: ".claude/skills" },
  agents: { label: "Codex and Agent Skills compatible agents", folder: ".agents/skills" },
  cursor: { label: "Cursor", folder: ".cursor/skills" },
};

function searchText(skill) {
  return [skill?.name, skill?.description, skill?.chapterTitle, skill?.input, skill?.output]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

export function filterSkills(skills, query) {
  const normalized = String(query ?? "").trim().toLowerCase();
  const list = Array.from(skills ?? []);
  if (!normalized) {
    return list;
  }
  return list.filter((skill) => searchText(skill).includes(normalized));
}

export function githubUrl(skill) {
  return `${REPO_URL}/tree/main/${skill.path}`;
}

export function manualInstallCommand(skill, target) {
  const entry = INSTALL_TARGETS[target];
  if (!entry) {
    throw new Error(`unknown target: ${target}`);
  }
  return `mkdir -p ${entry.folder} && cp -r context-engineering/${skill.path} ${entry.folder}/`;
}
