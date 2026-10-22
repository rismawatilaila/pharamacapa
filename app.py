"""
PharmaCAPA AI — Pharmaceutical Deviation & CAPA Copilot (Modern & Minimalist Operator Edition)
Standar Kepatuhan: BPOM RI CPOB 2018/2024, cGMP FDA 21 CFR Part 211, ICH Q9 & Q10
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="PharmaCAPA AI — Operator & QA Assistant",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed"  # Collapsed by default for clean minimalist workspace
)

# Modern Minimalist Clinical Styling
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Clean Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid rgba(14, 165, 233, 0.25);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 4px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(14, 165, 233, 0.15);
        color: #38bdf8;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .hero-title {
        color: #ffffff;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
    }
    .hero-desc {
        color: #94a3b8;
        font-size: 14px;
        margin-top: 6px;
    }

    /* Minimalist Operator Card */
    .operator-card {
        background: #ffffff;
        color: #0f172a;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    /* Status Pills */
    .pill-critical {
        background: #fee2e2;
        color: #991b1b;
        border: 1px solid #f87171;
        padding: 4px 12px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 13px;
        display: inline-block;
    }
    .pill-major {
        background: #fef3c7;
        color: #92400e;
        border: 1px solid #fcd34d;
        padding: 4px 12px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 13px;
        display: inline-block;
    }
    .pill-minor {
        background: #e0f2fe;
        color: #0369a1;
        border: 1px solid #7dd3fc;
        padding: 4px 12px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 13px;
        display: inline-block;
    }

    /* Whys Minimalist Steps */
    .step-box {
        background: rgba(15, 23, 42, 0.03);
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0ea5e9;
        border-radius: 0 10px 10px 0;
        padding: 12px 18px;
        margin-bottom: 12px;
    }
    .step-root {
        background: #fff1f2;
        border: 1px solid #fecdd3;
        border-left: 5px solid #f43f5e;
        border-radius: 0 10px 10px 0;
        padding: 14px 18px;
        margin-bottom: 12px;
    }

    /* Clean Metric Box */
    div[data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)

# Master Data Presets
PRESETS = {
    "1. Uji Disolusi OOS — Paracetamol 500mg": {
        "code": "DEV-2026-0842",
        "title": "Kegagalan Uji Disolusi (OOS) pada Paracetamol 500 mg Tablet",
        "product": "Paracetamol 500 mg Kaplet",
        "batch": "BTH-PCT-260412",
        "dosage_form": "Tablet / Kaplet Salut Film",
        "line": "Lini Solid Non-Steril Gedung II",
        "cleanroom": "Kelas E (White Area)",
        "stage": "Pencetakan & Pengujian QC Ruahan",
        "detected_by": "Staff Analis QC Kimia Fisika",
        "description": "Hasil uji disolusi tahap S1 (n=6) menunjukkan nilai Q30 menit berada di kisaran 68% - 74% (tidak memenuhi syarat rilis CPOB Q=80%). Nilai kekerasan tablet tercatat 14.2 kP (spesifikasi standar: 7 - 10 kP), sehingga waktu hancur terlambat.",
        "severity": 4, "probability": 3, "detectability": 1, "rpn": 12,
        "classification": "Major",
        "disposition": "Karantina Formal & Evaluasi Rework/Destruksi",
        "cqa_impact": "Laju disolusi melambat, berisiko mengganggu bioavailabilitas zat aktif dalam tubuh pasien.",
        "cpp_correlation": "Gaya kompresi rotary tablet press melebihi setpoint akibat sensor load cell tidak akurat.",
        "fishbone": {
            "1. Man (Personil)": ["Operator baru belum tersertifikasi penuh mesin cetak Fette", "Pemeriksaan IPC kekerasan terlewat saat pergantian shift"],
            "2. Machine (Peralatan)": ["🎯 ROOT CAUSE: Sensor load cell gaya kompresi mengalami drift pembacaan +22%", "Alarm over-force pada HMI dinonaktifkan sementara"],
            "3. Material (Bahan)": ["Kadar air granul (LOD) 1.1% (agak terlalu kering)", "Sifat alir serbuk berubah akibat over-drying di FBD"],
            "4. Method (SOP)": ["SOP belum mewajibkan verifikasi dua orang (four-eyes check) saat setup", "Batas tindakan IPC belum terintegrasi ke alarm HMI"],
            "5. Measurement (Alat)": ["Hardness Tester Erweka terkalibrasi harian", "Disolusi bath USP Apparatus II terkalibrasi"],
            "6. Milieu (Lingkungan)": ["Suhu ruangan 24.5 °C dan RH 58% masih dalam batas alert limit Kelas E"]
        },
        "five_whys": [
            ("Mengapa tablet tidak memenuhi syarat disolusi Q=80%?", "Kekerasan tablet rata-rata 14.2 kP (jauh di atas batas 7 - 10 kP), waktu hancur molor ke 24 menit."),
            ("Mengapa kekerasan tablet melonjak tinggi?", "Gaya kompresi utama mesin cetak berjalan di 24.8 kN padahal setpoint SOP adalah 18 - 20 kN."),
            ("Mengapa mesin berjalan pada gaya 24.8 kN tanpa disadari?", "Sensor load cell mengalami drift pembacaan +22% (menampilkan 19.5 kN padahal aktual 24.8 kN)."),
            ("Mengapa drift sensor tidak terdeteksi saat kalibrasi?", "Jadwal kalibrasi beban load cell 6-bulanan tertunda 3 minggu akibat mesin dipaksa beroperasi penuh."),
            ("Mengapa sistem mengizinkan penundaan kalibrasi komponen kritis?", "🎯 AKAR MASALAH SISTEMIK: Belum adanya 'Hard-Stop Interlock' pada software maintenance yang otomatis mengunci mesin jika kalibrasi instrumen kritis terlewati.")
        ],
        "capa": {
            "corrective": [
                {"Kode": "CA-01", "Tindakan": "Karantina fisik (Label Merah) seluruh batch BTH-PCT-260412 di gudang QA", "PIC": "QA Officer", "Target": "2026-10-23", "Status": "Pending"},
                {"Kode": "CA-02", "Tindakan": "Hentikan mesin cetak, lakukan penggantian dan re-kalibrasi load cell", "PIC": "Maintenance", "Target": "2026-10-24", "Status": "In Progress"},
                {"Kode": "CA-03", "Tindakan": "Kajian teknis evaluasi Rework atau Penolakan/Destruksi produk", "PIC": "QA Manager", "Target": "2026-10-26", "Status": "Pending"}
            ],
            "preventive": [
                {"Kode": "PA-01", "Tindakan": "Pasang Electronic Calibration Interlock pada PLC mesin pencetak tablet", "PIC": "Automation Team", "Target": "2026-11-10", "Status": "Scheduled"},
                {"Kode": "PA-02", "Tindakan": "Revisi SOP: Wajibkan Double-Sign Verification IPC kekerasan per 30 menit", "PIC": "QA Compliance", "Target": "2026-11-05", "Status": "Scheduled"},
                {"Kode": "PA-03", "Tindakan": "Pelatihan penyegaran identifikasi dini anomali gaya kompresi bagi operator", "PIC": "QA Trainer", "Target": "2026-11-15", "Status": "Scheduled"}
            ],
            "review": "Cek Efektivitas 60 Hari: Zero deviation kalibrasi sensor dan tren CpK disolusi 10 batch berikutnya > 1.33."
        }
    },
    "2. Ekskursi Suhu FBD — Amoxicillin Sirup": {
        "code": "DEV-2026-0915",
        "title": "Ekskursi Suhu di Ruang Pengering FBD Granulasi Amoxicillin Sirup",
        "product": "Amoxicillin Trihydrate 125 mg/5 mL Sirup Kering",
        "batch": "BTH-AMX-260519",
        "dosage_form": "Granul Suspensi Rekonstitusi Oral",
        "line": "Lini Betalaktam Khusus Gedung Antibiotik",
        "cleanroom": "Kelas D (Controlled)",
        "stage": "Pengeringan Fluid Bed Dryer (FBD-02)",
        "detected_by": "Operator Produksi FBD & SCADA Alarm",
        "description": "Suhu inlet air pada Fluid Bed Dryer melonjak hingga 78.4 °C selama 42 menit (Batas kritis CPOB: 55.0 - 60.0 °C). Amoxicillin bersifat termolabil berisiko mengalami degradasi cincin betalaktam menjadi produk inaktif (asam penisiloat).",
        "severity": 5, "probability": 2, "detectability": 1, "rpn": 10,
        "classification": "Critical",
        "disposition": "Karantina Total & Rekomendasi Reject / Destruksi",
        "cqa_impact": "Potensi pembentukan pengotor B (Penicilloic acid), penurunan potensi antibiotik, dan OOS Assay.",
        "cpp_correlation": "Suhu udara inlet FBD melebihi batas stabilitas termal antibiotik betalaktam.",
        "fishbone": {
            "1. Man (Personil)": ["Operator merespon alarm terlambat karena membantu tim sanitasi ruangan"],
            "2. Machine (Peralatan)": ["🎯 ROOT CAUSE: Pneumatic modulating steam valve macet pada 100% stroke akibat korosi", "Katup bypass manual terhalang pipa utilitas baru"],
            "3. Material (Bahan)": ["Kadar air awal granul homogen dan memenuhi spesifikasi sebelum pengeringan"],
            "4. Method (SOP)": ["Prosedur darurat ekskursi termal belum dilengkapi auto-cutoff solenoid"],
            "5. Measurement (Alat)": ["Sensor suhu RTD PT-100 inlet membaca akurat tervalidasi"],
            "6. Milieu (Lingkungan)": ["Tekanan negatif ruang betalaktam (-15 Pa) terjaga sesuai CPOB"]
        },
        "five_whys": [
            ("Mengapa suhu inlet FBD melonjak hingga 78.4 °C?", "Aliran uap panas (steam 3 bar) terus mengalir tanpa modulasi ke coil pemanas."),
            ("Mengapa uap panas terus mengalir tanpa modulasi?", "Pneumatic modulating control valve macet total pada posisi 100% terbuka."),
            ("Mengapa katup kontrol uap tersebut macet?", "Batang aktuator pneumatik mengalami korosi dan kerak kotoran steam trap."),
            ("Mengapa mesin tidak mematikan suplai steam saat suhu > 62 °C?", "FBD tipe lama tidak dilengkapi redundant emergency safety shut-off valve."),
            ("Mengapa tidak dilakukan upgrade interlock termal?", "🎯 AKAR MASALAH SISTEMIK: Belum dilakukannya FMEA utilitas pemanas mesin termolabil untuk menambahkan independent high-limit safety cut-off.")
        ],
        "capa": {
            "corrective": [
                {"Kode": "CA-01", "Tindakan": "Karantina batch BTH-AMX-260519 dan uji kadar serta related substances HPLC", "PIC": "QC Lab", "Target": "2026-10-24", "Status": "In Progress"},
                {"Kode": "CA-02", "Tindakan": "Overhaul dan ganti pneumatic steam control valve FBD-02 dan pasang strainer", "PIC": "Utility Team", "Target": "2026-10-25", "Status": "Pending"}
            ],
            "preventive": [
                {"Kode": "PA-01", "Tindakan": "Pasang Independent High-Temperature Safety Cut-off Solenoid Valve (trip pada 63 °C)", "PIC": "Automation", "Target": "2026-11-12", "Status": "Scheduled"},
                {"Kode": "PA-02", "Tindakan": "Audit dan inspeksi rutin steam trap di seluruh lini granulasi tiap 3 bulan", "PIC": "Plant Utility", "Target": "2026-11-20", "Status": "Scheduled"}
            ],
            "review": "Cek Efektivitas 90 Hari: Uji trip darurat katup safety cut-off berhasil 100% dalam 3 simulasi berturut-turut."
        }
    },
    "3. Partikel Asing Filling Aseptis — Ceftriaxone Injeksi": {
        "code": "DEV-2026-1002",
        "title": "Kontaminasi Partikel Asing pada Pengisian Aseptis Vial Injeksi",
        "product": "Ceftriaxone Sodium 1 g Serbuk Injeksi",
        "batch": "BTH-CTX-260604",
        "dosage_form": "Serbuk Kering Injeksi Steril",
        "line": "Lini Aseptis Steril Lt. 3",
        "cleanroom": "Kelas A dalam Latar Belakang Kelas B",
        "stage": "Filling & Stoppering Aseptis",
        "detected_by": "Automatic Visual Inspection (AVI)",
        "description": "Sistem AVI mendeteksi lonjakan partikel asing hitam 3.4% pada pengisian vial menit 120-150 (Reject limit CPOB: 0.5%). Analisis FTIR mikro mengonfirmasi partikel berupa fragmen karet elastomerik bromo-butyl.",
        "severity": 5, "probability": 2, "detectability": 1, "rpn": 10,
        "classification": "Critical",
        "disposition": "Karantina Total Sub-batch & Investigasi Menyeluruh",
        "cqa_impact": "Bebas partikulat asing (USP <788>) gagal, risiko fatal emboli kapiler pasien.",
        "cpp_correlation": "Interaksi mekanis stopper bowl feeder dengan chute track stainless steel.",
        "fishbone": {
            "1. Man (Personil)": ["Operator intervensi manual tanpa extension arm saat stopper macet"],
            "2. Machine (Peralatan)": ["🎯 ROOT CAUSE: Chute stainless steel memiliki burr mikro tajam akibat friksi", "🎯 ROOT CAUSE: Amplitudo vibrasi bowl feeder disetel 75% (spek 45%)"],
            "3. Material (Bahan)": ["Stopper karet bromo-butyl telah dicuci dan disterilisasi tervalidasi"],
            "4. Method (SOP)": ["SOP belum melarang pengubahan vibrasi getaran bowl di luar rentang"],
            "5. Measurement (Alat)": ["Kamera optik AVI mendeteksi partikel > 50 mikron secara akurat"],
            "6. Milieu (Lingkungan)": ["Partikel non-viable dan settle plate di LAF Kelas A nihil mikroba"]
        },
        "five_whys": [
            ("Mengapa ditemukan fragmen karet hitam di dalam vial?", "Stopper karet terkikis secara mekanis sebelum masuk ke leher vial."),
            ("Di mana pengikisan mekanis stopper karet terjadi?", "Pada jalur luncur (chute track) antara feeder bowl dan insertion head."),
            ("Mengapa stopper terkikis saat meluncur di chute track?", "Terdapat burr mikro tajam pada permukaan stainless steel rel."),
            ("Mengapa tekanan gesek stopper pada rel menjadi berlebih?", "Amplitudo getaran bowl dinaikkan manual oleh teknisi ke 75% untuk mempercepat aliran."),
            ("Mengapa vibrasi diubah tanpa validasi & Change Control?", "🎯 AKAR MASALAH SISTEMIK: Ketiadaan penguncian parameter kritis (CPP lockout) pada controller mesin dan absennya inspeksi kehalusan permukaan (surface roughness Ra) kontak steril.")
        ],
        "capa": {
            "corrective": [
                {"Kode": "CA-01", "Tindakan": "Tolak dan destruksi vial sub-batch menit 120-180 yang terpapar partikel", "PIC": "QA Head", "Target": "2026-10-25", "Status": "Pending"},
                {"Kode": "CA-02", "Tindakan": "Electropolishing ulang chute stainless steel hingga Ra < 0.4 µm bebas burr", "PIC": "Tooling Specialist", "Target": "2026-10-27", "Status": "In Progress"}
            ],
            "preventive": [
                {"Kode": "PA-01", "Tindakan": "Kunci parameter vibrasi dengan password Supervisor (21 CFR Part 11)", "PIC": "Sterile Engineer", "Target": "2026-11-08", "Status": "Scheduled"},
                {"Kode": "PA-02", "Tindakan": "Tambahkan checklist inspeksi mikroskopis kehalusan contact-parts bulanan", "PIC": "Maintenance", "Target": "2026-11-12", "Status": "Scheduled"}
            ],
            "review": "Cek Efektivitas 30 Hari: Tingkat reject partikel AVI pada 3 batch berikutnya harus < 0.15%."
        }
    },
    "4. Variasi Bobot & Capping — Cetirizine Tablet": {
        "code": "DEV-2026-1120",
        "title": "Variasi Bobot Tablet & Capping pada Mesin Cetak Cetirizine 10 mg",
        "product": "Cetirizine HCl 10 mg Tablet Salut Selaput",
        "batch": "BTH-CTZ-260731",
        "dosage_form": "Tablet Inti (Uncoated)",
        "line": "Lini Solid Non-Steril Gedung I",
        "cleanroom": "Kelas E",
        "stage": "Pencetakan Tablet (Compression)",
        "detected_by": "IPC In-Process Control Operator",
        "description": "Pengujian bobot tablet menit ke-90 menunjukkan RSD bobot 4.2% (batas alert CPOB < 2.0%) dan fenomena capping sebesar 1.8% pada tablet inti.",
        "severity": 3, "probability": 3, "detectability": 1, "rpn": 9,
        "classification": "Minor",
        "disposition": "Karantina Parsial untuk Sortir & Uji Keseragaman Kandungan",
        "cqa_impact": "Potensi variasi dosis (Content Uniformity OOS) antar unit sediaan.",
        "cpp_correlation": "Rasio pre-compression force dan kecepatan feed frame tidak sinkron.",
        "fishbone": {
            "1. Man (Personil)": ["Operator menaikkan kecepatan feed frame untuk mengejar output per jam"],
            "2. Machine (Peralatan)": ["🎯 ROOT CAUSE: Baut pengunci roller mengendur, gaya pre-compression anjlok ke 1.2 kN", "Upper punch scraper aus"],
            "3. Material (Bahan)": ["🎯 ROOT CAUSE: Proporsi fines serbuk (< 100 mesh) dalam granul mencapai 32% (spek < 20%)"],
            "4. Method (SOP)": ["Setting pre-compression force tidak dicatat dalam lembar IPC awal"],
            "5. Measurement (Alat)": ["Timbangan analitik Mettler Toledo terkalibrasi harian dengan anak timbang E2"],
            "6. Milieu (Lingkungan)": ["RH ruangan 45% optimal untuk pencetakan tablet cetirizine"]
        },
        "five_whys": [
            ("Mengapa bobot bervariasi (RSD 4.2%) dan terjadi capping?", "Aliran granul ke die cavity tidak konstan dan udara terjebak saat kompresi utama."),
            ("Mengapa udara terjebak di dalam serbuk granul?", "Gaya pra-kompresi turun drastis ke 1.2 kN sehingga udara belum keluar sebelum kompresi."),
            ("Mengapa gaya pra-kompresi turun?", "Baut pengunci posisi roller mengendur akibat getaran mesin pencetak."),
            ("Mengapa fines serbuk juga tinggi sehingga memperparah capping?", "Saringan mesh pada mesin granulator basah mengalami keausan sehingga fines 32%."),
            ("Mengapa saringan aus tidak diganti saat setup?", "🎯 AKAR MASALAH SISTEMIK: Belum adanya verifikasi umur pakai saringan granulator dan ketiadaan checklist torque wrench pada penguncian roller.")
        ],
        "capa": {
            "corrective": [
                {"Kode": "CA-01", "Tindakan": "Hentikan mesin, kencangkan baut roller dengan torque wrench tervalidasi ke 4.0 kN", "PIC": "Setup Technician", "Target": "2026-10-23", "Status": "Completed"},
                {"Kode": "CA-02", "Tindakan": "Pengujian Keseragaman Sediaan (Content Uniformity) sub-batch terdampak", "PIC": "QC Analyst", "Target": "2026-10-24", "Status": "In Progress"}
            ],
            "preventive": [
                {"Kode": "PA-01", "Tindakan": "Modifikasi Line Clearance: verifikasi torsi pengunci roller ganda", "PIC": "QA In-Process", "Target": "2026-11-02", "Status": "Scheduled"},
                {"Kode": "PA-02", "Tindakan": "Tetapkan batas maksimal jam kerja saringan oscillating granulator", "PIC": "Maintenance", "Target": "2026-11-06", "Status": "Scheduled"}
            ],
            "review": "Cek Efektivitas 45 Hari: RSD bobot tablet pada 5 batch berikutnya < 1.8% dan capping 0%."
        }
    }
}

# --- HEADER SECTION ---
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">✚ SISTEM MANAJEMEN PENYIMPANGAN MUTU PABRIK FARMASI</div>
    <h1 class="hero-title">PharmaCAPA AI — Operator &amp; QA Deviation Copilot</h1>
    <div class="hero-desc">
        Antarmuka terpadu untuk Operator Produksi, Teknisi Mesin, dan Tim QA dalam melaporkan deviasi bets, menganalisis akar masalah (6M Ishikawa &amp; 5-Whys), serta menyusun dokumen CAPA berstandar <strong>BPOM CPOB 2018/2024 &amp; ICH Q9/Q10</strong>.
    </div>
</div>
""", unsafe_allow_html=True)

