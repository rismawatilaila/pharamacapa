/**
 * PharmaCAPA - Master Pharmaceutical Knowledge Base & Real-world QA Presets
 * Standards: CPOB 2018/2024 (BPOM RI), cGMP FDA 21 CFR Part 211, ICH Q9 & ICH Q10
 */

const PHARMA_PRESETS = [
  {
    id: "case-01",
    code: "DEV-2026-0842",
    title: "Kegagalan Uji Disolusi (OOS) pada Paracetamol 500 mg Tablet",
    productName: "Paracetamol 500 mg Kaplet",
    batchNumber: "BTH-PCT-260412",
    dosageForm: "Tablet / Kaplet Salut Film",
    productionLine: "Lini Solid Non-Steril - Gedung Formulasi II",
    areaGrade: "Kelas E (White Area)",
    stage: "Pengujian QC Ruang Ruahan (Bulk Product)",
    detectedBy: "Staff Analis QC Kimia Fisika",
    dateDetected: "2026-10-22",
    deviationSummary: "Hasil uji disolusi tahap S1 (n=6) menunjukkan nilai Q30 menit berada di kisaran 68% - 74%, tidak memenuhi spesifikasi rilis Farmakope Indonesia / CPOB (Q=80% pada menit ke-30). Pengujian diperluas ke tahap S2 (n=12) menghasilkan rata-rata 73.5%, terkonfirmasi Out-of-Specification (OOS).",
    initialParameters: {
      temperature: "24.5 °C (Ruang Kompresi)",
      humidity: "58% RH",
      mixingTime: "12 menit (Waktu pengadukan akhir)",
      binderLot: "PVP K-30 Lot #PV-2026-09",
      compressionPressure: "24.8 kN (Target: 18 - 20 kN)",
      tabletHardness: "14.2 kP (Spesifikasi: 7 - 10 kP)"
    },
    riskAssessment: {
      severity: 4, // 1-5 (Critical impact on bioavailabilitas)
      probability: 3, // Occasional
      detectability: 1, // High detectability (terdeteksi saat QC rutin)
      rpn: 12, // S x P x D calculation
      severityLevel: "Major",
      batchDisposition: "Quarantine / Reject untuk Rework Evaluasi",
      cqaImpact: "Bioavailabilitas & Laju Pelepasan Zat Aktif (Dissolution Rate) terganggu fatal",
      cppCorrelation: "Tekanan kompresi (compression force) dan kekerasan tablet (hardness) melebihi batas atas"
    },
    fishboneData: {
      man: [
        { cause: "Operator baru belum tersertifikasi penuh untuk mesin kompresi tablet Fette", isRoot: false, severity: "medium" },
        { cause: "Supervisi IPC oleh line leader terlambat dilakukan pada 30 menit awal pencetakan", isRoot: false, severity: "low" }
      ],
      machine: [
        { cause: "Sensor tekanan hidrolik rotary tablet press mengalami drift kalibrasi sebesar +22%", isRoot: true, severity: "critical" },
        { cause: "Alarm over-force pada HMI dinonaktifkan sementara saat setting tooling awal", isRoot: true, severity: "high" }
      ],
      material: [
        { cause: "Kadar air granul (LOD) sebesar 1.1% (agak terlalu kering, spesifikasi 1.5 - 2.5%)", isRoot: false, severity: "medium" },
        { cause: "Karakteristik deformasi plastis granul berubah akibat waktu pengeringan berlebih di FBD", isRoot: false, severity: "medium" }
      ],
      method: [
        { cause: "SOP-PRD-TAB-014 tidak memiliki instruksi verifikasi dua orang (four-eyes check) untuk setting awal punch", isRoot: false, severity: "medium" },
        { cause: "Frekuensi pengujian IPC kekerasan tablet per 30 menit terlewat saat pergantian shift", isRoot: false, severity: "medium" }
      ],
      measurement: [
        { cause: "Alat Hardness Tester Erweka di ruang IPC terkalibrasi baik, data akurat", isRoot: false, severity: "low" },
        { cause: "Disolusi bath USP Apparatus II terkalibrasi dan media disolusi dapar fosfat valid", isRoot: false, severity: "low" }
      ],
      environment: [
        { cause: "Suhu ruangan 24.5 °C dan RH 58% masih dalam batas alert limit Kelas E (< 25 °C, < 60% RH)", isRoot: false, severity: "low" }
      ]
    },
    fiveWhys: [
      { step: 1, question: "Mengapa tablet Paracetamol tidak memenuhi syarat disolusi Q=80%?", answer: "Kekerasan tablet rata-rata 14.2 kP (jauh melampaui rentang spesifikasi 7 - 10 kP), sehingga waktu hancur tablet menjadi 24 menit (standar < 15 menit)." },
      { step: 2, question: "Mengapa kekerasan tablet melonjak tinggi selama pencetakan?", answer: "Gaya kompresi utama (main compression force) pada rotary press beroperasi pada 24.8 kN padahal setpoint SOP adalah 18 - 20 kN." },
      { step: 3, question: "Mengapa mesin berjalan pada gaya 24.8 kN tanpa operator menyadarinya?", answer: "Sensor load cell pada unit kompresi mengalami drift pembacaan sebesar +22%, menampilkan 19.5 kN pada layar HMI padahal tekanan aktual 24.8 kN." },
      { step: 4, question: "Mengapa drift sensor load cell tidak terdeteksi saat kalibrasi?", answer: "Jadwal kalibrasi beban load cell 6-bulanan tertunda 3 minggu karena utilitas mesin beroperasi penuh memenuhi lonjakan target produksi." },
      { step: 5, question: "Mengapa sistem pemeliharaan preventif (PM) mengizinkan penundaan kalibrasi komponen kritis?", answer: "Akar Masalah (Root Cause): Belum adanya sistem 'Hard-Stop Interlock' pada software maintenance yang secara otomatis mengunci mesin farmasi jika jadwal re-kalibrasi instrumen kritis terlewati." }
    ],
    capaPlan: {
      correctiveActions: [
        {
          id: "CA-01",
          description: "Karantina resmi (Quarantine Tag Merah) untuk seluruh batch BTH-PCT-260412 di gudang karantina QA.",
          responsible: "QA Officer - Karantina & Rilis",
          targetDate: "2026-10-23",
          status: "Pending Execution"
        },
        {
          id: "CA-02",
          description: "Segera hentikan operasi Mesin Tablet Press TP-03 dan lakukan re-kalibrasi darurat serta penggantian sensor load cell oleh tim Kalibrasi & Metrologi.",
          responsible: "Engineering & Maintenance Supervisor",
          targetDate: "2026-10-24",
          status: "In Progress"
        },
        {
          id: "CA-03",
          description: "Lakukan kajian teknis Rework Protocol (rekristalisasi/granulasi ulang) atau putuskan Penolakan/Destruksi jika stabilitas zat aktif berisiko.",
          responsible: "QA Manager & R&D Formulasi",
          targetDate: "2026-10-26",
          status: "Pending Execution"
        }
      ],
      preventiveActions: [
        {
          id: "PA-01",
          description: "Pemasangan 'Electronic Calibration Interlock' pada PLC mesin: mesin tidak dapat 'Start Run' apabila status kalibrasi sensor kritis kadaluarsa.",
          responsible: "Automation & Instrumentation Engineer",
          targetDate: "2026-11-10",
          status: "Scheduled"
        },
        {
          id: "PA-02",
          description: "Revisi SOP-PRD-TAB-014: Wajibkan 'Double-Sign Verification' IPC kekerasan & ketebalan tablet pada 15 menit pertama setting dan setiap pergantian shift.",
          responsible: "Production Supervisor & QA Compliance",
          targetDate: "2026-11-05",
          status: "Scheduled"
        },
        {
          id: "PA-03",
          description: "Pelatihan penyegaran (Refresher Training) bagi seluruh operator cetak tablet mengenai identifikasi dini anomali gaya kompresi.",
          responsible: "Training & People Development QA",
          targetDate: "2026-11-15",
          status: "Scheduled"
        }
      ],
      effectivenessReview: {
        reviewInterval: "60 Hari Pasca Implementasi CAPA",
        criteria: "Zero deviation terkait kalibrasi load cell tablet press dan trend CpK nilai disolusi 10 batch berikutnya > 1.33."
      }
    }
  },
  {
    id: "case-02",
    code: "DEV-2026-0915",
    title: "Ekskursi Suhu (Temperature Excursion) di Ruang Pengering FBD Granulasi Amoxicillin",
    productName: "Amoxicillin Trihydrate 125 mg/5 mL Sirup Kering",
    batchNumber: "BTH-AMX-260519",
    dosageForm: "Granul untuk Suspensi Rekonstitusi Oral",
    productionLine: "Lini Betalaktam - Gedung Khusus Antibiotik",
    areaGrade: "Kelas D (Controlled Area Betalaktam)",
    stage: "Pengeringan Fluid Bed Dryer (FBD-02)",
    detectedBy: "Operator Produksi FBD & Sistem SCADA Alarm",
    dateDetected: "2026-10-22",
    deviationSummary: "Suhu inlet air pada Fluid Bed Dryer melonjak hingga 78.4 °C selama 42 menit (Spesifikasi batas kritis suhu inlet: 55.0 - 60.0 °C). Amoxicillin bersifat termolabil sehingga kenaikan suhu berisiko menyebabkan degradasi cincin betalaktam menjadi asam penisiloat dan produk degradasi beracun/inaktif.",
    initialParameters: {
      inletAirTemp: "78.4 °C (Batas Kritis: 55 - 60 °C)",
      outletAirTemp: "54.2 °C (Target: 38 - 42 °C)",
      excursionDuration: "42 Menit",
      productTemp: "52.1 °C (Target maks: 45 °C)",
      steamControlValve: "Stuck Open pada 100% stroke"
    },
    riskAssessment: {
      severity: 5, // Catastrophic for antibiotic potency & patient safety
      probability: 2, // Rare
      detectability: 1, // Instantly logged by SCADA
      rpn: 10,
      severityLevel: "Critical",
      batchDisposition: "Quarantine Segera, Rekomendasi Reject / Destruksi Produk",
      cqaImpact: "Potensi terbentuknya pengotor B (Penicilloic acid), penurunan kadar zat aktif (Assay OOS), dan hilangnya potensi terapeutik",
      cppCorrelation: "Suhu udara masuk (Inlet Air Temp) melebihi batas kritis stabilitas antibiotik betalaktam"
    },
    fishboneData: {
      man: [
        { cause: "Operator merespon alarm SCADA setelah 25 menit karena sedang membantu tim sanitasi ruangan", isRoot: false, severity: "high" }
      ],
      machine: [
        { cause: "Pneumatic modulating steam valve macet pada posisi terbuka penuh (100%) akibat korosi internal aktuator", isRoot: true, severity: "critical" },
        { cause: "Katup bypass uap darurat manual sulit dijangkau karena terhalang pipa utilitas baru", isRoot: false, severity: "medium" }
      ],
      material: [
        { cause: "Kualitas granul sebelum pengeringan homogen dan memenuhi uji IPC kadar air awal", isRoot: false, severity: "low" }
      ],
      method: [
        { cause: "Prosedur penanganan darurat ekskursi termal di FBD belum mencantumkan auto-cutoff solenoid", isRoot: true, severity: "high" }
      ],
      measurement: [
        { cause: "Sensor RTD PT-100 suhu inlet membaca akurat (terkonfirmasi dengan termokopel independen)", isRoot: false, severity: "low" }
      ],
      environment: [
        { cause: "Tekanan negatif ruang betalaktam (-15 Pa) terjaga sesuai CPOB proteksi silang", isRoot: false, severity: "low" }
      ]
    },
    fiveWhys: [
      { step: 1, question: "Mengapa suhu inlet FBD mencapai 78.4 °C?", answer: "Aliran uap panas (steam) bertekanan 3 bar terus mengalir tanpa modulasi ke coil pemanas udara inlet." },
      { step: 2, question: "Mengapa uap panas terus mengalir tanpa modulasi?", answer: "Pneumatic control valve uap macet total pada posisi 100% open (terbuka penuh)." },
      { step: 3, question: "Mengapa katup kontrol uap tersebut macet?", answer: "Batang aktuator pneumatik mengalami korosi dan tumpukan kerak kotoran steam trap sehingga mechanical spring gagal menarik kembali katup." },
      { step: 4, question: "Mengapa sistem keselamatan mesin tidak mematikan suplai steam saat suhu > 62 °C?", answer: "Mesin FBD tipe lama ini tidak dilengkapi redundant emergency safety shut-off valve yang independen dari loop kontrol PLC." },
      { step: 5, question: "Mengapa tidak dilakukan upgrade sistem safety interlock termal?", answer: "Akar Masalah (Root Cause): Belum dilakukannya Failure Mode and Effects Analysis (FMEA) komprehensif pada utilitas pemanas mesin formulasi termolabil untuk menambahkan independent high-limit safety cut-off." }
    ],
    capaPlan: {
      correctiveActions: [
        {
          id: "CA-01",
          description: "Karantina batch BTH-AMX-260519 dan lakukan uji kadar Amoxicillin serta Related Substances (Impurities) via HPLC sesuai kompendial.",
          responsible: "QA Compliance & Lab QC",
          targetDate: "2026-10-24",
          status: "In Progress"
        },
        {
          id: "CA-02",
          description: "Overhaul dan ganti unit pneumatic steam control valve FBD-02 beserta instalasi steam strainer baru.",
          responsible: "Engineering Mechanical Section",
          targetDate: "2026-10-25",
          status: "Pending Execution"
        }
      ],
      preventiveActions: [
        {
          id: "PA-01",
          description: "Pasang Independent High-Temperature Safety Cut-off Solenoid Valve yang otomatis menutup aliran steam secara mekanik saat suhu mencapai 63 °C.",
          responsible: "Automation & Process Engineering",
          targetDate: "2026-11-12",
          status: "Scheduled"
        },
        {
          id: "PA-02",
          description: "Lakukan audit dan inspeksi steam trap di seluruh lini proses granulasi basah setiap 3 bulan sekali.",
          responsible: "Plant Utility Team",
          targetDate: "2026-11-20",
          status: "Scheduled"
        }
      ],
      effectivenessReview: {
        reviewInterval: "90 Hari",
        criteria: "Uji simulasi trip high-temp safety valve berhasil 100% dalam 3 kali percobaan tanpa kegagalan mekanik."
      }
    }
  },
  {
    id: "case-03",
    code: "DEV-2026-1002",
    title: "Kontaminasi Partikel Asing Terlihat pada Pengisian Aseptis Ampul Injeksi",
    productName: "Ceftriaxone Sodium 1 g Serbuk Injeksi",
    batchNumber: "BTH-CTX-260604",
    dosageForm: "Serbuk Kering Injeksi Steril",
    productionLine: "Lini Aseptis Steril - Gedung Steril Lt. 3",
    areaGrade: "Kelas A dalam Latar Belakang Kelas B (Grade A Laminar Airflow)",
    stage: "Filling & Stoppering Aseptis",
    detectedBy: "Inspeksi Visual Otomatis (Automatic Visual Inspection - AVI)",
    dateDetected: "2026-10-22",
    deviationSummary: "Sistem AVI mendeteksi lonjakan partikel asing gelap (black foreign particle) sebesar 3.4% pada vial pengisian menit ke 120-150 (Reject limit batas peringatan: 0.5%, batas tindakan: 1.0%). Analisis FTIR mikro menunjukkan partikel berupa fragmen karet elastomerik halogenasi.",
    initialParameters: {
      particlesDetected: "3.4% (Threshold: maks 0.5%)",
      ftirAnalysis: "Bromo-butyl rubber elastomer fragment",
      fillingSpeed: "120 vial / menit",
      nitrogenPurge: "Tekanan 1.2 bar",
      differentialPressure: "Delta P Kelas A ke B: +18 Pa (Normal)"
    },
    riskAssessment: {
      severity: 5, // Critical - Sterility & Foreign matter in parenteral
      probability: 2,
      detectability: 1, // Detected by 100% AVI camera
      rpn: 10,
      severityLevel: "Critical",
      batchDisposition: "Quarantine Sub-batch dan Karantina Total untuk Investigasi",
      cqaImpact: "Bebas partikulat asing (Particulate Matter USP <788>) gagal, risiko emboli kapiler pada pasien",
      cppCorrelation: "Interaksi mekanis stopper bowl feeder dengan chute stopper karet"
    },
    fishboneData: {
      man: [
        { cause: "Operator melakukan intervensi manual tanpa glove port extension saat stopper tersumbat", isRoot: false, severity: "high" }
      ],
      machine: [
        { cause: "Chute pengumpan stopper berbahan stainless steel 316L memiliki burr mikro akibat gesekan terus menerus", isRoot: true, severity: "critical" },
        { cause: "Vibrasi stopper bowl feeder disetel terlalu tinggi (amplitudo 75% vs SOP 45%)", isRoot: true, severity: "high" }
      ],
      material: [
        { cause: "Stopper karet bromo-butyl telah melalui proses cuci dan sterilisasi autoklaf sesuai siklus tervalidasi", isRoot: false, severity: "low" }
      ],
      method: [
        { cause: "SOP penanganan stopper jam di Kelas A tidak melarang penyetelan getaran bowl di luar rentang tervalidasi", isRoot: false, severity: "medium" }
      ],
      measurement: [
        { cause: "Kamera inspeksi optik AVI mendeteksi partikel berukuran > 50 mikron secara akurat", isRoot: false, severity: "low" }
      ],
      environment: [
        { cause: "Partikel non-viable 0.5 µm dan viable settle plate di LAF Kelas A nihil mikroba", isRoot: false, severity: "low" }
      ]
    },
    fiveWhys: [
      { step: 1, question: "Mengapa ditemukan fragmen partikel karet hitam di dalam vial?", answer: "Stopper karet terkikis secara mekanis sebelum dimasukkan ke dalam leher vial injeksi." },
      { step: 2, question: "Di mana pengikisan mekanis stopper karet tersebut terjadi?", answer: "Pada jalur luncur (chute track) antara vibratory feeder bowl dan insertion head." },
      { step: 3, question: "Mengapa stopper terkikis saat melewati chute track?", answer: "Terdapat burr tajam mikro pada permukaan rel stainless steel dan stopper meluncur dengan tekanan gesek berlebih." },
      { step: 4, question: "Mengapa tekanan gesek stopper pada rel menjadi berlebih?", answer: "Amplitudo getaran vibratory bowl dinaikkan manual oleh teknisi ke 75% untuk mempercepat aliran stopper yang sering tersendat." },
      { step: 5, question: "Mengapa vibrasi diubah tanpa kontrol perubahan (Change Control) dan validasi?", answer: "Akar Masalah (Root Cause): Kurangnya penguncian parameter kritis (Critical Process Parameter lockout) pada controller vibratory feeder dan ketiadaan inspeksi berkala terhadap kehalusan permukaan (surface roughness Ra) jalur stopper steril." }
    ],
    capaPlan: {
      correctiveActions: [
        {
          id: "CA-01",
          description: "Tolak dan destruksi vial sub-batch menit ke 120-180 yang terpapar partikel.",
          responsible: "QA Head of Quality Assurance",
          targetDate: "2026-10-25",
          status: "Pending Execution"
        },
        {
          id: "CA-02",
          description: "Lakukan electropolishing ulang pada chute stainless steel hingga mencapai nilai Ra < 0.4 µm bebas burr.",
          responsible: "Tooling & Fabrication Specialist",
          targetDate: "2026-10-27",
          status: "In Progress"
        }
      ],
      preventiveActions: [
        {
          id: "PA-01",
          description: "Kunci akses parameter amplitudo vibrasi feeder dengan password otorisasi tingkat Supervisor (21 CFR Part 11 compliant).",
          responsible: "Sterile Automation Engineer",
          targetDate: "2026-11-08",
          status: "Scheduled"
        },
        {
          id: "PA-02",
          description: "Tambahkan checklist inspeksi visual mikroskopis kehalusan permukaan contact-parts pada setiap pergantian kampanye produksi steril bulanan.",
          responsible: "Preventive Maintenance Team",
          targetDate: "2026-11-12",
          status: "Scheduled"
        }
      ],
      effectivenessReview: {
        reviewInterval: "30 Hari Pasca Kampanye Steril Berikutnya",
        criteria: "Tingkat reject partikel AVI pada 3 batch berikutnya harus < 0.15%."
      }
    }
  },
  {
    id: "case-04",
    code: "DEV-2026-1120",
    title: "Variasi Bobot Tablet & Capping pada Mesin Cetak Cetirizine 10 mg",
    productName: "Cetirizine HCl 10 mg Tablet Salut Selaput",
    batchNumber: "BTH-CTZ-260731",
    dosageForm: "Tablet Inti (Uncoated Tablet)",
    productionLine: "Lini Solid Non-Steril - Gedung Formulasi I",
    areaGrade: "Kelas E",
    stage: "Pencetakan Tablet (Compression)",
    detectedBy: "IPC In-Process Control Operator",
    dateDetected: "2026-10-22",
    deviationSummary: "Pemeriksaan bobot tablet pada menit ke-90 menunjukkan deviasi bobot rata-rata melebihi batas alert limit (RSD bobot 4.2%, spesifikasi < 2.0%). Ditemukan juga fenomena capping (bagian atas tablet terkelupas) sebesar 1.8% pada tablet inti.",
    initialParameters: {
      tabletWeightTarget: "150 mg ± 5% (142.5 - 157.5 mg)",
      actualWeightRange: "138 mg - 164 mg (RSD 4.2%)",
      cappingRate: "1.8% dari sampel 500 tablet",
      feedFrameSpeed: "35 RPM (Standar: 20 - 25 RPM)",
      preCompressionForce: "1.2 kN (Standar: 3.5 - 4.5 kN)"
    },
    riskAssessment: {
      severity: 3, // Moderate impact on content uniformity
      probability: 3, // Occasional
      detectability: 1, // Caught during routine 30-min IPC
      rpn: 9,
      severityLevel: "Minor",
      batchDisposition: "Karantina Parsial untuk Sortir & Evaluasi Keseragaman Kandungan",
      cqaImpact: "Potensi variasi dosis (Keseragaman Sediaan / Content Uniformity OOS)",
      cppCorrelation: "Rasio pre-compression force dan kecepatan force feeder tidak sinkron"
    },
    fishboneData: {
      man: [
        { cause: "Operator menaikkan kecepatan putar feed frame untuk mengejar target output per jam", isRoot: false, severity: "medium" }
      ],
      machine: [
        { cause: "Pre-compression roller tidak dikunci dengan torsi yang tepat, bergeser dari setpoint 4.0 kN ke 1.2 kN", isRoot: true, severity: "high" },
        { cause: "Upper punch scraper aus sehingga serbuk granul menumpuk di leher die", isRoot: false, severity: "medium" }
      ],
      material: [
        { cause: "Proporsi serbuk halus (fines < 100 mesh) dalam granul mencapai 32% (batas ideal < 20%)", isRoot: true, severity: "critical" }
      ],
      method: [
        { cause: "Setting pre-compression force tidak dicatat dalam lembar IPC awal", isRoot: false, severity: "medium" }
      ],
      measurement: [
        { cause: "Timbangan analitik Mettler Toledo terkalibrasi harian dengan anak timbang kelas E2", isRoot: false, severity: "low" }
      ],
      environment: [
        { cause: "RH ruangan 45% (optimal untuk pencetakan tablet cetirizine)", isRoot: false, severity: "low" }
      ]
    },
    fiveWhys: [
      { step: 1, question: "Mengapa bobot tablet bervariasi (RSD 4.2%) dan terjadi capping?", answer: "Aliran granul ke dalam die cavity tidak konstan dan udara terjebak di dalam serbuk saat proses kompresi utama." },
      { step: 2, question: "Mengapa udara terjebak di dalam serbuk granul?", answer: "Gaya pra-kompresi (pre-compression force) turun drastis ke 1.2 kN sehingga udara belum sempat keluar sebelum kompresi utama." },
      { step: 3, question: "Mengapa gaya pra-kompresi turun?", answer: "Baut pengunci posisi pre-compression roller mengendur akibat getaran mesin." },
      { step: 4, question: "Mengapa persentase fine powder juga tinggi sehingga memperparah capping?", answer: "Saringan mesh pada mesin granulator basah mengalami keausan sehingga menghasilkan fines berlebih (32%)." },
      { step: 5, question: "Mengapa saringan yang aus tidak diganti saat setup?", answer: "Akar Masalah (Root Cause): Belum adanya prosedur verifikasi keausan saringan mesh granulator sebelum proses granulasi dimulai dan ketiadaan torque wrench checklist pada penguncian roller kompresi." }
    ],
    capaPlan: {
      correctiveActions: [
        {
          id: "CA-01",
          description: "Hentikan pencetakan, kencangkan baut pre-compression roller dengan torque wrench tervalidasi pada setpoint 4.0 kN.",
          responsible: "Machine Setup Technician",
          targetDate: "2026-10-23",
          status: "Completed"
        },
        {
          id: "CA-02",
          description: "Lakukan pengujian Keseragaman Sediaan (Uniformity of Dosage Units) pada sub-batch yang terdampak.",
          responsible: "QC Finished Goods Analyst",
          targetDate: "2026-10-24",
          status: "In Progress"
        }
      ],
      preventiveActions: [
        {
          id: "PA-01",
          description: "Modifikasi lembar Line Clearance mesin kompresi: tambahkan verifikasi torsi pengunci roller dengan tanda tangan ganda.",
          responsible: "QA In-Process Assurance",
          targetDate: "2026-11-02",
          status: "Scheduled"
        },
        {
          id: "PA-02",
          description: "Tetapkan batas maksimal masa pakai (lifespan jam kerja) untuk saringan oscillating granulator sebelum wajib diganti.",
          responsible: "Preventive Maintenance Engineer",
          targetDate: "2026-11-06",
          status: "Scheduled"
        }
      ],
      effectivenessReview: {
        reviewInterval: "45 Hari",
        criteria: "RSD bobot tablet pada 5 batch berikutnya konsisten < 1.8% dan capping rate 0%."
      }
    }
  }
];

// Regulatory Reference Standards
const REGULATORY_STANDARDS = {
  cpob: "Pedoman Cara Pembuatan Obat yang Baik (CPOB 2018 / 2024 BPOM RI)",
  ichQ9: "ICH Q9: Quality Risk Management (FMEA, Risk Matrix, RPN)",
  ichQ10: "ICH Q10: Pharmaceutical Quality System (CAPA Methodology)",
  who: "WHO Technical Report Series, No. 986, Annex 2 (Good Manufacturing Practices)",
  fda: "FDA 21 CFR Part 211.192: Production record review - investigations of deviations"
};
