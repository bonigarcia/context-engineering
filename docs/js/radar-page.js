// Context Engineering Radar interactive logic
let resourcesData = [];
const radarRadius = 280;
const svgSize = 600;
const centerOffset = svgSize / 2;

// Elements
const radarContainer = document.getElementById("radarContainer");
const resourcesList = document.getElementById("resourcesList");
const searchInput = document.getElementById("radarSearchInput");
const filterButtons = document.querySelectorAll("#radarFilters .filter-pill");

// Modal Elements
const detailModal = document.getElementById("detailModal");
const closeModalBtn = document.getElementById("closePopupBtn");
const modalRingType = document.getElementById("popupRingType");
const modalTitle = document.getElementById("popupTitle");
const modalDescription = document.getElementById("popupDescription");
const modalDomain = document.getElementById("popupDomain");
const modalContribution = document.getElementById("popupContribution");
const modalLink = document.getElementById("popupLink");

// State
let activeFilter = "all";
let searchQuery = "";
let selectedNodeId = null;

// Conversion helper: Polar to Cartesian (relative to center offset)
function polarToCartesian(r, thetaDeg) {
  const thetaRad = (thetaDeg * Math.PI) / 180;
  return {
    x: centerOffset + r * Math.cos(thetaRad),
    y: centerOffset - r * Math.sin(thetaRad) // invert Y for SVG coordinates
  };
}

// Fetch Radar Data
async function loadRadarData() {
  try {
    const response = await fetch("radar-data.json");
    if (!response.ok) {
      throw new Error(`Failed to load radar data: ${response.statusText}`);
    }
    resourcesData = await response.json();
    initRadar();
  } catch (error) {
    console.error("Error loading radar data:", error);
    resourcesList.innerHTML = `<div class="text-muted" style="text-align:center; padding:2rem 0;">Error loading radar data. Please try again later.</div>`;
  }
}

// Color matching function based on level (matching CSS vars)
function getColorForRing(ring) {
  if (ring === "primary") return "var(--radar-primary)";
  if (ring === "secondary") return "var(--radar-secondary)";
  return "var(--radar-tertiary)";
}

// Filtering core function
function filterData() {
  return resourcesData.filter(item => {
    const matchesFilter = activeFilter === "all" || item.ring === activeFilter;
    const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          item.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          item.domain.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesFilter && matchesSearch;
  });
}

