/**
 * PharmaCAPA - Interactive Ishikawa (Fishbone) Diagram & 5-Whys Tree Generator
 */

class PharmaVisualizer {
  constructor() {
    this.container = null;
  }

  /**
   * Render dynamic SVG Fishbone (Ishikawa 6M) Diagram
   * @param {Object} fishboneData - { man: [], machine: [], material: [], method: [], measurement: [], environment: [] }
   * @param {string} problemTitle - The deviation title/effect
   * @param {HTMLElement} targetEl - DOM container element
   */
  renderFishbone(fishboneData, problemTitle, targetEl) {
    if (!targetEl) return;
    this.container = targetEl;

    const width = 1100;
    const height = 580;
    const spineY = height / 2;
    const headX = width - 180;
    const tailX = 60;

    // Branches definition (Top 3: Man, Machine, Material; Bottom 3: Method, Measurement, Environment)
    const branches = [
      { key: 'man', label: '1. MAN (Personil)', x: 220, isTop: true, color: '#3b82f6' },
      { key: 'machine', label: '2. MACHINE (Peralatan)', x: 480, isTop: true, color: '#ef4444' },
      { key: 'material', label: '3. MATERIAL (Bahan)', x: 740, isTop: true, color: '#8b5cf6' },
      { key: 'method', label: '4. METHOD (SOP/Metode)', x: 220, isTop: false, color: '#f59e0b' },
      { key: 'measurement', label: '5. MEASUREMENT (Ukur/QC)', x: 480, isTop: false, color: '#06b6d4' },
      { key: 'environment', label: '6. MILIEU (Lingkungan HVAC)', x: 740, isTop: false, color: '#10b981' }
    ];

    let svgHtml = `
      <svg viewBox="0 0 ${width} ${height}" class="fishbone-svg" preserveAspectRatio="xMidYMid meet">
        <defs>
          <linearGradient id="spineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#334155" />
            <stop offset="80%" stop-color="#0284c7" />
            <stop offset="100%" stop-color="#0369a1" />
          </linearGradient>
          <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
          </marker>
          <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>

        <!-- Main Spine -->
        <line x1="${tailX}" y1="${spineY}" x2="${headX}" y2="${spineY}" stroke="url(#spineGrad)" stroke-width="6" stroke-linecap="round" marker-end="url(#arrow)" />
        
        <!-- Fish Head: Problem Box -->
        <g class="fishbone-head" transform="translate(${headX + 10}, ${spineY - 55})">
          <rect width="190" height="110" rx="12" fill="#0f172a" stroke="#0ea5e9" stroke-width="2.5" filter="drop-shadow(0 8px 16px rgba(14,165,233,0.25))" />
          <rect x="0" y="0" width="190" height="28" rx="12" fill="#0ea5e9" />
          <text x="95" y="19" text-anchor="middle" fill="#ffffff" font-size="11" font-weight="700" letter-spacing="1">DEVIASI MUTU / EFEK</text>
          <foreignObject x="10" y="34" width="170" height="70">
            <div xmlns="http://www.w3.org/1999/xhtml" class="fish-head-text" title="${this.escapeHtml(problemTitle)}">
              ${this.escapeHtml(problemTitle)}
            </div>
          </foreignObject>
        </g>
    `;

    // Draw each 6M category branch
    branches.forEach(branch => {
      const items = (fishboneData && fishboneData[branch.key]) || [];
      const branchAngle = branch.isTop ? -50 : 50;
      const branchLength = 175;
      const endX = branch.x + (branch.isTop ? 70 : 70);
      const endY = branch.isTop ? spineY - branchLength : spineY + branchLength;

      // Category Header Box
      const labelY = branch.isTop ? endY - 26 : endY + 6;
      svgHtml += `
        <!-- Branch: ${branch.key} -->
        <line x1="${branch.x}" y1="${spineY}" x2="${endX}" y2="${endY}" stroke="${branch.color}" stroke-width="3.5" stroke-linecap="round" />
        
        <g class="branch-label" transform="translate(${endX - 85}, ${labelY})">
          <rect width="170" height="26" rx="6" fill="#0f172a" stroke="${branch.color}" stroke-width="1.8" />
          <text x="85" y="17" text-anchor="middle" fill="${branch.color}" font-size="10.5" font-weight="700">${branch.label}</text>
        </g>
      `;

      // Draw sub-branches / causes
      items.forEach((item, index) => {
        const factor = (index + 1) / (items.length + 1);
        const subOriginX = branch.x + (endX - branch.x) * factor;
        const subOriginY = spineY + (endY - spineY) * factor;

        const subLen = 145;
        const subEndX = subOriginX - subLen;
        const subEndY = subOriginY;

        const isRoot = item.isRoot;
        const strokeColor = isRoot ? '#f43f5e' : '#64748b';
        const strokeWidth = isRoot ? 2.5 : 1.5;

        svgHtml += `
          <!-- Subcause ${index + 1} -->
          <line x1="${subOriginX}" y1="${subOriginY}" x2="${subEndX}" y2="${subEndY}" stroke="${strokeColor}" stroke-width="${strokeWidth}" stroke-dasharray="${isRoot ? 'none' : '4,2'}" />
          
          <g class="subcause-item ${isRoot ? 'is-root-cause' : ''}" transform="translate(${subEndX - 10}, ${subEndY - 14})" data-severity="${item.severity || 'low'}">
            ${isRoot ? `
              <circle cx="0" cy="14" r="5" fill="#f43f5e" filter="url(#glow)">
                <animate attributeName="r" values="4;7;4" dur="2s" repeatCount="indefinite" />
              </circle>
            ` : ''}
            <foreignObject x="-210" y="-8" width="200" height="46">
              <div xmlns="http://www.w3.org/1999/xhtml" class="subcause-box ${isRoot ? 'root-box' : ''}" title="${this.escapeHtml(item.cause)}">
                ${isRoot ? '<span class="root-badge">ROOT CAUSE</span>' : ''}
                <span class="cause-text">${this.escapeHtml(item.cause)}</span>
              </div>
            </foreignObject>
          </g>
        `;
      });
    });

    svgHtml += `</svg>`;
    targetEl.innerHTML = svgHtml;
  }

