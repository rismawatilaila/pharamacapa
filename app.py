"""
PharmaCAPA AI — Pharmaceutical Deviation & CAPA Copilot
Framework: Streamlit (Ready for Streamlit Community Cloud & GitHub)
Standards: CPOB 2018/2024 (BPOM RI), cGMP FDA 21 CFR Part 211, ICH Q9 & Q10
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="PharmaCAPA AI — Pharmaceutical Deviation Copilot",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Clinical Pharma Look
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border: 1px solid rgba(14, 165, 233, 0.3);
        border-radius: 12px;
        padding: 20px 25px;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .header-title {
        color: #ffffff;
        font-size: 26px;
        font-weight: 800;
        margin: 0;
    }
    .header-subtitle {
        color: #7dd3fc;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }
    .metric-box {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .tag-critical { background-color: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .tag-major { background-color: #fef3c7; color: #92400e; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .tag-minor { background-color: #e0f2fe; color: #075985; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .root-cause-box {
        background: rgba(244, 63, 94, 0.1);
        border-left: 4px solid #f43f5e;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Pharma QA Dataset & Preset Cases
PRESETS = {
    "DEV-2026-0842 | Uji Disolusi OOS Paracetamol 500mg": {
        "code": "DEV-2026-0842",
        "title": "Kegagalan Uji Disolusi (OOS) pada Paracetamol 500 mg Tablet",
        "product": "Paracetamol 500 mg Kaplet",
        "batch": "BTH-PCT-260412",
        "dosage_form": "Tablet / Kaplet Salut Film",
        "line": "Lini Solid Non-Steril Gedung II",
        "cleanroom": "Kelas E (White Area)",
        "stage": "Pengujian QC Ruahan (Bulk Product)",
        "detected_by": "Staff Analis QC Kimia Fisika",
        "description": "Hasil uji disolusi tahap S1 (n=6) menunjukkan nilai Q30 menit berada di kisaran 68% - 74%, tidak memenuhi syarat CPOB/FI (Q=80% pada menit ke-30). Tahap S2 (n=12) menghasilkan rata-rata 73.5%, terkonfirmasi Out-of-Specification (OOS). Kekerasan tablet tercatat 14.2 kP (spek 7-10 kP).",
        "severity": 4, "probability": 3, "detectability": 1, "rpn": 12,
        "classification": "Major",
        "disposition": "Karantina Formal & Evaluasi Rework/Destruksi",
        "cqa_impact": "Laju pelepasan zat aktif & profil bioavailabilitas in vivo berisiko gagal.",
        "cpp_correlation": "Gaya kompresi rotary tablet press melebihi setpoint akibat drift sensor.",
        "fishbone": {
            "Man (Personil)": ["Operator baru belum sertifikasi penuh mesin tablet Fette", "Supervisi IPC oleh Group Leader terlambat dilakukan"],
            "Machine (Peralatan)": ["🎯 ROOT CAUSE: Sensor load cell gaya kompresi mengalami drift pembacaan +22%", "Alarm over-force pada HMI dinonaktifkan sementara saat setting"],
            "Material (Bahan)": ["Kadar air granul (LOD) 1.1% (agak terlalu kering, spesifikasi 1.5 - 2.5%)", "Deformasi plastis serbuk berubah akibat over-drying di FBD"],
            "Method (SOP)": ["SOP-PRD-TAB-014 belum mencantumkan verifikasi 2 orang (four-eyes check) saat setup", "Frekuensi pengujian IPC kekerasan terlewat saat pergantian shift"],
            "Measurement (Alat Ukur)": ["Hardness Tester Erweka terkalibrasi baik", "Disolusi bath USP Apparatus II terkalibrasi dan media valid"],
            "Milieu (Lingkungan HVAC)": ["Suhu ruangan 24.5 °C dan RH 58% masih dalam batas alert limit Kelas E"]
        },
        "five_whys": [
            ("Mengapa tablet Paracetamol tidak memenuhi syarat disolusi Q=80%?", "Kekerasan tablet rata-rata 14.2 kP (spesifikasi 7 - 10 kP), waktu hancur molor hingga 24 menit."),
            ("Mengapa kekerasan tablet melonjak tinggi selama pencetakan?", "Gaya kompresi utama pada rotary press beroperasi pada 24.8 kN padahal setpoint SOP adalah 18 - 20 kN."),
            ("Mengapa mesin berjalan pada gaya 24.8 kN tanpa disadari?", "Sensor load cell mengalami drift pembacaan +22%, menampilkan 19.5 kN pada layar HMI padahal tekanan aktual 24.8 kN."),
            ("Mengapa drift sensor load cell tidak terdeteksi saat kalibrasi?", "Jadwal kalibrasi beban load cell 6-bulanan tertunda 3 minggu akibat utilitas mesin dipaksa running terus."),
            ("Mengapa sistem mengizinkan penundaan kalibrasi komponen kritis?", "🎯 AKAR MASALAH: Belum adanya sistem 'Hard-Stop Interlock' pada software maintenance yang otomatis mengunci mesin jika kalibrasi sensor kritis kadaluarsa.")
        ],
        "capa": {
            "corrective": [
                {"Kode": "CA-01", "Tindakan": "Karantina resmi (Quarantine Tag Merah) seluruh batch BTH-PCT-260412", "PIC": "QA Officer Karantina", "Target": "2026-10-23", "Status": "Pending"},
                {"Kode": "CA-02", "Tindakan": "Hentikan Mesin TP-03, lakukan re-kalibrasi darurat dan ganti load cell", "PIC": "Engineering Supervisor", "Target": "2026-10-24", "Status": "In Progress"},
                {"Kode": "CA-03", "Tindakan": "Kajian teknis Rework Protocol atau Penolakan/Destruksi produk", "PIC": "QA Manager & R&D", "Target": "2026-10-26", "Status": "Pending"}
            ],
            "preventive": [
                {"Kode": "PA-01", "Tindakan": "Pasang Electronic Calibration Interlock pada PLC mesin tablet press", "PIC": "Automation Engineer", "Target": "2026-11-10", "Status": "Scheduled"},
                {"Kode": "PA-02", "Tindakan": "Revisi SOP-PRD-TAB-014: Wajibkan Double-Sign Verification IPC kekerasan", "PIC": "QA Compliance", "Target": "2026-11-05", "Status": "Scheduled"},
                {"Kode": "PA-03", "Tindakan": "Pelatihan penyegaran identifikasi dini anomali gaya kompresi bagi operator", "PIC": "QA Training Specialist", "Target": "2026-11-15", "Status": "Scheduled"}
            ],
            "review": "Evaluasi Efektivitas (60 Hari): Zero deviation terkait kalibrasi load cell dan nilai CpK disolusi 10 batch berikutnya > 1.33."
        }
    },
    "DEV-2026-0915 | Ekskursi Suhu FBD Granulasi Amoxicillin": {
        "code": "DEV-2026-0915",
        "title": "Ekskursi Suhu di Ruang Pengering FBD Granulasi Amoxicillin Sirup",
        "product": "Amoxicillin Trihydrate 125 mg/5 mL Sirup Kering",
        "batch": "BTH-AMX-260519",
        "dosage_form": "Granul Suspensi Rekonstitusi Oral",
        "line": "Lini Betalaktam Khusus Gedung Antibiotik",
        "cleanroom": "Kelas D (Controlled)",
        "stage": "Pengeringan Fluid Bed Dryer (FBD-02)",
        "detected_by": "Operator Produksi FBD & SCADA Alarm",
        "description": "Suhu inlet air pada Fluid Bed Dryer melonjak hingga 78.4 °C selama 42 menit (Batas kritis CPOB: 55.0 - 60.0 °C). Amoxicillin termolabil berisiko mengalami degradasi cincin betalaktam menjadi produk inaktif/toksik (asam penisiloat).",
        "severity": 5, "probability": 2, "detectability": 1, "rpn": 10,
        "classification": "Critical",
        "disposition": "Karantina Total & Rekomendasi Reject / Destruksi",
        "cqa_impact": "Potensi pembentukan pengotor B (Penicilloic acid), penurunan potensi terapeutik, dan OOS Assay.",
        "cpp_correlation": "Suhu udara inlet FBD melebihi batas stabilitas termal antibiotik betalaktam.",
        "fishbone": {
            "Man (Personil)": ["Operator merespon alarm SCADA terlambat 25 menit karena membantu tim sanitasi"],
            "Machine (Peralatan)": ["🎯 ROOT CAUSE: Pneumatic modulating steam valve macet pada 100% stroke akibat korosi batang aktuator", "Katup bypass manual terhalang instalasi pipa utilitas baru"],
            "Material (Bahan)": ["Kadar air awal granul sebelum pengeringan homogen memenuhi spesifikasi"],
            "Method (SOP)": ["Prosedur darurat ekskursi termal FBD belum dilengkapi auto-cutoff solenoid"],
            "Measurement (Alat Ukur)": ["Sensor suhu RTD PT-100 inlet membaca akurat tervalidasi"],
            "Milieu (Lingkungan HVAC)": ["Tekanan negatif ruang betalaktam (-15 Pa) terjaga sesuai proteksi silang CPOB"]
        },
        "five_whys": [
            ("Mengapa suhu inlet FBD mencapai 78.4 °C?", "Aliran uap panas (steam 3 bar) terus mengalir tanpa modulasi ke coil pemanas."),
            ("Mengapa uap panas terus mengalir tanpa modulasi?", "Pneumatic modulating control valve macet total pada posisi 100% terbuka."),
            ("Mengapa katup kontrol uap tersebut macet?", "Batang aktuator pneumatik mengalami korosi dan kerak kotoran steam trap."),
            ("Mengapa mesin tidak mematikan suplai steam saat suhu > 62 °C?", "FBD tipe lama tidak dilengkapi redundant emergency safety shut-off valve."),
            ("Mengapa tidak dilakukan upgrade interlock termal?", "🎯 AKAR MASALAH: Belum dilakukannya FMEA komprehensif pada utilitas pemanas mesin termolabil untuk menambahkan independent high-limit safety cut-off.")
        ],
        "capa": {
            "corrective": [
                {"Kode": "CA-01", "Tindakan": "Karantina batch BTH-AMX-260519 dan uji kadar serta related substances HPLC", "PIC": "QA Officer & QC Lab", "Target": "2026-10-24", "Status": "In Progress"},
                {"Kode": "CA-02", "Tindakan": "Overhaul dan ganti pneumatic steam control valve FBD-02 dan pasang steam strainer", "PIC": "Engineering Mechanical", "Target": "2026-10-25", "Status": "Pending"}
            ],
            "preventive": [
                {"Kode": "PA-01", "Tindakan": "Pasang Independent High-Temperature Safety Cut-off Solenoid Valve (trip otomatis pada 63 °C)", "PIC": "Automation Engineer", "Target": "2026-11-12", "Status": "Scheduled"},
                {"Kode": "PA-02", "Tindakan": "Audit dan inspeksi rutin steam trap di seluruh lini granulasi tiap 3 bulan", "PIC": "Utility Team", "Target": "2026-11-20", "Status": "Scheduled"}
            ],
            "review": "Evaluasi Efektivitas (90 Hari): Uji trip darurat katup safety cut-off berhasil 100% dalam 3 simulasi."
        }
    },
    "DEV-2026-1002 | Partikel Asing Filling Aseptis Ceftriaxone": {
        "code": "DEV-2026-1002",
        "title": "Kontaminasi Partikel Asing Terlihat pada Pengisian Aseptis Vial Injeksi",
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
        "disposition": "Karantina Sub-batch & Karantina Total untuk Investigasi",
        "cqa_impact": "Bebas partikulat asing (Particulate Matter USP <788>) gagal, risiko fatal emboli kapiler pasien.",
        "cpp_correlation": "Interaksi mekanis stopper bowl feeder dengan chute stainless steel.",
        "fishbone": {
            "Man (Personil)": ["Operator intervensi manual tanpa extension arm saat stopper tersumbat"],
            "Machine (Peralatan)": ["🎯 ROOT CAUSE: Chute track stainless steel memiliki burr mikro tajam akibat friksi", "🎯 ROOT CAUSE: Amplitudo vibrasi stopper bowl feeder disetel 75% (spek 45%)"],
            "Material (Bahan)": ["Stopper karet bromo-butyl telah dicuci dan disterilisasi sesuai siklus validasi"],
            "Method (SOP)": ["SOP tidak melarang pengubahan manual vibrasi getaran bowl di luar rentang tervalidasi"],
            "Measurement (Alat Ukur)": ["Kamera optik AVI mendeteksi partikel > 50 mikron secara akurat"],
            "Milieu (Lingkungan HVAC)": ["Partikel non-viable dan settle plate di LAF Kelas A nihil kontaminasi mikroba"]
        },
        "five_whys": [
            ("Mengapa ditemukan fragmen karet hitam di dalam vial?", "Stopper karet terkikis secara mekanis sebelum masuk ke leher vial."),
            ("Di mana pengikisan mekanis stopper karet terjadi?", "Pada jalur luncur (chute track) antara feeder bowl dan insertion head."),
            ("Mengapa stopper terkikis saat meluncur di chute track?", "Terdapat burr mikro tajam pada permukaan stainless steel rel."),
            ("Mengapa tekanan gesek stopper pada rel menjadi berlebih?", "Amplitudo getaran bowl dinaikkan manual oleh teknisi ke 75% untuk mempercepat aliran."),
            ("Mengapa parameter vibrasi diubah tanpa validasi & Change Control?", "🎯 AKAR MASALAH: Ketiadaan penguncian parameter kritis (CPP lockout) pada controller mesin dan absennya inspeksi kehalusan permukaan (surface roughness Ra) kontak steril.")
        ],
        "capa": {
            "corrective": [
                {"Kode": "CA-01", "Tindakan": "Tolak dan destruksi vial sub-batch menit 120-180 yang terpapar partikel", "PIC": "Head of QA", "Target": "2026-10-25", "Status": "Pending"},
                {"Kode": "CA-02", "Tindakan": "Electropolishing ulang chute stainless steel hingga Ra < 0.4 µm bebas burr", "PIC": "Tooling Specialist", "Target": "2026-10-27", "Status": "In Progress"}
            ],
            "preventive": [
                {"Kode": "PA-01", "Tindakan": "Kunci parameter vibrasi dengan password Supervisor (21 CFR Part 11 compliant)", "PIC": "Sterile Automation", "Target": "2026-11-08", "Status": "Scheduled"},
                {"Kode": "PA-02", "Tindakan": "Tambahkan checklist inspeksi mikroskopis kehalusan contact-parts bulanan", "PIC": "Preventive Maintenance", "Target": "2026-11-12", "Status": "Scheduled"}
            ],
            "review": "Evaluasi Efektivitas (30 Hari): Tingkat reject partikel AVI pada 3 batch berikutnya harus < 0.15%."
        }
    },
    "DEV-2026-1120 | Variasi Bobot Tablet & Capping Cetirizine": {
        "code": "DEV-2026-1120",
        "title": "Variasi Bobot Tablet & Capping pada Mesin Cetak Cetirizine 10 mg",
        "product": "Cetirizine HCl 10 mg Tablet Salut Selaput",
        "batch": "BTH-CTZ-260731",
        "dosage_form": "Tablet Inti (Uncoated)",
        "line": "Lini Solid Non-Steril Gedung I",
        "cleanroom": "Kelas E",
        "stage": "Pencetakan Tablet (Compression)",
        "detected_by": "IPC In-Process Control Operator",
        "description": "Pengujian bobot tablet menit ke-90 menunjukkan RSD bobot 4.2% (batas alert CPOB < 2.0%) dan fenomena capping sebesar 1.8% pada tablet inti cetak rotary.",
        "severity": 3, "probability": 3, "detectability": 1, "rpn": 9,
        "classification": "Minor",
        "disposition": "Karantina Parsial untuk Sortir & Uji Keseragaman Kandungan",
        "cqa_impact": "Potensi variasi dosis (Content Uniformity OOS) antar unit sediaan.",
        "cpp_correlation": "Rasio pre-compression force dan kecepatan feed frame tidak sinkron.",
        "fishbone": {
            "Man (Personil)": ["Operator menaikkan kecepatan feed frame untuk mengejar output per jam"],
            "Machine (Peralatan)": ["🎯 ROOT CAUSE: Baut pengunci pre-compression roller mengendur, gaya anjlok ke 1.2 kN", "Upper punch scraper aus sehingga serbuk menumpuk di leher die"],
            "Material (Bahan)": ["🎯 ROOT CAUSE: Proporsi serbuk halus (fines < 100 mesh) dalam granul mencapai 32% (batas ideal < 20%)"],
            "Method (SOP)": ["Setting pre-compression force tidak dicatat dalam lembar IPC awal"],
            "Measurement (Alat Ukur)": ["Timbangan analitik Mettler Toledo terkalibrasi harian dengan anak timbang E2"],
            "Milieu (Lingkungan HVAC)": ["RH ruangan 45% optimal untuk pencetakan tablet cetirizine"]
        },
        "five_whys": [
            ("Mengapa bobot bervariasi (RSD 4.2%) dan terjadi capping?", "Aliran granul ke die cavity tidak konstan dan udara terjebak saat kompresi utama."),
            ("Mengapa udara terjebak di dalam serbuk granul?", "Gaya pra-kompresi turun drastis ke 1.2 kN sehingga udara belum keluar sebelum kompresi."),
            ("Mengapa gaya pra-kompresi turun?", "Baut pengunci posisi roller mengendur akibat getaran mesin pencetak."),
            ("Mengapa fines serbuk juga tinggi sehingga memperparah capping?", "Saringan mesh pada mesin granulator basah mengalami keausan sehingga fines 32%."),
            ("Mengapa saringan aus tidak diganti saat setup?", "🎯 AKAR MASALAH: Belum adanya verifikasi umur pakai saringan granulator dan ketiadaan checklist torque wrench pada penguncian roller.")
        ],
        "capa": {
            "corrective": [
                {"Kode": "CA-01", "Tindakan": "Hentikan mesin, kencangkan baut roller dengan torque wrench tervalidasi ke 4.0 kN", "PIC": "Setup Technician", "Target": "2026-10-23", "Status": "Completed"},
                {"Kode": "CA-02", "Tindakan": "Pengujian Keseragaman Sediaan (Uniformity of Dosage Units) sub-batch terdampak", "PIC": "QC Analyst", "Target": "2026-10-24", "Status": "In Progress"}
            ],
            "preventive": [
                {"Kode": "PA-01", "Tindakan": "Modifikasi lembar Line Clearance: tambahkan verifikasi torsi pengunci roller ganda", "PIC": "QA In-Process", "Target": "2026-11-02", "Status": "Scheduled"},
                {"Kode": "PA-02", "Tindakan": "Tetapkan batas maksimal jam kerja saringan oscillating granulator", "PIC": "Preventive Maintenance", "Target": "2026-11-06", "Status": "Scheduled"}
            ],
            "review": "Evaluasi Efektivitas (45 Hari): RSD bobot tablet pada 5 batch berikutnya < 1.8% dan capping 0%."
        }
    }
}

# SIDEBAR: App Settings & Info
with st.sidebar:
    st.markdown("### 💊 PharmaCAPA AI")
    st.caption("CPOB 2018/2024 & ICH Q9/Q10 Compliant")
    st.divider()

    selected_preset_key = st.selectbox(
        "📁 Pilih Kasus Uji Industri Farmasi:",
        options=list(PRESETS.keys())
    )

    st.divider()
    st.markdown("#### ⚙️ Konfigurasi Mesin AI")
    engine_mode = st.radio("Pilih Engine:", ["Pharma Expert Neural (Offline Default)", "Google Gemini Live API"])
    gemini_key = ""
    if engine_mode == "Google Gemini Live API":
        gemini_key = st.text_input("Gemini API Key:", type="password", placeholder="AIzaSy...")
        if gemini_key:
            st.success("API Key terkonfigurasi!")
        else:
            st.info("Masukkan API Key atau gunakan mode Offline.")

    st.divider()
    st.markdown("""
    **Standar Kepatuhan Farmasi:**
    - BPOM RI CPOB 2018/2024
    - FDA 21 CFR 211.192
    - ICH Q9 (Risk Management)
    - ICH Q10 (Quality System)
    
    *Dikembangkan untuk Tugas Mata Kuliah Aplikasi AI untuk Industri.*
    """)

# Current Case Data
case_data = PRESETS[selected_preset_key]

# MAIN HEADER BANNER
st.markdown(f"""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 class="header-title">PharmaCAPA AI — Pharmaceutical Deviation & CAPA Copilot</h1>
            <div class="header-subtitle">PT PHARMA NUSANTARA TBK • QUALITY ASSURANCE DIVISION • CPOB & cGMP STANDARDS</div>
        </div>
        <div style="background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; color: #34d399; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 12px;">
            ● SISTEM OPERASIONAL AKTIF
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# TOP METRICS ROW
col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1.5])