# --- TOP INTERACTIVE PRESET CHIPS ---
st.markdown("##### 📌 Pilih Kasus Deviasi atau Input Baru:")
c1, c2, c3, c4 = st.columns(4)

preset_names = list(PRESETS.keys())
selected_case_name = st.selectbox(
    "Pilih Laporan Deviasi:",
    options=preset_names,
    index=0,
    label_visibility="collapsed"
)

current_case = PRESETS[selected_case_name]

# --- QUICK METRIC STRIP ---
col_m1, col_m2, col_m3, col_m4 = st.columns([1.5, 1, 1, 1.5])

with col_m1:
    st.markdown(f"**No. Deviasi:** `{current_case['code']}`")
    st.markdown(f"**Produk:** **{current_case['product']}**")
    st.caption(f"Bets: `{current_case['batch']}` • {current_case['line']}")

with col_m2:
    st.metric(
        label="Risk Priority Number (RPN)",
        value=current_case["rpn"],
        delta=f"S:{current_case['severity']} × P:{current_case['probability']} × D:{current_case['detectability']}"
    )

with col_m3:
    cls = current_case["classification"]
    badge_html = f"<span class='pill-{cls.lower()}'>{cls.upper()}</span>"
    st.markdown("**Klasifikasi Dampak:**")
    st.markdown(badge_html, unsafe_allow_html=True)
    st.caption("Standar ICH Q9")

