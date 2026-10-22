# 💊 PharmaCAPA AI — Pharmaceutical Batch Deviation & Root Cause Analysis Copilot

> **Aplikasi AI Industri Farmasi untuk Manajemen Penyimpangan Mutu (Batch Deviation), Analisis Akar Masalah (6M Ishikawa & 5-Whys), dan Penyusunan Tindakan Korektif & Preventif (CAPA)**  
> **Kepatuhan Regulasi:** Pedoman CPOB 2018/2024 (BPOM RI) • cGMP FDA 21 CFR Part 211.192 • ICH Q9 (Quality Risk Management) • ICH Q10 (Pharmaceutical Quality System).

---

## 📌 1. Latar Belakang & Masalah Industri Farmasi

Di industri manufaktur farmasi, kepatuhan terhadap standar **CPOB (Cara Pembuatan Obat yang Baik)** dan **cGMP (current Good Manufacturing Practice)** adalah mandat hukum dan etika medis tertinggi. Setiap kali terjadi penyimpangan mutu (*batch deviation*) atau hasil uji di luar spesifikasi (*Out of Specification / OOS*), tim **Quality Assurance (QA)** diwajibkan melakukan investigasi menyeluruh sebelum produk dapat dirilis ke pasar atau diputuskan untuk ditolak (*reject/destruksi*).

### Masalah Nyata di Industri Farmasi:
1. **Waktu Investigasi yang Lambat:** Proses investigasi manual sering memakan waktu berhari-hari hingga berminggu-minggu, menahan rilis produk di gudang karantina dan menimbulkan kerugian finansial.
2. **Keterbatasan Analisis Akar Masalah (Root Cause):** Sering kali tim hanya mengidentifikasi "gejala" (misal: kesalahan operator) tanpa menemukan akar masalah sistemik (*true systemic root cause*) pada mesin, kalibrasi, atau SOP.
3. **Penyusunan CAPA yang Kurang Efektif:** Tindakan korektif dan preventif sering kali bersifat generik sehingga deviasi yang sama berulang kembali (*recurring deviations*), yang menjadi temuan audit kritis oleh inspektur BPOM atau FDA.

---

## 💡 2. Solusi yang Dihadirkan: PharmaCAPA AI

**PharmaCAPA AI** hadir sebagai *asisten cerdas (AI Copilot)* berbasis web bagi personel QA, QC, dan Produksi farmasi untuk:
1. **Mengotomatisasi Penilaian Risiko Mutu (ICH Q9 Risk Matrix):** Menghitung nilai *Severity (S)*, *Probability (P)*, *Detectability (D)*, dan *Risk Priority Number (RPN)* secara objektif.
2. **Mengklasifikasikan Tingkat Keparahan Deviasi:** Mengkategorikan insiden menjadi **Critical**, **Major**, atau **Minor** serta memberikan rekomendasi disposisi bets seketika (*Quarantine, Reject, Rework, atau Conditional Release*).
3. **Membangun Diagram Tulang Ikan (Ishikawa 6M) Interaktif:** Memetakan seluruh faktor penyebab ke dalam 6 domain farmasi:
   - **1. Man (Personil & Kompetensi)**
   - **2. Machine (Peralatan, Tooling, & Status Kalibrasi)**
   - **3. Material (Bahan Baku API, Eksipien, & Kemasan Primer)**
   - **4. Method (SOP, Instruksi Kerja, & Line Clearance)**
   - **5. Measurement (Metrologi, Instrumen QC, & Validasi Analitik)**
   - **6. Milieu (Lingkungan Bersih HVAC, Tekanan Diferensial ΔP, Suhu & RH)**
4. **Menjalankan Metode 5-Whys Terstruktur:** Menelusuri rantai kausalitas dari gejala awal hingga ke akar masalah sistemik.
5. **Menyintesis Rencana CAPA Resmi (ICH Q10):** Menghasilkan tabel *Corrective Action (CA)* langsung dan *Preventive Action (PA)* sistemik lengkap dengan PIC, batas waktu, dan kriteria uji efektivitas (*Effectiveness Review*).
6. **Menerbitkan Formulir Resmi CPOB Siap Cetak/PDF:** Menghasilkan dokumen resmi investigasi deviasi farmasi (`SOP-QA-042`) dengan stempel verifikasi digital.

---

## 🏗️ 3. Arsitektur Teknologi & Fitur AI

### A. Dual-Engine AI Architecture
* **Mode 1: Pharma Expert Neural-Heuristic Engine (Offline Default):**  
  Mesin inferensi aturan farmasi berbasis matriks risiko ICH Q9 dan logika CPOB BPOM. Berjalan 100% lokal, cepat, andal, dan siap didemokan kapan saja tanpa ketergantungan koneksi internet maupun kuota API.