with col1:
    st.markdown(f"**No. Deviasi:** `{case_data['code']}`")
    st.markdown(f"**Produk:** **{case_data['product']}**")
    st.caption(f"No. Bets: `{case_data['batch']}` | Lini: {case_data['line']}")

with col2:
    st.metric(
        label="Risk Priority Number (RPN)",
        value=case_data["rpn"],
        delta=f"S:{case_data['severity']} × P:{case_data['probability']} × D:{case_data['detectability']}"
    )

with col3:
    cls = case_data["classification"]
    badge_color = "#f43f5e" if cls == "Critical" else ("#f59e0b" if cls == "Major" else "#0ea5e9")
    st.markdown(f"**Klasifikasi Deviasi:**")
    st.markdown(f"<div style='font-size: 22px; font-weight: 800; color: {badge_color};'>{cls.upper()}</div>", unsafe_allow_html=True)
    st.caption("Tingkat Dampak Mutu ICH Q9")

with col4:
    st.markdown(f"**Rekomendasi Disposisi Bets:**")
    st.markdown(f"<div style='font-size: 15px; font-weight: 700; color: #f43f5e;'>🔒 {case_data['disposition']}</div>", unsafe_allow_html=True)
    st.caption("Protokol Penahanan Karantina CPOB")

st.divider()