  /**
   * Render Interactive 5-Whys Sequential Ladder
   * @param {Array} fiveWhys - Array of { step, question, answer }
   * @param {HTMLElement} targetEl - DOM container element
   */
  renderFiveWhys(fiveWhys, targetEl) {
    if (!targetEl || !fiveWhys) return;

    let html = `
      <div class="five-whys-container">
        <div class="five-whys-header">
          <div class="whys-title">
            <span class="pulse-icon">🔍</span>
            <span>Metode 5-Whys Root Cause Drill-down (Standar CPOB / ICH Q9)</span>
          </div>
          <span class="whys-badge">5 Langkah Investigasi Mendalam</span>
        </div>
        <div class="five-whys-timeline">
    `;

    fiveWhys.forEach((why, idx) => {
      const isLast = idx === fiveWhys.length - 1;
      html += `
        <div class="why-card ${isLast ? 'why-root-card' : ''}">
          <div class="why-indicator">
            <div class="why-number">${why.step || idx + 1}</div>
            ${!isLast ? '<div class="why-line"></div>' : ''}
          </div>
          <div class="why-content">
            <div class="why-question">
              <span class="why-q-tag">Tanya:</span>
              <span>${this.escapeHtml(why.question)}</span>
            </div>
            <div class="why-answer">
              <span class="why-a-tag ${isLast ? 'tag-root' : ''}">${isLast ? '🎯 AKAR MASALAH (ROOT CAUSE):' : 'Jawaban:'}</span>
              <p class="why-text">${this.escapeHtml(why.answer)}</p>
            </div>
          </div>
        </div>
      `;
    });

    html += `
        </div>
      </div>
    `;

    targetEl.innerHTML = html;
  }

  escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }
}

// Global visualizer instance
window.pharmaVisualizer = new PharmaVisualizer();
