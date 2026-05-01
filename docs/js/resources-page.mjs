import {
  parseKeywords,
  filterResources,
  sortResources,
  collectKeywordCounts,
} from "./resources-core.mjs";

const searchInput = document.getElementById("searchInput");
const sortSelect = document.getElementById("sortSelect");
const resetButton = document.getElementById("resetButton");
const pageFallback = document.getElementById("pageFallback");
const fallbackTitle = document.getElementById("fallbackTitle");
const fallbackDescription = document.getElementById("fallbackDescription");
const topicChips = document.getElementById("topicChips");
const keywordChips = document.getElementById("keywordChips");
const resultsSummary = document.getElementById("resultsSummary");
const resourceGrid = document.getElementById("resourceGrid");
const emptyState = document.getElementById("emptyState");

const DEFAULT_SORT = "title-asc";
const TOPIC_FILTERS = [
  { id: "context-engineering", label: "Context Engineering", terms: ["context engineering"] },
  { id: "prompt-engineering", label: "Prompt Engineering", terms: ["prompt engineering"] },
  {
    id: "ai-foundations",
    label: "AI Foundations",
    terms: ["machine learning", "foundation models", "deep learning", "statistics", "neural networks", "generative ai", "llms"],
  },
  {
    id: "ai-agents",
    label: "AI Agents",
    terms: ["ai agents", "agentic ai", "multi-agent", "agentic software development", "tool use", "react", "agent context", "langgraph"],
  },
  { id: "mcp", label: "MCP", terms: ["model context protocol", "mcp"] },
  {
    id: "retrieval-rag",
    label: "Retrieval and RAG",
    terms: ["retrieval", "rag", "cag", "chunking", "embeddings", "information retrieval"],
  },
  {
    id: "ai-for-software-development",
    label: "AI for Software Development",
    terms: ["ai-assisted development", "software development", "developer workflows", "coding assistants", "software engineering", "coding agents"],
  },
  { id: "youtube", label: "YouTube", terms: ["youtube.com", "youtube", "lectures", "courses"] },
];

const state = {
  resources: [],
  query: "",
  sortKey: DEFAULT_SORT,
  activeTopic: "",
  activeKeywords: new Set(),
  keywordLabels: new Map(),
  focusTopic: "",
  focusKeyword: "",
  error: "",
};

function createElement(tagName, className, textContent) {
  const element = document.createElement(tagName);

  if (className) {
    element.className = className;
  }

  if (textContent != null) {
    element.textContent = textContent;
  }

  return element;
}

function createKeywordLabelMap(resources) {
  const keywordLabels = new Map();

  for (const resource of resources) {
    for (const keyword of parseKeywords(resource?.Keywords)) {
      const normalizedKeyword = keyword.trim().toLowerCase();

      if (normalizedKeyword && !keywordLabels.has(normalizedKeyword)) {
        keywordLabels.set(normalizedKeyword, keyword.trim());
      }
    }
  }

  return keywordLabels;
}