// Generate the Radar SVG
function drawRadar() {
  radarContainer.innerHTML = "";

  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", `0 0 ${svgSize} ${svgSize}`);
  svg.setAttribute("class", "radar-svg");

  // 1. Draw concentric background rings
  const ringRadii = [90, 180, 260];
  const ringLabels = ["Primary", "Secondary", "Tertiary"];
  
  ringRadii.forEach((r, idx) => {
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", centerOffset);
    circle.setAttribute("cy", centerOffset);
    circle.setAttribute("r", r);
    circle.setAttribute("class", "radar-ring");
    svg.appendChild(circle);

    // Label each ring
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", centerOffset + 5);
    text.setAttribute("y", centerOffset - r + 15);
    text.setAttribute("class", "radar-ring-text");
    text.textContent = ringLabels[idx];
    svg.appendChild(text);
  });

  // 2. Draw quadrant axes (dashed crosshairs)
  const axes = [
    { x1: centerOffset - radarRadius, y1: centerOffset, x2: centerOffset + radarRadius, y2: centerOffset },
    { x1: centerOffset, y1: centerOffset - radarRadius, x2: centerOffset, y2: centerOffset + radarRadius }
  ];
  
  axes.forEach(axis => {
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", axis.x1);
    line.setAttribute("y1", axis.y1);
    line.setAttribute("x2", axis.x2);
    line.setAttribute("y2", axis.y2);
    line.setAttribute("class", "radar-axis");
    svg.appendChild(line);
  });

  // 3. Draw Quadrant Headers
  const quadrants = [
    { name: "Literature & Research", x: centerOffset + 110, y: centerOffset - 225 },
    { name: "Frameworks & Tools", x: centerOffset - 240, y: centerOffset - 225 },
    { name: "Models & Vendors", x: centerOffset - 230, y: centerOffset + 235 },
    { name: "Communities & Indices", x: centerOffset + 100, y: centerOffset + 235 }
  ];
  
  quadrants.forEach(q => {
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", q.x);
    text.setAttribute("y", q.y);
    text.setAttribute("class", "radar-quadrant-text");
    text.textContent = q.name;
    svg.appendChild(text);
  });

  // 4. Draw node connectors (dashed line to center, active only)
  resourcesData.forEach(item => {
    const pos = polarToCartesian(item.r, item.theta);
    const connector = document.createElementNS("http://www.w3.org/2000/svg", "line");
    connector.setAttribute("x1", centerOffset);
    connector.setAttribute("y1", centerOffset);
    connector.setAttribute("x2", pos.x);
    connector.setAttribute("y2", pos.y);
    connector.setAttribute("id", `connector-${item.id}`);
    connector.setAttribute("class", "radar-node-connector");
    connector.setAttribute("stroke", getColorForRing(item.ring));
    svg.appendChild(connector);
  });

  // 5. Draw data nodes
  const filteredData = filterData();

  filteredData.forEach(item => {
    const pos = polarToCartesian(item.r, item.theta);
    const color = getColorForRing(item.ring);

    const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
    group.setAttribute("class", `radar-node ${item.id === selectedNodeId ? "active" : ""}`);
    group.setAttribute("id", `node-${item.id}`);
    group.style.transformOrigin = `${pos.x}px ${pos.y}px`;
    group.style.color = color;

    // Node Circle
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", pos.x);
    circle.setAttribute("cy", pos.y);
    circle.setAttribute("r", item.id === selectedNodeId ? 9 : 6);
    circle.setAttribute("fill", color);
    circle.setAttribute("stroke", "#ffffff");
    circle.setAttribute("stroke-width", item.id === selectedNodeId ? 2.5 : 1.5);
    group.appendChild(circle);

    // Node Tooltip (shown on hover)
    const title = document.createElementNS("http://www.w3.org/2000/svg", "title");
    title.textContent = `${item.name} (${item.ring} Ring)`;
    group.appendChild(title);

    // Hover interactions
    group.addEventListener("mouseenter", () => highlightNode(item.id));
    group.addEventListener("mouseleave", () => unhighlightNode(item.id));
    
    // Select interaction
    group.addEventListener("click", () => openDetail(item));

    svg.appendChild(group);
  });

  radarContainer.appendChild(svg);
}

// Render result cards in the sidebar
function renderCards() {
  resourcesList.innerHTML = "";
  const filteredData = filterData();

  if (filteredData.length === 0) {
    resourcesList.innerHTML = `<div class="text-muted text-center" style="padding: 2rem 0; font-size: 14px;">No resources match your search criteria.</div>`;
    return;
  }

  filteredData.forEach(item => {
    const card = document.createElement("div");
    card.setAttribute("class", `card card-padding radar-card ring-${item.ring} ${item.id === selectedNodeId ? "active" : ""}`);
    card.setAttribute("id", `card-${item.id}`);
    card.style.borderRadius = "var(--radius)";
    card.style.boxShadow = "var(--shadow)";
    card.style.marginBottom = "12px";

    card.innerHTML = `
      <div class="d-flex justify-content-between align-items-center mb-1">
        <h4 class="h6 mb-0 font-weight-bold" style="color: var(--text);">${item.name}</h4>
        <span class="badge ${item.ring === 'primary' ? 'badge-primary' : item.ring === 'secondary' ? 'badge-secondary' : 'badge-tertiary'}" 
              style="font-size: 10px; padding: 2px 6px; text-transform: uppercase;">${item.ring}</span>
      </div>
      <p class="text-muted mb-2" style="font-size: 13px; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
        ${item.description}
      </p>
      <div class="d-flex justify-content-between" style="font-size: 11px; color: var(--muted);">
        <span>Domain: <strong>${item.domain}</strong></span>
        <span>${item.contribution}</span>
      </div>
    `;

    // Connect interactions
    card.addEventListener("mouseenter", () => highlightNode(item.id));
    card.addEventListener("mouseleave", () => unhighlightNode(item.id));
    card.addEventListener("click", () => openDetail(item));

    resourcesList.appendChild(card);
  });
}