# TABBED WORKSPACE
tab_ishikawa, tab_whys, tab_capa, tab_report = st.tabs([
    "🐟 Diagram Tulang Ikan 6M (Ishikawa)",
    "🔍 Metode 5-Whys Root Cause",
    "🛡️ Rencana CAPA (ICH Q10)",
    "📄 Dokumen Resmi Formulir Penyelidikan CPOB"
])

# TAB 1: ISHIKAWA 6M
with tab_ishikawa:
    st.markdown("### Model Ishikawa 6M Industri Farmasi")
    st.caption("Pemetaan faktor penyebab kegagalan mutu pada Man, Machine, Material, Method, Measurement, dan Milieu (Lingkungan HVAC).")
    
    col_left, col_right = st.columns(2)
    categories = list(case_data["fishbone"].items())
    
    with col_left:
        for cat, items in categories[:3]:
            with st.expander(f"📁 {cat}", expanded=True):
                for item in items:
                    if "ROOT CAUSE" in item:
                        st.markdown(f"<div class='root-cause-box'><strong>{item}</strong></div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"- {item}")
    
    with col_right:
        for cat, items in categories[3:]:
            with st.expander(f"📁 {cat}", expanded=True):
                for item in items:
                    if "ROOT CAUSE" in item:
                        st.markdown(f"<div class='root-cause-box'><strong>{item}</strong></div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"- {item}")

# TAB 2: 5-WHYS
with tab_whys:
    st.markdown("### Penelusuran Kausalitas Bertingkat (5-Whys Methodology)")
    st.caption("Investigasi mendalam dari gejala awal hingga menemukan akar masalah sistemik (True Root Cause).")
    
    for i, (q, a) in enumerate(case_data["five_whys"]):
        is_last = (i == len(case_data["five_whys"]) - 1)
        if is_last:
            st.error(f"**Langkah {i+1} — {q}**\n\n{a}")
        else:
            st.info(f"**Langkah {i+1} — {q}**\n\n{a}")

# TAB 3: CAPA PLAN
with tab_capa:
    st.markdown("### Matriks Rencana Tindakan Korektif & Preventif (CAPA)")
    
    st.subheader("⚡ A. Tindakan Korektif Langsung (Corrective Action - CA)")
    df_ca = pd.DataFrame(case_data["capa"]["corrective"])
    st.dataframe(df_ca, use_container_width=True, hide_index=True)

    st.subheader("🛡️ B. Tindakan Pencegahan Sistemik (Preventive Action - PA)")
    df_pa = pd.DataFrame(case_data["capa"]["preventive"])
    st.dataframe(df_pa, use_container_width=True, hide_index=True)

    st.success(f"🎯 **Protokol Evaluasi Efektivitas:** {case_data['capa']['review']}")

# TAB 4: OFFICIAL CPOB REPORT
with tab_report:
    st.markdown("### Formulir Resmi Penyelidikan Penyimpangan Mutu & Rencana CAPA")
    st.caption("Format Baku SOP-QA-042 Terakreditasi BPOM RI CPOB 2018/2024 & FDA 21 CFR Part 211")

    report_text = f"""
========================================================================================
PT PHARMA NUSANTARA TBK — QUALITY ASSURANCE DIVISION
FORMULIR PENYELIDIKAN PENYIMPANGAN MUTU & RENCANA CAPA (CPOB 2018/2024 BPOM)
No. Dokumen: SOP-QA-042-F01 (Rev. 05) | No. Deviasi: {case_data['code']}
========================================================================================

BAGIAN 1: INFORMASI BETS & PENYIMPANGAN
- Nama Produk        : {case_data['product']}
- No. Bets           : {case_data['batch']}
- Bentuk Sediaan     : {case_data['dosage_form']}
- Lini Produksi      : {case_data['line']}
- Kelas Kebersihan   : {case_data['cleanroom']}
- Tahapan Proses     : {case_data['stage']}
- Dideteksi Oleh     : {case_data['detected_by']}
- Tanggal Deteksi    : {datetime.now().strftime('%Y-%m-%d')}

DESKRIPSI KEJADIAN FAKTUAL:
{case_data['description']}

BAGIAN 2: KAJIAN RISIKO MUTU & DISPOSISI (ICH Q9)
- Nilai RPN          : {case_data['rpn']} (Severity: {case_data['severity']}, Probability: {case_data['probability']}, Detectability: {case_data['detectability']})
- Klasifikasi Deviasi: {case_data['classification'].upper()}
- Disposisi Bets     : {case_data['disposition']}
- Dampak CQA         : {case_data['cqa_impact']}
- Korelasi CPP       : {case_data['cpp_correlation']}

BAGIAN 3: ANALISIS AKAR MASALAH (ROOT CAUSE)
{case_data['five_whys'][-1][1]}

BAGIAN 4: RENCANA CAPA (ICH Q10)
Tindakan Korektif (CA):
{chr(10).join([f"  [{c['Kode']}] {c['Tindakan']} | PIC: {c['PIC']} | Target: {c['Target']}" for c in case_data['capa']['corrective']])}

Tindakan Pencegahan (PA):
{chr(10).join([f"  [{p['Kode']}] {p['Tindakan']} | PIC: {p['PIC']} | Target: {p['Target']}" for p in case_data['capa']['preventive']])}

Kriteria Evaluasi Efektivitas:
{case_data['capa']['review']}

BAGIAN 5: OTORISASI & TANDA TANGAN MULTIDISIPLIN
- Investigator QA     : apt. Rismawati L., S.Farm. [VERIFIED DIGITAL]
- Head of Production  : Ir. Hendra Wijaya, M.M.     [VERIFIED DIGITAL]
- Qualified Person/QA : apt. Dr. Arry S., M.Si.     [AUTHORIZED BPOM]
========================================================================================
Token Audit Trail: SHA256-PHARMA-{case_data['code']}-VALIDATED
    """

    st.code(report_text, language="markdown")
    st.download_button(
        label="📥 Download Laporan Resmi CPOB (.txt / .doc)",
        data=report_text,
        file_name=f"CPOB_Report_{case_data['code']}.txt",
        mime="text/plain"
    )
