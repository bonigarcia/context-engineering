function toSearchText(resource) {
  return [
    resource?.Title,
    resource?.Author,
    resource?.Description,
    resource?.Keywords,
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

function normalizeKeyword(value) {
  return String(value ?? "").trim().toLowerCase();
}

function getNormalizedKeywords(resource) {
  return Array.from(new Set(parseKeywords(resource?.Keywords).map(normalizeKeyword).filter(Boolean)));
}

function parseYear(value) {
  if (value == null) {
    return null;
  }

  if (typeof value === "string" && !value.trim()) {
    return null;
  }

  const year = Number(value);
  return Number.isFinite(year) ? year : null;
}

function compareTitles(left, right) {
  return String(left?.Title ?? "").localeCompare(String(right?.Title ?? ""), undefined, {
    sensitivity: "base",
  });
}

export function parseKeywords(value) {
  return String(value ?? "")
    .split(",")
    .map((keyword) => keyword.trim())
    .filter(Boolean);
}

export function filterResources(resources, { query, activeKeywords } = {}) {
  const normalizedQuery = String(query ?? "").trim().toLowerCase();
  const normalizedActiveKeywords = Array.from(activeKeywords ?? [], normalizeKeyword).filter(Boolean);

  return Array.from(resources ?? []).filter((resource) => {
    if (normalizedQuery && !toSearchText(resource).includes(normalizedQuery)) {
      return false;
    }

    if (!normalizedActiveKeywords.length) {
      return true;
    }

    const resourceKeywords = new Set(getNormalizedKeywords(resource));

    return normalizedActiveKeywords.every((keyword) => resourceKeywords.has(keyword));
  });
}

export function sortResources(resources, sortKey) {
  return Array.from(resources ?? []).sort((left, right) => {
    const leftYear = parseYear(left?.Year);
    const rightYear = parseYear(right?.Year);

    if (sortKey === "year-desc") {
      if (leftYear === null && rightYear === null) {
        return compareTitles(left, right);
      }

      if (leftYear === null) {
        return 1;
      }

      if (rightYear === null) {
        return -1;
      }

      return rightYear - leftYear || compareTitles(left, right);
    }

    if (sortKey === "year-asc") {
      if (leftYear === null && rightYear === null) {
        return compareTitles(left, right);
      }

      if (leftYear === null) {
        return 1;
      }

      if (rightYear === null) {
        return -1;
      }

      return leftYear - rightYear || compareTitles(left, right);
    }

    return compareTitles(left, right);
  });
}

export function collectKeywordCounts(resources) {
  const keywordCounts = new Map();

  for (const resource of Array.from(resources ?? [])) {
    for (const keyword of getNormalizedKeywords(resource)) {
      keywordCounts.set(keyword, (keywordCounts.get(keyword) ?? 0) + 1);
    }
  }

  return Array.from(keywordCounts.entries()).sort(
    (left, right) => right[1] - left[1] || left[0].localeCompare(right[0], undefined, {
      sensitivity: "base",
    })
  );
}