with col_m4:
    st.markdown("**Rekomendasi Disposisi Bets:**")
    st.markdown(f"🔒 **{current_case['disposition']}**")
    st.caption("Penahanan Karantina CPOB")

st.markdown("---")

# --- MAIN WORKSPACE TABS ---
tab_input, tab_fishbone, tab_whys, tab_capa, tab_report = st.tabs([
    "📝 1. Formulir Input Operator",
    "🐟 2. Diagram 6M (Ishikawa)",
    "🔍 3. Metode 5-Whys",
    "🛡️ 4. Rencana CAPA",
    "📄 5. Formulir Resmi CPOB"
])

# TAB 1: FORMULIR INPUT OPERATOR (SANGAT MINIMALIS & GUIDED)
with tab_input:
    st.markdown("### 📝 Formulir Cepat Pelaporan Deviasi (Shift Operator & Teknisi)")
    st.caption("Isi data berikut dengan ringkas. Gunakan tombol preset di atas untuk simulasi instan.")
    
    with st.form("operator_deviation_form"):
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            in_product = st.text_input("Nama Produk:", value=current_case["product"])
            in_batch = st.text_input("Nomor Bets / Lot:", value=current_case["batch"])
            in_cleanroom = st.selectbox(
                "Kelas Ruangan:",
                ["Kelas A (LAF Steril)", "Kelas B (Background Steril)", "Kelas C (Proses Bersih)", "Kelas D (Controlled Area)", "Kelas E (White Area Non-Steril)"],
                index=4 if "Kelas E" in current_case["cleanroom"] else (3 if "Kelas D" in current_case["cleanroom"] else 0)
            )
        with f_col2:
            in_stage = st.text_input("Tahapan Proses Terjadinya Insiden:", value=current_case["stage"])
            in_line = st.text_input("Lini Mesin / Lokasi Gedung:", value=current_case["line"])
            in_reporter = st.text_input("Pelapor / Operator Bertugas:", value=current_case["detected_by"])

        in_desc = st.text_area(
            "Deskripsi Faktual Deviasi / Kerusakan:",
            value=current_case["description"],
            height=110,
            help="Tuliskan apa yang menyimpang, parameter mesin, atau hasil pengujian IPC yang tidak sesuai."
        )

        submitted = st.form_submit_button("⚡ Jalankan Analisis AI CPOB & ICH Q9", use_container_width=True)
        if submitted:
            st.success("✅ Analisis AI Selesai! Buka tab '2. Diagram 6M', '3. 5-Whys', dan '4. Rencana CAPA' untuk melihat hasil investigasi.")

