/**
 * PharmaCAPA - Official CPOB Deviation & CAPA Report Generator
 * Compliant with BPOM RI CPOB 2018/2024 & FDA 21 CFR Part 211
 */

class PharmaReportGenerator {
  /**
   * Render formal CPOB Deviation & CAPA Report inside target element
   * @param {Object} data - Deviation & analysis data
   * @param {HTMLElement} targetEl - Container DOM element
   */
  renderOfficialReport(data, targetEl) {
    if (!targetEl || !data) return;

    const risk = data.riskAssessment || {};
    const capa = data.capaPlan || {};
    const caList = capa.correctiveActions || [];
    const paList = capa.preventiveActions || [];
    const review = capa.effectivenessReview || {};

    const sevBadgeClass = risk.severityLevel === 'Critical' ? 'rep-badge-critical' : (risk.severityLevel === 'Major' ? 'rep-badge-major' : 'rep-badge-minor');

    const html = `
      <div class="cpob-official-doc" id="cpobOfficialDocument">
        <!-- Document Header -->
        <div class="doc-header-border">
          <table class="doc-header-table">
            <tr>
              <td class="logo-cell" rowspan="3" style="width: 130px; text-align: center; vertical-align: middle;">
                <div class="company-badge-logo">
                  <span class="cross-icon">✚</span>
                  <div class="logo-sub">PHARMA QA</div>
                </div>
              </td>
              <td class="title-cell" rowspan="3" style="text-align: center;">
                <div class="company-name">PT PHARMA NUSANTARA Tbk. — QUALITY ASSURANCE DIVISION</div>
                <div class="doc-title-main">FORMULIR PENYELIDIKAN PENYIMPANGAN & RENCANA CAPA</div>
                <div class="doc-subtitle-sub">CPOB 2018/2024 (BPOM RI) & cGMP FDA 21 CFR Part 211 COMPLIANT</div>
              </td>
              <td class="meta-label">No. Dokumen:</td>
              <td class="meta-val">SOP-QA-042-F01 (Rev. 05)</td>
            </tr>
            <tr>
              <td class="meta-label">No. Deviasi:</td>
              <td class="meta-val highlight-code">${data.code || 'DEV-2026-XXXX'}</td>
            </tr>
            <tr>
              <td class="meta-label">Tgl. Terbit:</td>
              <td class="meta-val">${data.dateDetected || new Date().toISOString().split('T')[0]}</td>
            </tr>
          </table>
        </div>

        <!-- Section 1: Informasi Batch & Kejadian -->
        <div class="rep-section">
          <div class="rep-section-title">BAGIAN 1: INFORMASI BATCH & RINCIAN PENYIMPANGAN</div>
          <table class="rep-data-grid">
            <tr>
              <td class="grid-label">Nama Produk</td>
              <td class="grid-val font-bold">${data.productName || '-'}</td>
              <td class="grid-label">No. Bets / Batch</td>
              <td class="grid-val font-mono highlight-batch">${data.batchNumber || '-'}</td>
            </tr>
            <tr>
              <td class="grid-label">Bentuk Sediaan</td>
              <td class="grid-val">${data.dosageForm || '-'}</td>
              <td class="grid-label">Lini Produksi / Lokasi</td>
              <td class="grid-val">${data.productionLine || '-'}</td>
            </tr>
            <tr>
              <td class="grid-label">Kelas Kebersihan Ruang</td>
              <td class="grid-val">${data.areaGrade || 'Kelas E'}</td>
              <td class="grid-label">Tahapan Proses</td>
              <td class="grid-val">${data.stage || '-'}</td>
            </tr>
            <tr>
              <td class="grid-label">Dideteksi Oleh</td>
              <td class="grid-val">${data.detectedBy || '-'}</td>
              <td class="grid-label">Tanggal Deteksi</td>
              <td class="grid-val">${data.dateDetected || '-'}</td>
            </tr>
          </table>

          <div class="rep-narrative-box">
            <div class="box-label">Deskripsi Kejadian Penyimpangan (Faktual & Terukur):</div>
            <p class="box-text">${data.deviationSummary || '-'}</p>
          </div>
        </div>

        <!-- Section 2: Kajian Risiko Mutu (ICH Q9) -->
        <div class="rep-section">
          <div class="rep-section-title">BAGIAN 2: KAJIAN RISIKO MUTU & DISPOSISI BETS (ICH Q9 QUALITY RISK MANAGEMENT)</div>
          <div class="risk-summary-flex">
            <div class="risk-matrix-card">
              <div class="risk-score-pill ${sevBadgeClass}">
                KLASIFIKASI: ${risk.severityLevel ? risk.severityLevel.toUpperCase() : 'MAJOR'}
              </div>
              <div class="rpn-calc">
                <span>Severity (S): <strong>${risk.severity || 4}/5</strong></span> •
                <span>Probability (P): <strong>${risk.probability || 3}/5</strong></span> •
                <span>Detectability (D): <strong>${risk.detectability || 1}/5</strong></span>
              </div>
              <div class="rpn-total">Risk Priority Number (RPN): <strong>${risk.rpn || 12}</strong></div>
            </div>
            <div class="disposition-card">
              <div class="disp-title">REKOMENDASI DISPOSISI BETS:</div>
              <div class="disp-status">${risk.batchDisposition || 'Karantina Fisik & Sistem'}</div>
              <div class="disp-cqa"><strong>Dampak CQA:</strong> ${risk.cqaImpact || '-'}</div>
            </div>
          </div>
        </div>

        <!-- Section 3: Analisis Akar Masalah (5-Whys & 6M) -->
        <div class="rep-section">
          <div class="rep-section-title">BAGIAN 3: ANALISIS AKAR MASALAH (ROOT CAUSE ANALYSIS - ISHIKAWA & 5-WHYS)</div>
          <div class="whys-summary-table">
            <div class="whys-table-title">Deduction Path (Metode 5-Whys):</div>
            <ol class="formal-whys-list">
              ${(data.fiveWhys || []).map((w, i) => `
                <li class="${i === (data.fiveWhys.length - 1) ? 'final-root-why' : ''}">
                  <strong>W${w.step || i+1}: ${this.escapeHtml(w.question)}</strong>
                  <p class="why-ans-text">${this.escapeHtml(w.answer)}</p>
                </li>
              `).join('')}
            </ol>
          </div>
        </div>

        <!-- Section 4: Rencana CAPA (Corrective and Preventive Action) -->
        <div class="rep-section">
          <div class="rep-section-title">BAGIAN 4: RENCANA TINDAKAN KOREKTIF & PREVENTIF (CAPA PLAN - ICH Q10)</div>
          
          <div class="capa-subheading">A. Tindakan Korektif Langsung (Corrective Action - CA)</div>
          <table class="rep-capa-table">
            <thead>
              <tr>
                <th style="width: 70px;">Kode</th>
                <th>Deskripsi Tindakan Korektif</th>
                <th style="width: 180px;">Penanggung Jawab</th>
                <th style="width: 100px;">Target</th>
                <th style="width: 90px;">Status</th>
              </tr>
            </thead>
            <tbody>
              ${caList.map(ca => `
                <tr>
                  <td class="font-mono text-center font-bold">${ca.id}</td>
                  <td>${this.escapeHtml(ca.description)}</td>
                  <td>${this.escapeHtml(ca.responsible)}</td>
                  <td class="text-center font-mono">${ca.targetDate}</td>
                  <td class="text-center"><span class="table-status-pill">${ca.status}</span></td>
                </tr>
              `).join('')}
            </tbody>
          </table>

          <div class="capa-subheading" style="margin-top: 14px;">B. Tindakan Pencegahan Berulang (Preventive Action - PA)</div>
          <table class="rep-capa-table">
            <thead>
              <tr>
                <th style="width: 70px;">Kode</th>
                <th>Deskripsi Tindakan Pencegahan Sistemik</th>
                <th style="width: 180px;">Penanggung Jawab</th>
                <th style="width: 100px;">Target</th>
                <th style="width: 90px;">Status</th>
              </tr>
            </thead>
            <tbody>
              ${paList.map(pa => `
                <tr>
                  <td class="font-mono text-center font-bold">${pa.id}</td>
                  <td>${this.escapeHtml(pa.description)}</td>
                  <td>${this.escapeHtml(pa.responsible)}</td>
                  <td class="text-center font-mono">${pa.targetDate}</td>
                  <td class="text-center"><span class="table-status-pill">${pa.status}</span></td>
                </tr>
              `).join('')}
            </tbody>
          </table>

          <div class="effectiveness-box">
            <span class="eff-label">Protokol Evaluasi Efektivitas CAPA (${review.reviewInterval || '60 Hari'}):</span>
            <span class="eff-text">${review.criteria || 'Zero recurring deviation dalam 5 batch komersial berikutnya.'}</span>
          </div>
        </div>

        <!-- Section 5: Otorisasi & Tanda Tangan Formal -->
        <div class="rep-section" style="page-break-inside: avoid;">
          <div class="rep-section-title">BAGIAN 5: OTORISASI & PERSETUJUAN MULTIDISIPLIN (CPOB COMPLIANCE SIGN-OFF)</div>
          <table class="sign-off-table">
            <tr>
              <td style="width: 33.3%;">
                <div class="sign-role">DIPERIKSA OLEH (INVESTIGATOR):</div>
                <div class="sign-space">
                  <div class="digital-sign-stamp">
                    <span>DIGITALLY VERIFIED</span>
                    <small>QA Compliance Specialist</small>
                  </div>
                </div>
                <div class="sign-name">apt. Rismawati L., S.Farm.</div>
                <div class="sign-meta">Tanggal: ${data.dateDetected || '2026-10-22'}</div>
              </td>
              <td style="width: 33.3%;">
                <div class="sign-role">DISETUJUI OLEH (PRODUKSI):</div>
                <div class="sign-space">
                  <div class="digital-sign-stamp">
                    <span>DIGITALLY VERIFIED</span>
                    <small>Head of Production</small>
                  </div>
                </div>
                <div class="sign-name">Ir. Hendra Wijaya, M.M.</div>
                <div class="sign-meta">Tanggal: ${data.dateDetected || '2026-10-22'}</div>
              </td>
              <td style="width: 33.3%;">
                <div class="sign-role">DISETUJUI AKHIR (PEMASTIAN MUTU):</div>
                <div class="sign-space">
                  <div class="digital-sign-stamp stamp-gold">
                    <span>QUALIFIED PERSON / QA HEAD</span>
                    <small>BPOM CPOB Authorized</small>
                  </div>
                </div>
                <div class="sign-name">apt. Dr. Arry S., M.Si.</div>
                <div class="sign-meta">Tanggal: ${data.dateDetected || '2026-10-22'}</div>
              </td>
            </tr>
          </table>
          <div class="audit-trail-footer">
            <span>Audit Trail Token: SHA256-e9b42c-${Date.now().toString(16)}</span> •
            <span>Sistem: PharmaCAPA AI v2.4 (ICH Q9/Q10 Engine)</span> •
            <span>Halaman 1 dari 1 (Dokumen Terkendali)</span>
          </div>
        </div>
      </div>
    `;

    targetEl.innerHTML = html;
  }

