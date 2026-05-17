const MANIFEST_URL = "ai-ecosystem/manifest.json";

const searchInput = document.getElementById("searchInput");
const resultsSummary = document.getElementById("resultsSummary");
const sectionNav = document.getElementById("sectionNav");
const sectionGrid = document.getElementById("sectionGrid");
const emptyState = document.getElementById("emptyState");

const state = {
  query: "",
  sections: [],
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

function normalizeText(value) {
  return String(value ?? "").toLowerCase();
}

function itemSearchText(item) {
  const metaValues = Object.entries(item ?? {})
    .filter(([key]) => !["name", "url", "description", "features"].includes(key))
    .flatMap(([, value]) => (Array.isArray(value) ? value : [value]));

  return [
    item?.name,
    item?.url,
    item?.description,
    ...(Array.isArray(item?.features) ? item.features : [item?.features]),
    ...metaValues,
  ]
    .filter(Boolean)
    .map(normalizeText)
    .join(" ");
}

function formatLabel(key) {
  return key
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replace(/[_-]/g, " ")
    .replace(/\b\w/g, (match) => match.toUpperCase())
    .replace(/\bUrl\b/g, "URL")
    .replace(/\bMcp\b/g, "MCP")
    .replace(/\bRag\b/g, "RAG")
    .replace(/\bSdk\b/g, "SDK")
    .replace(/\bSdd\b/g, "SDD");
}

function renderMeta(item) {
  const metaEntries = Object.entries(item ?? {})
    .filter(([key, value]) => !["name", "url", "description", "features"].includes(key) && value != null && value !== "");

  if (!metaEntries.length) {
    return null;
  }

  const meta = createElement("div", "ecosystem-meta");

  for (const [key, value] of metaEntries) {
    const row = createElement("div", "ecosystem-meta-row");
    const label = createElement("span", "ecosystem-meta-label", formatLabel(key));
    const body = createElement("span", "ecosystem-meta-value", Array.isArray(value) ? value.join(", ") : String(value));

    row.append(label, body);
    meta.append(row);
  }

  return meta;
}

function renderFeatures(features) {
  if (!Array.isArray(features) || !features.length) {
    return null;
  }

  const list = createElement("ul", "ecosystem-feature-list");

  for (const feature of features) {
    list.append(createElement("li", "", String(feature)));
  }

  return list;
}

function renderItem(item) {
  const card = createElement("article", "ecosystem-card");
  const title = createElement("h4");
  const link = createElement("a", "ecosystem-card-link", item.name ?? "Untitled item");

  if (item.url) {
    link.href = item.url;
    link.target = "_blank";
    link.rel = "noreferrer";
  }

  title.append(link);
  card.append(title);

  if (item.description) {
    card.append(createElement("p", "ecosystem-description", String(item.description)));
  }

  const features = renderFeatures(item.features);
  if (features) {
    card.append(features);
  }

  const meta = renderMeta(item);
  if (meta) {
    card.append(meta);
  }

  return card;
}

function renderGroup(group) {
  const groupWrap = createElement("section", "ecosystem-group");
  groupWrap.append(createElement("h3", "ecosystem-group-title", group.title));

  const grid = createElement("div", "ecosystem-grid");
  for (const item of group.items ?? []) {
    grid.append(renderItem(item));
  }

  groupWrap.append(grid);
  return groupWrap;
}

function renderSection(section) {
  const sectionEl = createElement("section", "ecosystem-section card");
  sectionEl.id = `section-${section.id}`;

  const header = createElement("div", "ecosystem-section-header");
  const titleWrap = createElement("div");
  titleWrap.append(createElement("h2", "", section.title));

  if (section.intro) {
    titleWrap.append(createElement("p", "ecosystem-section-intro", section.intro));
  }

  header.append(titleWrap, createElement("span", "badge", `${section.visibleCount} items`));
  sectionEl.append(header);

  for (const group of section.groups ?? []) {
    sectionEl.append(renderGroup(group));
  }

  return sectionEl;
}

function renderNav(sections) {
  sectionNav.replaceChildren();

  for (const section of sections) {
    const chip = createElement("button", "section-chip", section.title);
    chip.type = "button";
    chip.addEventListener("click", () => {
      document.getElementById(`section-${section.id}`)?.scrollIntoView({ behavior: "smooth", block: "start" });
    });

    sectionNav.append(chip);
  }
}

function filterSection(section, query) {
  const groups = [];
  let visibleCount = 0;

  for (const group of section.groups ?? []) {
    const items = (group.items ?? []).filter((item) => !query || itemSearchText(item).includes(query));

    if (!items.length) {
      continue;
    }

    visibleCount += items.length;
    groups.push({ ...group, items });
  }

  if (!groups.length) {
    return null;
  }

  return { ...section, groups, visibleCount };
}

function render() {
  const query = normalizeText(state.query).trim();
  const sections = state.sections
    .map((section) => filterSection(section, query))
    .filter(Boolean);

  sectionGrid.replaceChildren();
  renderNav(state.sections);

  if (!sections.length) {
    resultsSummary.textContent = "No matching items";
    emptyState.hidden = false;
    return;
  }

  emptyState.hidden = true;
  const totalItems = state.sections.reduce((count, section) => count + (section.groups ?? []).reduce((groupCount, group) => groupCount + (group.items ?? []).length, 0), 0);
  const visibleItems = sections.reduce((count, section) => count + section.visibleCount, 0);
  resultsSummary.textContent = `${visibleItems} of ${totalItems} items across ${sections.length} sections`;

  for (const section of sections) {
    sectionGrid.append(renderSection(section));
  }
}

async function loadData() {
  const manifest = await fetch(MANIFEST_URL).then((response) => {
    if (!response.ok) {
      throw new Error(`Unable to load ${MANIFEST_URL}`);
    }

    return response.json();
  });

  state.sections = await Promise.all(
    manifest.map(async (entry) => {
      const section = await fetch(`ai-ecosystem/${entry.file}`).then((response) => {
        if (!response.ok) {
          throw new Error(`Unable to load ai-ecosystem/${entry.file}`);
        }

        return response.json();
      });

      return {
        id: entry.id,
        title: section.title ?? entry.label,
        intro: section.intro ?? "",
        groups: section.groups ?? [],
      };
    })
  );

  render();
}

searchInput.addEventListener("input", () => {
  state.query = searchInput.value;
  render();
});

loadData().catch((error) => {
  resultsSummary.textContent = "Unable to load AI ecosystem data.";
  emptyState.hidden = false;
  emptyState.querySelector("p").textContent = error.message;
});