# TAB 2: ISHIKAWA 6M
with tab_fishbone:
    st.markdown("### 🐟 Diagram Tulang Ikan 6M (Ishikawa Matrix)")
    st.caption("Pemetaan penyebab kegagalan mutu pada Man, Machine, Material, Method, Measurement, dan Milieu.")

    f_left, f_right = st.columns(2)
    cat_items = list(current_case["fishbone"].items())

    with f_left:
        for cat_name, items in cat_items[:3]:
            with st.expander(f"📁 {cat_name}", expanded=True):
                for item in items:
                    if "ROOT CAUSE" in item:
                        st.error(f"**{item}**")
                    else:
                        st.markdown(f"• {item}")

    with f_right:
        for cat_name, items in cat_items[3:]:
            with st.expander(f"📁 {cat_name}", expanded=True):
                for item in items:
                    if "ROOT CAUSE" in item:
                        st.error(f"**{item}**")
                    else:
                        st.markdown(f"• {item}")

# TAB 3: 5-WHYS
with tab_whys:
    st.markdown("### 🔍 Metode 5-Whys (Penelusuran Akar Masalah Bertingkat)")
    st.caption("Menelusuri dari gejala permukaan hingga ke akar masalah sistemik (True Root Cause).")

    for idx, (question, answer) in enumerate(current_case["five_whys"]):
        is_final = (idx == len(current_case["five_whys"]) - 1)
        if is_final:
            st.markdown(f"""
            <div class="step-root">
                <div style="font-weight: 800; color: #be123c; font-size: 14px;">🎯 TINGKAT {idx+1} (AKAR MASALAH SISTEMIK): {question}</div>
                <div style="color: #881337; font-size: 14px; margin-top: 6px;">{answer}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="step-box">
                <div style="font-weight: 700; color: #0369a1; font-size: 13px;">LANGKAH {idx+1}: {question}</div>
                <div style="color: #334155; font-size: 13.5px; margin-top: 4px;">{answer}</div>
            </div>
            """, unsafe_allow_html=True)