* **Mode 2: Live Google Gemini API Integration (Opsional):**  
  Mendukung integrasi langsung ke LLM Google Gemini (Gemini 1.5 Flash) untuk analisis teks deviasi bebas secara generatif dan adaptif.

### B. Antarmuka Web Modern (Clinical High-Tech Aesthetic)
* Dibangun menggunakan **HTML5 semantik, Vanilla Modern CSS, dan JavaScript ES6 murni** (tanpa dependensi framework yang berat).
* Mengusung desain *Clinical Navy & Slate Glassmorphism* dengan tipografi modern, aksen bercahaya (*glow badges*), visualisasi vektor SVG interaktif, dan *print stylesheet* siap cetak A4.

---

## 🧪 4. Empat Skenario Uji Industri Farmasi (Preset Kasus QA)

Aplikasi telah dilengkapi dengan 4 preset kasus deviasi riil yang biasa dihadapi pabrik farmasi:

| Kode Deviasi | Nama Produk | Lini Produksi | Deskripsi Kejadian | Klasifikasi |
|---|---|---|---|---|
| **DEV-2026-0842** | Paracetamol 500 mg Kaplet | Lini Solid Non-Steril | Hasil uji disolusi OOS tahap S1/S2 (Q=73.5% vs standar Q=80%). Disebabkan drift sensor gaya kompresi rotary tablet press. | **MAJOR** |
| **DEV-2026-0915** | Amoxicillin 125mg/5mL Sirup Kering | Lini Betalaktam Khusus | Lonjakan suhu inlet Fluid Bed Dryer hingga 78.4 °C akibat katup uap macet (ancaman degradasi cincin betalaktam). | **CRITICAL** |
| **DEV-2026-1002** | Ceftriaxone 1 g Serbuk Injeksi | Lini Aseptis Steril Kelas A/B | Deteksi partikel karet elastomerik hitam 3.4% pada pengisian vial akibat gesekan vibratory bowl stopper. | **CRITICAL** |
| **DEV-2026-1120** | Cetirizine HCl 10 mg Tablet | Lini Cetak Rotari | Variasi bobot tablet tinggi (RSD 4.2%) dan capping 1.8% akibat pre-compression roller mengendur dan fines berlebih. | **MINOR** |

> 💡 **Fitur Live Input Kustom:** Penguji/Dosen dapat mengklik opsi **"Input Deviasi Kustom Bebas"** untuk menguji kecerdasan AI dalam membedah kasus deviasi farmasi lainnya secara spontan!

---

## 🚀 5. Cara Menjalankan Aplikasi Secara Lokal

Aplikasi ini sangat ringan dan dapat dijalankan di komputer mana pun tanpa perlu instalasi `npm` atau kompilasi rumit:

### Langkah Menjalankan:
1. Buka terminal di folder proyek:
   ```bash
   cd "/Users/rismawatilaila/Tugas AI Prof Arry"
   ```
2. Jalankan skrip peluncur:
   ```bash
   ./run_app.sh
   ```
   *Atau langsung jalankan web server Python:*
   ```bash
   python3 -m http.server 3000
   ```
3. Buka peramban (browser) dan akses:
   ```
   http://localhost:3000
   ```

---

## 📋 6. Panduan Demonstrasi untuk Evaluasi Dosen (Prof. Arry)

Saat mempresentasikan aplikasi ini di hadapan dosen:
1. **Langkah 1 (Tampilan Awal):** Tunjukkan bahwa sistem langsung memuat kasus deviasi riil pertama (Disolusi OOS Paracetamol). Jelaskan metrik RPN, Klasifikasi Mutu (*MAJOR*), dan Disposisi Bets (*Karantina*).
2. **Langkah 2 (Tab Ishikawa 6M):** Buka tab diagram tulang ikan untuk memperlihatkan bagaimana AI memetakan akar masalah mekanis (*load cell drift*) dengan indikator merah berdenyut.
3. **Langkah 3 (Tab 5-Whys):** Klik tab 5-Whys untuk menunjukkan proses penalaran bertingkat dari gejala disolusi hingga akar masalah manajemen kalibrasi mesin.
4. **Langkah 4 (Tab CAPA):** Tunjukkan rencana tindakan korektif (CA) dan preventif (PA) yang spesifik serta terukur.
5. **Langkah 5 (Ekspor Dokumen Resmi CPOB):** Klik tombol **"Cetak Dokumen Resmi CPOB"**. Tunjukkan formulir resmi berkepala surat standar BPOM yang lengkap dengan tanda tangan digital QA, Produksi, dan Kepala Pemastian Mutu.

---

*Dikembangkan untuk Tugas Mata Kuliah Aplikasi AI untuk Industri — 2026.*