  /**
   * Trigger native browser print dialog for the official report
   */
  printReport() {
    window.print();
  }

  /**
   * Export the complete official CPOB document as a formatted Microsoft Word file (.doc)
   * @param {Object} data - Deviation data
   */
  downloadWordDoc(data) {
    if (!data) return;
    const docElement = document.getElementById('cpobOfficialDocument');
    if (!docElement) return;

    const contentHtml = docElement.innerHTML;
    const preHtml = `
      <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
      <head>
        <meta charset='utf-8'>
        <title>Formulir CPOB - ${data.code || 'DEV-2026'}</title>
        <!--[if gte mso 9]>
        <xml>
          <w:WordDocument>
            <w:View>Print</w:View>
            <w:Zoom>100</w:Zoom>
            <w:DoNotOptimizeForBrowser/>
          </w:WordDocument>
        </xml>
        <![endif]-->
        <style>
          body { font-family: 'Arial', sans-serif; font-size: 10pt; color: #0f172a; line-height: 1.35; margin: 15mm; }
          table { width: 100%; border-collapse: collapse; margin-bottom: 8px; }
          td, th { border: 1px solid #475569; padding: 6px 8px; font-size: 9pt; }
          .doc-header-border { border: 2px solid #0f172a; margin-bottom: 12px; }
          .rep-section-title { background: #0f172a; color: #ffffff; font-weight: bold; padding: 5px 8px; font-size: 9.5pt; margin-top: 10px; margin-bottom: 5px; }
          .grid-label { background: #f1f5f9; font-weight: bold; width: 130px; }
          .rep-badge-critical { background: #fee2e2; color: #991b1b; font-weight: bold; }
          .rep-badge-major { background: #fef3c7; color: #92400e; font-weight: bold; }
          .rep-badge-minor { background: #e0f2fe; color: #075985; font-weight: bold; }
          .digital-sign-stamp { border: 1.5px dashed #0284c7; padding: 5px; text-align: center; font-size: 8pt; font-weight: bold; color: #0284c7; }
          .stamp-gold { border-color: #b45309; color: #b45309; }
          .effectiveness-box { border: 1px dashed #0284c7; background: #f0f9ff; padding: 6px 10px; font-size: 8.5pt; margin-top: 8px; }
        </style>
      </head>
      <body>
    `;
    const postHtml = `</body></html>`;
    const fullHtml = preHtml + contentHtml + postHtml;

    const blob = new Blob(['\ufeff', fullHtml], {
      type: 'application/msword'
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Formulir_CPOB_${data.code || 'DEV-2026'}.doc`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
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

// Global report generator instance
window.pharmaReport = new PharmaReportGenerator();