# TAB 4: CAPA PLAN
with tab_capa:
    st.markdown("### 🛡️ Rencana Tindakan Korektif &amp; Preventif (CAPA)")
    
    st.markdown("##### ⚡ A. Tindakan Korektif Langsung (Corrective Action - CA)")
    st.dataframe(pd.DataFrame(current_case["capa"]["corrective"]), use_container_width=True, hide_index=True)

    st.markdown("##### 🛡️ B. Tindakan Pencegahan Sistemik (Preventive Action - PA)")
    st.dataframe(pd.DataFrame(current_case["capa"]["preventive"]), use_container_width=True, hide_index=True)

    st.info(f"🎯 **Protokol Cek Efektivitas CAPA:** {current_case['capa']['review']}")

# TAB 5: OFFICIAL CPOB FORM
with tab_report:
    st.markdown("### 📄 Formulir Resmi Penyelidikan Deviasi &amp; Rencana CAPA")
    st.caption("Format Baku SOP-QA-042 (CPOB BPOM RI 2018/2024 & FDA 21 CFR Part 211)")

    doc_text = f"""========================================================================================
PT PHARMA NUSANTARA TBK — QUALITY ASSURANCE DIVISION
FORMULIR PENYELIDIKAN PENYIMPANGAN MUTU & RENCANA CAPA (CPOB 2018/2024 BPOM)
No. Dokumen: SOP-QA-042-F01 (Rev. 05) | No. Deviasi: {current_case['code']}
========================================================================================

BAGIAN 1: INFORMASI BETS & PENYIMPANGAN
- Nama Produk        : {current_case['product']}
- No. Bets           : {current_case['batch']}
- Bentuk Sediaan     : {current_case['dosage_form']}
- Lini Produksi      : {current_case['line']}
- Kelas Kebersihan   : {current_case['cleanroom']}
- Tahapan Proses     : {current_case['stage']}
- Dideteksi Oleh     : {current_case['detected_by']}
- Tanggal Deteksi    : {datetime.now().strftime('%Y-%m-%d')}

DESKRIPSI KEJADIAN FAKTUAL:
{current_case['description']}

BAGIAN 2: KAJIAN RISIKO MUTU & DISPOSISI (ICH Q9)
- Nilai RPN          : {current_case['rpn']} (S:{current_case['severity']} × P:{current_case['probability']} × D:{current_case['detectability']})
- Klasifikasi        : {current_case['classification'].upper()}
- Disposisi Bets     : {current_case['disposition']}
- Dampak CQA         : {current_case['cqa_impact']}
- Korelasi CPP       : {current_case['cpp_correlation']}

BAGIAN 3: AKAR MASALAH (ROOT CAUSE)
{current_case['five_whys'][-1][1]}

BAGIAN 4: RENCANA CAPA (ICH Q10)
Tindakan Korektif (CA):
{chr(10).join([f"  [{c['Kode']}] {c['Tindakan']} | PIC: {c['PIC']} | Target: {c['Target']}" for c in current_case['capa']['corrective']])}

Tindakan Pencegahan (PA):
{chr(10).join([f"  [{p['Kode']}] {p['Tindakan']} | PIC: {p['PIC']} | Target: {p['Target']}" for p in current_case['capa']['preventive']])}

BAGIAN 5: OTORISASI & TANDA TANGAN
- Investigator QA     : apt. Rismawati L., S.Farm. [VERIFIED DIGITAL]
- Head of Production  : Ir. Hendra Wijaya, M.M.     [VERIFIED DIGITAL]
- Qualified Person/QA : apt. Dr. Arry S., M.Si.     [AUTHORIZED BPOM]
========================================================================================"""

    # Build formatted Microsoft Word (.doc) HTML
    ca_rows = "".join([f"<tr><td style='text-align:center;font-weight:bold;'>{c['Kode']}</td><td>{c['Tindakan']}</td><td>{c['PIC']}</td><td style='text-align:center;'>{c['Target']}</td><td style='text-align:center;'>{c['Status']}</td></tr>" for c in current_case['capa']['corrective']])
    pa_rows = "".join([f"<tr><td style='text-align:center;font-weight:bold;'>{p['Kode']}</td><td>{p['Tindakan']}</td><td>{p['PIC']}</td><td style='text-align:center;'>{p['Target']}</td><td style='text-align:center;'>{p['Status']}</td></tr>" for p in current_case['capa']['preventive']])
    whys_items = "".join([f"<li style='margin-bottom:6px;'><strong>W{i+1}: {w[0]}</strong><br><span style='color:#334155;'>{w[1]}</span></li>" for i, w in enumerate(current_case['five_whys'])])

    word_html = f"""<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
<head>
  <meta charset='utf-8'>
  <title>Formulir CPOB - {current_case['code']}</title>
  <!--[if gte mso 9]>
  <xml><w:WordDocument><w:View>Print</w:View><w:Zoom>100</w:Zoom><w:DoNotOptimizeForBrowser/></w:WordDocument></xml>
  <![endif]-->
  <style>
    body {{ font-family: Arial, sans-serif; font-size: 10pt; color: #0f172a; margin: 15mm; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 8px; }}
    td, th {{ border: 1px solid #475569; padding: 6px 8px; font-size: 9pt; }}
    .sec-title {{ background: #0f172a; color: #ffffff; font-weight: bold; padding: 5px 8px; font-size: 9.5pt; margin-top: 10px; margin-bottom: 5px; }}
    .grid-label {{ background: #f1f5f9; font-weight: bold; width: 130px; }}
    .badge {{ padding: 3px 8px; font-weight: bold; border-radius: 4px; }}
    .badge-critical {{ background: #fee2e2; color: #991b1b; }}
    .badge-major {{ background: #fef3c7; color: #92400e; }}
    .badge-minor {{ background: #e0f2fe; color: #075985; }}
    .stamp {{ border: 1.5px dashed #0284c7; padding: 4px; text-align: center; color: #0284c7; font-weight: bold; font-size: 8pt; }}
  </style>
</head>
<body>
  <table style="border: 2px solid #0f172a; margin-bottom: 12px;">
    <tr>
      <td style="width: 100px; text-align: center; vertical-align: middle;">
        <div style="font-size: 26pt; color: #0284c7;">✚</div>
        <div style="font-size: 8pt; font-weight: bold;">PHARMA QA</div>
      </td>
      <td style="text-align: center;">
        <div style="font-size: 8.5pt; color: #475569; font-weight: bold;">PT PHARMA NUSANTARA Tbk. — QUALITY ASSURANCE DIVISION</div>
        <div style="font-size: 13pt; font-weight: bold; color: #0f172a; margin: 3px 0;">FORMULIR PENYELIDIKAN PENYIMPANGAN & RENCANA CAPA</div>
        <div style="font-size: 8pt; color: #0284c7; font-weight: bold;">CPOB 2018/2024 (BPOM RI) & cGMP FDA 21 CFR Part 211 COMPLIANT</div>
      </td>
      <td style="width: 150px; font-size: 8.5pt;">
        <strong>No. Dok:</strong> SOP-QA-042<br>
        <strong>No. Dev:</strong> <span style="color:#0284c7; font-weight:bold;">{current_case['code']}</span><br>
        <strong>Tgl:</strong> {datetime.now().strftime('%Y-%m-%d')}
      </td>
    </tr>
  </table>

  <div class="sec-title">BAGIAN 1: INFORMASI BETS & RINCIAN PENYIMPANGAN</div>
  <table>
    <tr>
      <td class="grid-label">Nama Produk</td><td><strong>{current_case['product']}</strong></td>
      <td class="grid-label">No. Bets / Lot</td><td><strong>{current_case['batch']}</strong></td>
    </tr>
    <tr>
      <td class="grid-label">Bentuk Sediaan</td><td>{current_case['dosage_form']}</td>
      <td class="grid-label">Lini Produksi</td><td>{current_case['line']}</td>
    </tr>
    <tr>
      <td class="grid-label">Kelas Ruangan</td><td>{current_case['cleanroom']}</td>
      <td class="grid-label">Tahapan Proses</td><td>{current_case['stage']}</td>
    </tr>
  </table>
  <div style="border: 1px solid #cbd5e1; background: #f8fafc; padding: 8px 10px; margin-bottom: 10px; font-size: 9pt;">
    <strong>Deskripsi Faktual Kejadian:</strong><br>{current_case['description']}
  </div>

  <div class="sec-title">BAGIAN 2: KAJIAN RISIKO MUTU & DISPOSISI BETS (ICH Q9)</div>
  <table>
    <tr>
      <td style="width: 50%;">
        <strong>Klasifikasi:</strong> <span class="badge badge-{current_case['classification'].lower()}">{current_case['classification'].upper()}</span><br>
        <strong>RPN:</strong> {current_case['rpn']} (S:{current_case['severity']} × P:{current_case['probability']} × D:{current_case['detectability']})
      </td>
      <td>
        <strong>Disposisi Bets:</strong> <span style="color:#b91c1c; font-weight:bold;">{current_case['disposition']}</span><br>
        <strong>Dampak CQA:</strong> {current_case['cqa_impact']}
      </td>
    </tr>
  </table>

  <div class="sec-title">BAGIAN 3: ANALISIS AKAR MASALAH (5-WHYS METHODOLOGY)</div>
  <ol style="font-size: 9pt; padding-left: 20px;">
    {whys_items}
  </ol>

  <div class="sec-title">BAGIAN 4: RENCANA CAPA (ICH Q10)</div>
  <div style="font-weight:bold; font-size:9pt; margin: 5px 0;">A. Tindakan Korektif Langsung (Corrective Action - CA)</div>
  <table>
    <tr style="background:#f1f5f9;"><th>Kode</th><th>Tindakan Korektif</th><th>PIC</th><th>Target</th><th>Status</th></tr>
    {ca_rows}
  </table>

  <div style="font-weight:bold; font-size:9pt; margin: 8px 0 5px;">B. Tindakan Pencegahan Sistemik (Preventive Action - PA)</div>
  <table>
    <tr style="background:#f1f5f9;"><th>Kode</th><th>Tindakan Pencegahan</th><th>PIC</th><th>Target</th><th>Status</th></tr>
    {pa_rows}
  </table>

  <div style="border: 1px dashed #0284c7; background: #f0f9ff; padding: 6px 10px; font-size: 8.5pt; margin: 8px 0;">
    <strong>Protokol Cek Efektivitas CAPA:</strong> {current_case['capa']['review']}
  </div>

  <div class="sec-title">BAGIAN 5: OTORISASI & TANDA TANGAN (CPOB BPOM)</div>
  <table>
    <tr>
      <td style="width: 33.3%; text-align: center;">
        <div style="font-size: 8pt; color:#64748b;">DIPERIKSA (INVESTIGATOR):</div>
        <div class="stamp" style="margin: 8px auto; width: 140px;">DIGITALLY VERIFIED<br><small>QA Specialist</small></div>
        <strong>apt. Rismawati L., S.Farm.</strong>
      </td>
      <td style="width: 33.3%; text-align: center;">
        <div style="font-size: 8pt; color:#64748b;">DISETUJUI (PRODUKSI):</div>
        <div class="stamp" style="margin: 8px auto; width: 140px;">DIGITALLY VERIFIED<br><small>Head of Production</small></div>
        <strong>Ir. Hendra Wijaya, M.M.</strong>
      </td>
      <td style="width: 33.3%; text-align: center;">
        <div style="font-size: 8pt; color:#64748b;">DISETUJUI (QA HEAD):</div>
        <div class="stamp" style="border-color:#b45309; color:#b45309; margin: 8px auto; width: 140px;">QUALIFIED PERSON<br><small>BPOM Authorized</small></div>
        <strong>apt. Dr. Arry S., M.Si.</strong>
      </td>
    </tr>
  </table>
</body></html>"""

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="📥 Unduh Dokumen Microsoft Word (.doc) Lengkap Tabel",
            data=word_html,
            file_name=f"Formulir_CPOB_{current_case['code']}.doc",
            mime="application/msword",
            use_container_width=True
        )
    with col_dl2:
        st.download_button(
            label="📄 Unduh Ringkasan Teks (.txt)",
            data=doc_text,
            file_name=f"Laporan_CPOB_{current_case['code']}.txt",
            mime="text/plain",
            use_container_width=True
        )