function toTopicText(resource) {
  return [resource?.Title, resource?.Author, resource?.Description, resource?.Keywords, resource?.URL]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

function getTopicFilter(topicId) {
  return TOPIC_FILTERS.find((topic) => topic.id === topicId) ?? null;
}

function matchesTopic(resource, topicId) {
  const topic = getTopicFilter(topicId);

  if (!topic) {
    return true;
  }

  const text = toTopicText(resource);
  return topic.terms.some((term) => text.includes(term));
}

function setFallbackContent({ title, message, visible }) {
  fallbackTitle.textContent = title;
  fallbackDescription.replaceChildren();
  fallbackDescription.append(`${message} `);

  const fallbackLink = createElement("a", "", "resources.json");
  fallbackLink.href = "resources.json";
  fallbackDescription.append(fallbackLink, ".");

  pageFallback.hidden = !visible;
}

function getVisibleResources() {
  const topicResources = state.activeTopic
    ? state.resources.filter((resource) => matchesTopic(resource, state.activeTopic))
    : state.resources;

  const filteredResources = filterResources(topicResources, {
    query: state.query,
    activeKeywords: state.activeKeywords,
  });

  return sortResources(filteredResources, state.sortKey);
}

function renderTopicChips() {
  topicChips.replaceChildren();

  for (const topic of TOPIC_FILTERS) {
    const count = state.resources.filter((resource) => matchesTopic(resource, topic.id)).length;
    const chip = createElement("button", "topic-chip");
    const label = createElement("span", "", topic.label);
    const total = createElement("small", "", String(count));

    chip.type = "button";
    chip.dataset.topic = topic.id;
    chip.setAttribute("aria-pressed", state.activeTopic === topic.id ? "true" : "false");
    chip.classList.toggle("is-active", state.activeTopic === topic.id);
    chip.append(label, total);
    chip.addEventListener("click", () => {
      state.activeTopic = state.activeTopic === topic.id ? "" : topic.id;
      state.focusTopic = topic.id;
      render();
    });

    topicChips.append(chip);
  }

  if (state.focusTopic) {
    const focusedChip = topicChips.querySelector(`[data-topic="${CSS.escape(state.focusTopic)}"]`);

    if (focusedChip) {
      focusedChip.focus();
    }

    state.focusTopic = "";
  }
}

function renderKeywordChips() {
  keywordChips.replaceChildren();

  for (const [keyword, count] of collectKeywordCounts(state.resources)) {
    const chip = createElement("button", "keyword-chip");
    const label = createElement("span", "", state.keywordLabels.get(keyword) ?? keyword);
    const total = createElement("small", "", String(count));

    chip.type = "button";
    chip.dataset.keyword = keyword;
    chip.setAttribute("aria-pressed", state.activeKeywords.has(keyword) ? "true" : "false");
    chip.classList.toggle("is-active", state.activeKeywords.has(keyword));
    chip.append(label, total);
    chip.addEventListener("click", () => {
      if (state.activeKeywords.has(keyword)) {
        state.activeKeywords.delete(keyword);
      } else {
        state.activeKeywords.add(keyword);
      }

      state.focusKeyword = keyword;
      render();
    });

    keywordChips.append(chip);
  }

  if (state.focusKeyword) {
    const focusedChip = keywordChips.querySelector(`[data-keyword="${CSS.escape(state.focusKeyword)}"]`);

    if (focusedChip) {
      focusedChip.focus();
    }

    state.focusKeyword = "";
  }
}

function renderSummary(visibleResources) {
  if (state.error) {
    resultsSummary.textContent = state.error;
    return;
  }

  const activeTopic = getTopicFilter(state.activeTopic);
  const activeKeywords = Array.from(state.activeKeywords);
  const filters = [];

  if (activeTopic) {
    filters.push(`topic: ${activeTopic.label}`);
  }

  if (state.query) {
    filters.push(`search: "${state.query}"`);
  }

  if (activeKeywords.length) {
    filters.push(`keywords: ${activeKeywords.join(", ")}`);
  }

  const suffix = filters.length ? ` for ${filters.join(" | ")}` : "";
  const total = state.resources.length;
  const count = visibleResources.length;
  resultsSummary.textContent = `${count} of ${total} resources${suffix}`;
}

function renderCards(visibleResources) {
  resourceGrid.replaceChildren();

  for (const resource of visibleResources) {
    const card = createElement("article", "card resource-card");
    const header = document.createElement("header");
    const title = createElement("h2", "", resource?.Title ?? "Untitled resource");
    const resourceTitle = resource?.Title ?? "Untitled resource";
    const metaParts = [resource?.Author, resource?.Year].filter(Boolean);
    const meta = createElement("p", "resource-meta", metaParts.join(" · "));
    const description = createElement("p", "resource-description", resource?.Description ?? "");
    const keywordList = createElement("div", "resource-keywords");
    const link = createElement("a", "resource-link", "Open resource");

    link.href = resource?.URL ?? "#";
    link.target = "_blank";
    link.rel = "noreferrer";
    link.setAttribute("aria-label", `Open resource: ${resourceTitle}`);

    header.append(title);
    if (meta.textContent) {
      header.append(meta);
    }

    for (const keyword of parseKeywords(resource?.Keywords)) {
      keywordList.append(createElement("span", "badge", keyword));
    }

    card.append(header);
    if (description.textContent) {
      card.append(description);
    }
    if (keywordList.childNodes.length) {
      card.append(keywordList);
    }
    card.append(link);
    resourceGrid.append(card);
  }
}

function renderEmptyState(visibleResources) {
  const showEmpty = !state.error && visibleResources.length === 0;
  emptyState.hidden = !showEmpty || Boolean(state.error);
  resourceGrid.hidden = showEmpty || Boolean(state.error);

  if (state.error) {
    setFallbackContent({
      title: "Interactive catalog unavailable",
      message: "The catalog could not be loaded automatically. You can still browse the raw resource list in",
      visible: true,
    });
    return;
  }

  pageFallback.hidden = true;
  emptyState.querySelector("h2").textContent = "No matching resources";
  emptyState.querySelector("p").textContent = "Try a different search term or clear the active filters.";
}

function render() {
  const visibleResources = getVisibleResources();
  //renderTopicChips();
  renderKeywordChips();
  renderSummary(visibleResources);
  renderCards(visibleResources);
  renderEmptyState(visibleResources);
}

function resetFilters() {
  state.query = "";
  state.sortKey = DEFAULT_SORT;
  state.activeTopic = "";
  state.activeKeywords.clear();
  searchInput.value = "";
  sortSelect.value = DEFAULT_SORT;
  render();
}

async function loadResources() {
  try {
    const response = await fetch(new URL("../references.json", import.meta.url));

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const data = await response.json();
    state.resources = Array.isArray(data) ? data : [];
    state.keywordLabels = createKeywordLabelMap(state.resources);
    setFallbackContent({
      title: "Interactive catalog fallback",
      message: "If the interactive catalog does not load, you can still browse the raw resource list in",
      visible: false,
    });
    state.error = "";
  } catch {
    state.resources = [];
    state.keywordLabels = new Map();
    state.error = "Unable to load the interactive catalog.";
  }

  render();
}

searchInput.addEventListener("input", (event) => {
  state.query = event.target.value.trim();
  render();
});

sortSelect.addEventListener("change", (event) => {
  state.sortKey = event.target.value;
  render();
});

resetButton.addEventListener("click", resetFilters);

loadResources();
