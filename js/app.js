/**
 * PharmaCAPA - Main Application Orchestrator
 */

document.addEventListener('DOMContentLoaded', () => {
  // Application State
  const state = {
    currentPresetId: 'case-01',
    currentAnalysisData: null,
    activeTab: 'fishbone'
  };

  // DOM Elements
  const elements = {
    caseButtons: document.querySelectorAll('.case-pill-btn'),
    presetGrid: document.getElementById('presetGrid'),
    form: {
      productName: document.getElementById('inputProduct'),
      batchNumber: document.getElementById('inputBatch'),
      dosageForm: document.getElementById('inputDosageForm'),
      productionLine: document.getElementById('inputLine'),
      areaGrade: document.getElementById('inputAreaGrade'),
      stage: document.getElementById('inputStage'),
      detectedBy: document.getElementById('inputDetectedBy'),
      deviationDescription: document.getElementById('inputDescription'),
      parametersBox: document.getElementById('paramPillsGrid')
    },
    btnAnalyze: document.getElementById('btnAnalyze'),
    btnOpenReport: document.getElementById('btnOpenReport'),
    btnConfigApi: document.getElementById('btnConfigApi'),
    
    // Overview Metrics
    overviewTitle: document.getElementById('overviewTitle'),
    overviewCode: document.getElementById('overviewCode'),
    overviewProduct: document.getElementById('overviewProduct'),
    overviewDate: document.getElementById('overviewDate'),
    
    metricRpn: document.getElementById('metricRpn'),
    metricRpnDetail: document.getElementById('metricRpnDetail'),
    metricSeverity: document.getElementById('metricSeverity'),
    metricSeverityBadge: document.getElementById('metricSeverityBadge'),
    metricDisposition: document.getElementById('metricDisposition'),
    metricEngineUsed: document.getElementById('metricEngineUsed'),
    
    // Tab Panels
    tabBtns: document.querySelectorAll('.tab-btn'),
    tabPanels: document.querySelectorAll('.tab-content-panel'),
    fishboneTarget: document.getElementById('fishboneSvgContainer'),
    fiveWhysTarget: document.getElementById('fiveWhysContainer'),
    
    // CAPA elements
    caTableBody: document.getElementById('caTableBody'),
    paTableBody: document.getElementById('paTableBody'),
    effInterval: document.getElementById('effInterval'),
    effCriteria: document.getElementById('effCriteria'),

    // Modals
    reportModal: document.getElementById('reportModal'),
    reportContent: document.getElementById('reportDocContainer'),
    btnCloseReport: document.getElementById('btnCloseReport'),
    btnPrintReport: document.getElementById('btnPrintReport'),
    
    apiModal: document.getElementById('apiModal'),
    btnCloseApi: document.getElementById('btnCloseApi'),
    inputApiKey: document.getElementById('inputApiKey'),
    btnSaveApiKey: document.getElementById('btnSaveApiKey'),
    btnRemoveApiKey: document.getElementById('btnRemoveApiKey'),
    apiStatusNote: document.getElementById('apiStatusNote')
  };

  // 1. Initialize Preset Click Handlers
  function initPresetButtons() {
    elements.caseButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        elements.caseButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const presetId = btn.getAttribute('data-case-id');
        state.currentPresetId = presetId;

        if (presetId === 'custom') {
          loadCustomBlankForm();
        } else {
          const preset = PHARMA_PRESETS.find(p => p.id === presetId);
          if (preset) {
            loadPresetIntoForm(preset);
            loadAnalysisData(preset);
          }
        }
      });
    });
  }

  // Load a preset into form fields
  function loadPresetIntoForm(preset) {
    elements.form.productName.value = preset.productName || '';
    elements.form.batchNumber.value = preset.batchNumber || '';
    elements.form.dosageForm.value = preset.dosageForm || 'Tablet';
    elements.form.productionLine.value = preset.productionLine || '';
    elements.form.areaGrade.value = preset.areaGrade || 'Kelas E';
    elements.form.stage.value = preset.stage || '';
    elements.form.detectedBy.value = preset.detectedBy || '';
    elements.form.deviationDescription.value = preset.deviationSummary || '';

    // Render parameters pill grid
    renderParamGrid(preset.initialParameters || {});
  }

  // Load blank form for custom case
  function loadCustomBlankForm() {
    elements.form.productName.value = 'Injeksi Ciprofloxacin 200 mg / 100 mL';
    elements.form.batchNumber.value = 'BTH-CIP-260888';
    elements.form.dosageForm.value = 'Infus / Cairan Steril';
    elements.form.productionLine.value = 'Lini Sediaan Steril - Gedung Formulasi IV';
    elements.form.areaGrade.value = 'Kelas B / A';
    elements.form.stage.value = 'Sterilisasi Akhir Autoklaf';
    elements.form.detectedBy.value = 'Supervisor Validasi Proses Sterilisasi';
    elements.form.deviationDescription.value = 'Siklus sterilisasi autoklaf mengalami penurunan tekanan uap (steam pressure drop dari 2.1 bar menjadi 1.4 bar) pada menit ke-12 dari total siklus 20 menit. Suhu chamber turun ke 116.8 °C (spesifikasi 121.1 °C). Nilai F0 akumulatif hanya mencapai 10.2 menit (spesifikasi F0 CPOB minimal 15.0 menit).';

    renderParamGrid({
      autoclaveTemp: '116.8 °C (Target 121.1 °C)',
      steamPressure: '1.4 bar (Target 2.1 bar)',
      accumulatedF0: '10.2 Menit (Min 15.0 Menit)',
      bioIndicator: 'Geobacillus stearothermophilus (Sedang diinkubasi)'
    });
  }

  function renderParamGrid(params) {
    if (!elements.form.parametersBox) return;
    const entries = Object.entries(params);
    if (entries.length === 0) {
      elements.form.parametersBox.innerHTML = '<div class="param-item" style="grid-column: span 2;">Tidak ada parameter khusus terdaftar</div>';
      return;
    }
    elements.form.parametersBox.innerHTML = entries.map(([key, val]) => `
      <div class="param-item">
        <strong style="color:#7dd3fc;">${key}:</strong> ${val}
      </div>
    `).join('');
  }

  // 2. Load Analysis Data into Visual Elements
  function loadAnalysisData(data) {
    state.currentAnalysisData = data;

    // Header Overview
    elements.overviewTitle.textContent = data.title || `Penyimpangan: ${data.productName}`;
    elements.overviewCode.textContent = data.code || 'DEV-2026-XXXX';
    elements.overviewProduct.textContent = `${data.productName} (${data.batchNumber})`;
    elements.overviewDate.textContent = data.dateDetected || new Date().toISOString().split('T')[0];

    // Risk Metrics
    const risk = data.riskAssessment || {};
    elements.metricRpn.textContent = risk.rpn || (risk.severity * risk.probability * risk.detectability) || 12;
    elements.metricRpnDetail.textContent = `S:${risk.severity || 4} × P:${risk.probability || 3} × D:${risk.detectability || 1}`;

    const sevLevel = risk.severityLevel || 'Major';
    elements.metricSeverity.textContent = sevLevel.toUpperCase();
    
    // Set color themes for severity badge
    const badge = elements.metricSeverityBadge;
    badge.className = 'metric-icon-box';
    if (sevLevel === 'Critical') {
      badge.classList.add('bg-rose-tint');
      badge.innerHTML = '🚨';
    } else if (sevLevel === 'Major') {
      badge.classList.add('bg-amber-tint');
      badge.innerHTML = '⚠️';
    } else {
      badge.classList.add('bg-cyan-tint');
      badge.innerHTML = 'ℹ️';
    }

    elements.metricDisposition.textContent = risk.batchDisposition || 'Karantina Fisik & Evaluasi Mutu';
    elements.metricEngineUsed.textContent = data.engineUsed || 'Pharma Expert Neural Engine (ICH Q9 / CPOB)';

    // Render Fishbone Diagram
    window.pharmaVisualizer.renderFishbone(
      data.fishboneData,
      data.title || data.deviationSummary || 'Penyimpangan Mutu',
      elements.fishboneTarget
    );

    // Render 5-Whys Timeline
    window.pharmaVisualizer.renderFiveWhys(
      data.fiveWhys,
      elements.fiveWhysTarget
    );

    // Render CAPA Board
    renderCapaBoard(data.capaPlan || {});
  }

  // Render CAPA Tables
  function renderCapaBoard(capa) {
    const caList = capa.correctiveActions || [];
    const paList = capa.preventiveActions || [];
    const review = capa.effectivenessReview || {};

    elements.caTableBody.innerHTML = caList.map(ca => `
      <tr>
        <td><span class="capa-code-badge">${ca.id}</span></td>
        <td>${escapeHtml(ca.description)}</td>
        <td>${escapeHtml(ca.responsible)}</td>
        <td style="font-family: var(--font-mono); font-size: 0.75rem;">${ca.targetDate}</td>
        <td><span class="status-pill ${getStatusPillClass(ca.status)}">${ca.status}</span></td>
      </tr>
    `).join('');

    elements.paTableBody.innerHTML = paList.map(pa => `
      <tr>
        <td><span class="capa-code-badge">${pa.id}</span></td>
        <td>${escapeHtml(pa.description)}</td>
        <td>${escapeHtml(pa.responsible)}</td>
        <td style="font-family: var(--font-mono); font-size: 0.75rem;">${pa.targetDate}</td>
        <td><span class="status-pill ${getStatusPillClass(pa.status)}">${pa.status}</span></td>
      </tr>
    `).join('');

    elements.effInterval.textContent = review.reviewInterval || '60 Hari Pasca Implementasi';
    elements.effCriteria.textContent = review.criteria || 'Zero recurring deviation dalam 5 batch komersial berturut-turut.';
  }

  function getStatusPillClass(status) {
    if (!status) return 'status-pending';
    const s = status.toLowerCase();
    if (s.includes('complete') || s.includes('selesai')) return 'status-completed';
    if (s.includes('progress') || s.includes('jalan')) return 'status-progress';
    if (s.includes('schedule') || s.includes('jadwal')) return 'status-scheduled';
    return 'status-pending';
  }

  // 3. Tab Switching
  elements.tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-tab');
      state.activeTab = targetId;

      elements.tabBtns.forEach(b => b.classList.remove('active'));
      elements.tabPanels.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const panel = document.getElementById(targetId);
      if (panel) panel.classList.add('active');
    });
  });

  // 4. Trigger AI Analysis Button
  elements.btnAnalyze.addEventListener('click', async () => {
    const formData = {
      productName: elements.form.productName.value,
      batchNumber: elements.form.batchNumber.value,
      dosageForm: elements.form.dosageForm.value,
      productionLine: elements.form.productionLine.value,
      areaGrade: elements.form.areaGrade.value,
      stage: elements.form.stage.value,
      detectedBy: elements.form.detectedBy.value,
      deviationDescription: elements.form.deviationDescription.value,
      initialParameters: {}
    };

    if (!formData.deviationDescription || formData.deviationDescription.length < 10) {
      alert("Silakan masukkan deskripsi deviasi/penyimpangan produksi farmasi yang memadai (minimal 10 karakter).");
      return;
    }

    // Set UI to loading state
    const originalText = elements.btnAnalyze.innerHTML;
    elements.btnAnalyze.disabled = true;
    elements.btnAnalyze.innerHTML = `
      <span style="display:inline-block; animation: spin 1s infinite linear;">⟳</span>
      Sedang Menganalisis CPOB / ICH Q9...
    `;

    try {
      const result = await window.pharmaAI.analyzeDeviation(formData);
      loadAnalysisData(result);
    } catch (err) {
      alert("Terjadi kendala saat analisis AI: " + err.message);
    } finally {
      elements.btnAnalyze.disabled = false;
      elements.btnAnalyze.innerHTML = originalText;
    }
  });

  // 5. Official CPOB Report Modal
  elements.btnOpenReport.addEventListener('click', () => {
    if (!state.currentAnalysisData) return;
    window.pharmaReport.renderOfficialReport(state.currentAnalysisData, elements.reportContent);
    elements.reportModal.classList.add('active');
  });

  elements.btnCloseReport.addEventListener('click', () => {
    elements.reportModal.classList.remove('active');
  });

  const btnExecuteExport = document.getElementById('btnExecuteExport');
  const exportFormatSelect = document.getElementById('exportFormatSelect');
  const btnExportLabel = document.getElementById('btnExportLabel');

  if (exportFormatSelect && btnExportLabel) {
    exportFormatSelect.addEventListener('change', () => {
      if (exportFormatSelect.value === 'doc') {
        btnExportLabel.textContent = 'Unduh Dokumen Word (.doc)';
      } else {
        btnExportLabel.textContent = 'Cetak / Simpan ke PDF';
      }
    });
  }

  if (btnExecuteExport && exportFormatSelect) {
    btnExecuteExport.addEventListener('click', () => {
      const selected = exportFormatSelect.value;
      if (selected === 'doc') {
        if (state.currentAnalysisData) {
          window.pharmaReport.downloadWordDoc(state.currentAnalysisData);
        }
      } else {
        window.pharmaReport.printReport();
      }
    });
  }

  // Close modal when clicking background overlay
  elements.reportModal.addEventListener('click', (e) => {
    if (e.target === elements.reportModal) {
      elements.reportModal.classList.remove('active');
    }
  });

  // 6. Settings Modal (Gemini API Configuration)
  elements.btnConfigApi.addEventListener('click', () => {
    elements.inputApiKey.value = window.pharmaAI.getApiKey();
    updateApiStatusDisplay();
    elements.apiModal.classList.add('active');
  });

  elements.btnCloseApi.addEventListener('click', () => {
    elements.apiModal.classList.remove('active');
  });

  elements.btnSaveApiKey.addEventListener('click', () => {
    const key = elements.inputApiKey.value.trim();
    window.pharmaAI.setApiKey(key);
    updateApiStatusDisplay();
    alert(key ? "API Key Google Gemini berhasil disimpan!" : "API Key dihapus. Beralih ke Pharma Expert Neural Engine (Offline Mode).");
    elements.apiModal.classList.remove('active');
  });

  elements.btnRemoveApiKey.addEventListener('click', () => {
    window.pharmaAI.setApiKey('');
    elements.inputApiKey.value = '';
    updateApiStatusDisplay();
    alert("API Key telah dibersihkan. Sistem menggunakan Pharma Expert Neural Engine (Offline Mode).");
  });

  function updateApiStatusDisplay() {
    if (window.pharmaAI.hasApiKey()) {
      elements.apiStatusNote.innerHTML = '<span style="color:#34d399;">✓ Live Google Gemini API Aktif</span> (Model: gemini-1.5-flash)';
    } else {
      elements.apiStatusNote.innerHTML = '<span style="color:#7dd3fc;">● Mode Aktif: Pharma Expert Neural-Heuristic Engine (CPOB & ICH Q9 Offline Mode)</span>';
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  // 7. Operator Quick Incident Chips
  function initQuickChips() {
    const chipBtns = document.querySelectorAll('.quick-chip-btn');
    chipBtns.forEach(chip => {
      chip.addEventListener('click', () => {
        const type = chip.getAttribute('data-chip');
        if (type === 'dissolution') {
          document.getElementById('presetBtn1').click();
        } else if (type === 'thermal') {
          document.getElementById('presetBtn2').click();
        } else if (type === 'sterile') {
          document.getElementById('presetBtn3').click();
        } else if (type === 'capping') {
          document.getElementById('presetBtn4').click();
        }
      });
    });
  }

  // 8. Initial Startup Sequence
  initPresetButtons();
  initQuickChips();
  updateApiStatusDisplay();

  // Load Preset 1 by default
  const defaultPreset = PHARMA_PRESETS[0];
  loadPresetIntoForm(defaultPreset);
  loadAnalysisData(defaultPreset);
});