// Highlight a node and its sidebar card
function highlightNode(id) {
  // SVG Node highlight
  const node = document.getElementById(`node-${id}`);
  if (node) {
    node.classList.add("active");
    const circle = node.querySelector("circle");
    if (circle) {
      circle.setAttribute("r", 9);
      circle.setAttribute("stroke-width", 2.5);
    }
  }

  // Active connector line
  const connector = document.getElementById(`connector-${id}`);
  if (connector) {
    connector.classList.add("active");
  }

  // Sidebar card highlight
  const card = document.getElementById(`card-${id}`);
  if (card) {
    card.classList.add("active");
  }
}

// Reset node and card highlight
function unhighlightNode(id) {
  if (id === selectedNodeId) return; // Keep active state if selected

  const node = document.getElementById(`node-${id}`);
  if (node) {
    node.classList.remove("active");
    const circle = node.querySelector("circle");
    if (circle) {
      circle.setAttribute("r", 6);
      circle.setAttribute("stroke-width", 1.5);
    }
  }

  const connector = document.getElementById(`connector-${id}`);
  if (connector) {
    connector.classList.remove("active");
  }

  const card = document.getElementById(`card-${id}`);
  if (card) {
    card.classList.remove("active");
  }
}

// Open Detail Modal
function openDetail(item) {
  // Clear previous active states
  if (selectedNodeId) {
    const oldId = selectedNodeId;
    selectedNodeId = null;
    unhighlightNode(oldId);
  }

  // Set new active state
  selectedNodeId = item.id;
  highlightNode(item.id);

  // Populate Modal Fields
  modalTitle.textContent = item.name;
  modalDescription.textContent = item.description;
  modalRingType.textContent = `${item.ring} Source`;
  modalRingType.style.backgroundColor = getColorForRing(item.ring);
  modalDomain.textContent = item.domain;
  
  if (item.contribution) {
    modalContribution.textContent = item.contribution;
    document.getElementById("popupContribContainer").style.display = "block";
  } else {
    document.getElementById("popupContribContainer").style.display = "none";
  }

  modalLink.setAttribute("href", item.url);

  // Show Modal
  detailModal.classList.add("open");
  detailModal.setAttribute("aria-hidden", "false");
}

// Close Modal
function closeDetail() {
  detailModal.classList.remove("open");
  detailModal.setAttribute("aria-hidden", "true");
  
  if (selectedNodeId) {
    const oldId = selectedNodeId;
    selectedNodeId = null;
    unhighlightNode(oldId);
  }
}

// Setup Event Listeners
function initRadar() {
  drawRadar();
  renderCards();

  // Search Event
  searchInput.addEventListener("input", (e) => {
    searchQuery = e.target.value;
    drawRadar();
    renderCards();
  });

  // Category Filter Events
  filterButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      filterButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeFilter = btn.getAttribute("data-filter");
      
      drawRadar();
      renderCards();
    });
  });

  // Modal Close Triggers
  closeModalBtn.addEventListener("click", closeDetail);
  detailModal.addEventListener("click", (e) => {
    if (e.target === detailModal) {
      closeDetail();
    }
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeDetail();
    }
  });
}

// Load data on start
window.addEventListener("DOMContentLoaded", loadRadarData);
