import { INSTALL_TARGETS, filterSkills, githubUrl, manualInstallCommand } from "./skills-core.mjs";

const searchInput = document.getElementById("searchInput");
const resultsSummary = document.getElementById("resultsSummary");
const skillGrid = document.getElementById("skillGrid");
const emptyState = document.getElementById("emptyState");
const pageFallback = document.getElementById("pageFallback");

let skills = [];

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) {
    node.className = className;
  }
  if (text !== undefined) {
    node.textContent = text;
  }
  return node;
}

async function copyText(text, button) {
  try {
    await navigator.clipboard.writeText(text);
    button.textContent = "Copied";
  } catch {
    button.textContent = "Copy failed";
  }
  setTimeout(() => {
    button.textContent = "Copy";
  }, 1500);
}

function commandRow(label, command) {
  const row = element("div", "skill-command");
  const code = element("code", "", command);
  const button = element("button", "reset-button copy-button", "Copy");
  button.type = "button";
  button.addEventListener("click", () => copyText(command, button));
  row.append(code, button);
  const wrapper = element("div", "skill-install-row");
  wrapper.append(element("span", "skill-install-label", label), row);
  return wrapper;
}

function renderCard(skill) {
  const card = element("article", "card-tool card-padding skill-card");

  const header = element("div", "d-flex justify-content-between align-items-center mb-2");
  header.append(element("h2", "h5 mb-0 skill-name", skill.name));
  if (skill.chapter) {
    header.append(element("span", "badge", `Chapter ${skill.chapter}`));
  }
  card.append(header);

  if (skill.chapterTitle) {
    card.append(element("p", "resource-meta", skill.chapterTitle));
  }
  card.append(element("p", "resource-description", skill.description));

  const facts = element("dl", "skill-facts");
  for (const [term, value] of [["Reviews", skill.input], ["Returns", skill.output]]) {
    if (value) {
      facts.append(element("dt", "", term), element("dd", "", value));
    }
  }
  card.append(facts);

  const details = element("details", "skill-install");
  details.append(element("summary", "", "Install this skill only"));
  details.append(commandRow("Clone", "git clone https://github.com/bonigarcia/context-engineering.git"));
  for (const [target, entry] of Object.entries(INSTALL_TARGETS)) {
    details.append(commandRow(entry.label, manualInstallCommand(skill, target)));
  }
  card.append(details);

  const link = element("a", "btn btn-primary w-100", "View on GitHub");
  link.href = githubUrl(skill);
  card.append(link);
  return card;
}

function render() {
  const visible = filterSkills(skills, searchInput.value);
  skillGrid.replaceChildren(...visible.map(renderCard));
  emptyState.hidden = visible.length > 0;
  resultsSummary.textContent =
    visible.length === skills.length ? `${skills.length} skills` : `${visible.length} of ${skills.length} skills`;
}

async function init() {
  document.querySelectorAll("[data-copy-target]").forEach((button) => {
    const target = document.getElementById(button.dataset.copyTarget);
    button.addEventListener("click", () => copyText(target.textContent, button));
  });
  try {
    const response = await fetch("skills.json");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    skills = await response.json();
  } catch (error) {
    pageFallback.hidden = false;
    resultsSummary.textContent = "The skill catalog could not be loaded.";
    console.error(error);
    return;
  }
  searchInput.addEventListener("input", render);
  render();
}

init();
