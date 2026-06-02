"""
Generate comprehensive technical report — Pulsevera CC26-PRU439.
Output: ../reports/pulsevera_comprehensive_report.pdf

Covers: Cover, Executive Summary, Problem Discovery, Dataset,
Data Wrangling, EDA, Feature Engineering, A/B Testing,
ML Baseline, Deep Learning, Evaluation, SHAP, Architecture, Limitations.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use('Agg')

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT

BASE    = Path(__file__).resolve().parent
MODELS  = BASE / 'models'
REPORTS = BASE.parent / 'reports'
FIGS    = BASE.parent / 'notebooks' / 'figures'
REPORTS.mkdir(parents=True, exist_ok=True)

# ── Load metadata from JSON ─────────────────────────────────────────────────
with open(MODELS / 'dl_metadata.json') as f:
    DL = json.load(f)

with open(MODELS / 'ml_results.json') as f:
    ML = json.load(f)

with open(MODELS / 'shap_metadata.json') as f:
    SHAP = json.load(f)


def img(path: Path, w_cm: float, h_cm: float, halign: str = 'CENTER') -> Image:
    """Return Image if file exists, else a placeholder Spacer."""
    if path.exists():
        return Image(str(path), width=w_cm * cm, height=h_cm * cm, hAlign=halign)
    sp = Spacer(1, h_cm * cm)
    return sp


# ── Styles ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

INDIGO  = colors.HexColor('#4F46E5')
EMERALD = colors.HexColor('#10B981')
CORAL   = colors.HexColor('#EF4444')
NAVY    = colors.HexColor('#1E3A5F')
SLATE   = colors.HexColor('#64748B')
LIGHT   = colors.HexColor('#EEF2FF')
WHITE   = colors.white

def _add(name, parent='BodyText', **kw):
    styles.add(ParagraphStyle(name=name, parent=styles[parent], **kw))

_add('Cover1',    'Title',    alignment=TA_CENTER, fontSize=32, textColor=INDIGO,   spaceAfter=6)
_add('Cover2',    'Normal',   alignment=TA_CENTER, fontSize=14, textColor=NAVY,     spaceAfter=4)
_add('CoverSub',  'Normal',   alignment=TA_CENTER, fontSize=10, textColor=SLATE,    spaceAfter=4)
_add('H1',        'Heading1', textColor=INDIGO,   spaceBefore=18, spaceAfter=8,  fontSize=15)
_add('H2',        'Heading2', textColor=NAVY,     spaceBefore=12, spaceAfter=6,  fontSize=12)
_add('H3',        'Heading3', textColor=SLATE,    spaceBefore=8,  spaceAfter=4,  fontSize=10)
_add('Body',      'BodyText', alignment=TA_JUSTIFY, fontSize=9.5, leading=14)
_add('Note',      'BodyText', fontSize=8.5, textColor=SLATE, leftIndent=10, leading=12)
_add('Mono',      'BodyText', fontName='Courier', fontSize=8, leading=11, leftIndent=10)
_add('Badge',     'Normal',   alignment=TA_CENTER, fontSize=9, textColor=WHITE,
     backColor=INDIGO, borderPadding=4)
_add('LIM',       'Body',     spaceBefore=6, leftIndent=10)
_add('KF',        'Body',     spaceBefore=5, leftIndent=12)
_add('TOC',       'Body',     spaceBefore=4, leftIndent=8)

TBL_HEADER = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), NAVY),
    ('TEXTCOLOR',  (0, 0), (-1, 0), WHITE),
    ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE',   (0, 0), (-1, -1), 8.5),
    ('ALIGN',      (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID',       (0, 0), (-1, -1), 0.4, colors.HexColor('#CBD5E0')),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
])

def tbl(data, col_widths, extra_style=None):
    t = Table(data, colWidths=[w * cm for w in col_widths])
    s = TableStyle(TBL_HEADER._cmds[:])
    if extra_style:
        for cmd in extra_style:
            s.add(*cmd)
    t.setStyle(s)
    return t

# ── Document ────────────────────────────────────────────────────────────────
pdf_path = REPORTS / 'pulsevera_comprehensive_report.pdf'
doc = SimpleDocTemplate(
    str(pdf_path), pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.2*cm, bottomMargin=2*cm,
)

flow = []
P  = lambda text, style='Body': flow.append(Paragraph(text, styles[style]))
SP = lambda h=6: flow.append(Spacer(1, h))
HR = lambda: flow.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#CBD5E0'), spaceAfter=6))


# ═══════════════════════════════════════════════════════════════════════════
# COVER
# ═══════════════════════════════════════════════════════════════════════════
SP(40)
P('Pulsevera', 'Cover1')
P('Laporan Teknis Komprehensif', 'Cover2')
SP(8)
HR()
SP(8)
P('Deteksi Dini Risiko Penyakit Jantung Berbasis Kecerdasan Buatan', 'Cover2')
SP(16)

cover_meta = tbl([
    ['Proyek', 'CC26-PRU439 · DBS Foundation Coding Camp 2026'],
    ['Dataset', 'CDC BRFSS 2022 — 445.132 responden'],
    ['Model Final', f'Deep Learning + SMOTE @ Threshold {DL["best_threshold"]}'],
    ['Akurasi', f'{DL["test_accuracy"]*100:.2f}%'],
    ['Recall (Positif)', f'{DL["test_recall_pos"]*100:.2f}%'],
    ['ROC-AUC', f'{DL["test_roc_auc"]:.4f}'],
    ['Tanggal Laporan', datetime.now().strftime('%d %B %Y')],
], [4, 12])
flow.append(cover_meta)

SP(24)
P(
    '<i>"Jantungmu, Cerita Masa Depanmu."</i><br/>'
    'Pulsevera — Early Cardiovascular Risk Detection for Everyone.',
    'CoverSub',
)
flow.append(PageBreak())


# ═══════════════════════════════════════════════════════════════════════════
# DAFTAR ISI
# ═══════════════════════════════════════════════════════════════════════════
P('Daftar Isi', 'H1')
SP(4)
toc_items = [
    ('1.', 'Executive Summary'),
    ('2.', 'Problem Discovery & Business Context'),
    ('3.', 'Dataset — CDC BRFSS 2022'),
    ('4.', 'Data Wrangling & Preprocessing'),
    ('5.', 'Exploratory Data Analysis'),
    ('6.', 'Feature Engineering'),
    ('7.', 'A/B Testing — Validasi Hipotesis'),
    ('8.', 'ML Baseline Modeling'),
    ('9.', 'Deep Learning — Arsitektur & Training'),
    ('10.', 'Evaluasi Model & Threshold Tuning'),
    ('11.', 'SHAP Interpretability'),
    ('12.', 'Arsitektur Sistem & Deployment'),
    ('13.', 'Limitasi & Rencana ke Depan'),
]
for num, title in toc_items:
    P(f'<b>{num}</b>&nbsp;&nbsp;{title}', 'TOC')
flow.append(PageBreak())


# ═══════════════════════════════════════════════════════════════════════════
# 1. EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════════════════════
P('1. Executive Summary', 'H1')
HR()
P(
    'Pulsevera adalah aplikasi web berbasis Kecerdasan Buatan yang memungkinkan siapa pun '
    'melakukan screening awal risiko penyakit jantung dalam kurang dari dua menit, tanpa '
    'memerlukan latar belakang medis atau kunjungan ke fasilitas kesehatan. '
    'Laporan ini mendokumentasikan seluruh pipeline sains data — mulai dari eksplorasi '
    'dataset, rekayasa fitur, pengujian hipotesis, pemodelan, hingga interpretabilitas '
    'dan integrasi ke sistem produksi.'
)
SP()
P('Temuan Kunci:', 'H2')

key_findings = [
    ('Dataset', 'CDC BRFSS 2022 dengan 445.132 sampel; target HadHeartAttack memiliki class imbalance ekstrem (5,6% positif). Empat strategi digunakan: SMOTE, class_weight balanced, Focal Loss, dan threshold tuning.'),
    ('Model Final', f'Deep Learning (Dense 256-128-64) + SMOTE, dilatih dengan Focal Loss (γ=2.0, α=0.25) dan EarlyStoppingByRecall. Threshold operasional 0.23 dipilih sebagai sweet spot yang memenuhi kedua target: Accuracy ≥85% dan Recall ≥70%.'),
    ('Performa', f'Accuracy {DL["test_accuracy"]*100:.2f}%, Recall {DL["test_recall_pos"]*100:.2f}%, Precision {DL["test_precision_pos"]*100:.2f}%, F1 {DL["test_f1_pos"]*100:.2f}%, ROC-AUC {DL["test_roc_auc"]:.4f}. Model mengungguli Random Forest (RF) dalam Recall (71% vs 44%) dan ROC-AUC (0.88 vs 0.85) meskipun RF memiliki accuracy lebih tinggi (91%).'),
    ('Feature Engineering', '6 fitur baru dibuat: BMI, LifestyleRiskScore (0–5), IsObese, IsSleepDeprived, IsActiveSmoker, HasChronicCondition. LifestyleRiskScore masuk top-20 global SHAP importance.'),
    ('A/B Testing', '4 hipotesis epidemiologis divalidasi secara statistik (semua signifikan, p < 0.001). Aktivitas fisik, BMI, merokok, dan pola tidur terbukti berhubungan dengan risiko serangan jantung.'),
    ('Interpretabilitas', 'SHAP TreeExplainer digunakan untuk atribusi fitur per instance dan global importance. GeneralHealth, AgeCategory, dan HadAngina adalah kontributor utama prediksi.'),
    ('Sistem', 'Three-layer architecture: React + Vite frontend, Express.js proxy, FastAPI ML API. Inference time ±350ms termasuk preprocessing, model forward pass, SHAP matching, dan Gemini recommendation.'),
]
for topic, desc in key_findings:
    P(f'<b>{topic}:</b> {desc}', 'KF')
flow.append(PageBreak())


# ═══════════════════════════════════════════════════════════════════════════
# 2. PROBLEM DISCOVERY & BUSINESS CONTEXT
# ═══════════════════════════════════════════════════════════════════════════
P('2. Problem Discovery & Business Context', 'H1')
HR()
P('2.1 Skala Masalah', 'H2')
P(
    'Penyakit kardiovaskular (CVD) adalah penyebab kematian nomor satu di Indonesia dan dunia. '
    'Data epidemiologis dari berbagai sumber internasional dan nasional mengkonfirmasi '
    'skala dan urgensi masalah ini:'
)
SP()

problem_data = [
    ['Statistik', 'Angka', 'Sumber'],
    ['Kematian CVD per tahun (Indonesia)', '~635.000', 'WHO Global Health Estimates 2023'],
    ['Serangan jantung pertama yang langsung fatal', '40%', 'AHA Heart Disease Statistics 2024'],
    ['Biaya perawatan CVD per episode', 'Rp 30–150 juta', 'BPJS Kesehatan Annual Report 2022'],
    ['Penderita yang tidak menyadari risiko', '1 dari 3', 'Riskesdas Biomedis 2019'],
    ['Proporsi kematian total dari CVD', '~17%', 'Riskesdas 2023'],
]
flow.append(tbl(problem_data, [7, 4, 6]))
SP(10)

P('2.2 Tiga Gap yang Pulsevera Isi', 'H2')
gaps = [
    ('Gap 1 — Akses Screening Terbatas',
     'Screening EKG/echocardiogram membutuhkan peralatan khusus (Rp 300K–2,5 juta), '
     'tenaga medis spesialis, dan infrastruktur RS tipe B/C ke atas. Di luar Jawa, '
     'rasio dokter jantung 1:1,2 juta penduduk — jauh di bawah standar WHO (1:100.000).'),
    ('Gap 2 — Kesadaran Rendah di Usia Produktif',
     'Generasi muda (25–34 tahun) cenderung merasa "terlalu muda untuk khawatir." '
     'Tidak ada tools personal, relevan, dan berbasis data yang tersedia untuk segmen ini. '
     'Padahal faktor risiko sudah mulai terbentuk di usia 20-an.'),
    ('Gap 3 — Tidak Ada Early Warning Digital',
     '40% serangan jantung pertama langsung fatal sebelum sempat ke RS. '
     'Tidak ada titik sentuh preventif digital yang personal dan transparan. '
     'Gap ini adalah akibat langsung dari Gap 1 dan Gap 2.'),
]
for title, desc in gaps:
    P(f'<b>{title}</b>', 'H3')
    P(desc)
    SP(4)

P('2.3 Solusi: Pulsevera', 'H2')
P(
    'Pulsevera adalah aplikasi web yang memungkinkan screening mandiri dengan mengisi '
    '10 pertanyaan tentang gaya hidup sehari-hari (tidak memerlukan peralatan medis). '
    'Output berupa: (1) <b>Skor Gaya Hidup 0–5</b> yang actionable, '
    '(2) <b>Estimasi Probabilitas Risiko</b> berbasis model DL, '
    '(3) <b>Rekomendasi personal</b> via Gemini AI. '
    'Seluruh proses selesai dalam kurang dari dua menit, gratis, dan tidak menyimpan data pengguna.'
)
SP()

compare_data = [
    ['Aspek', 'Klinik/RS Konvensional', 'Pulsevera'],
    ['Akses', 'Jadwal dokter, antrian, biaya', 'Browser, gratis, 24/7'],
    ['Waktu', '1–3 jam', '< 2 menit'],
    ['Output', 'Angka klinis (EKG, lipid panel)', 'Skor gaya hidup + rekomendasi actionable'],
    ['Personalisasi', 'Standar (form umum)', 'AI-generated per profil'],
    ['Bahasa', 'Teknis medis', 'Bahasa awam, mudah dipahami'],
    ['Privasi', 'Data disimpan di rekam medis', 'Tidak disimpan, real-time inference'],
]
flow.append(tbl(compare_data, [4, 6.5, 6.5]))
flow.append(PageBreak())


# ═══════════════════════════════════════════════════════════════════════════
# 3. DATASET
# ═══════════════════════════════════════════════════════════════════════════
P('3. Dataset — CDC BRFSS 2022', 'H1')
HR()
P('3.1 Profil Dataset', 'H2')
P(
    'Behavioral Risk Factor Surveillance System (BRFSS) adalah survei telefon rutin yang '
    'dijalankan oleh Centers for Disease Control and Prevention (CDC) Amerika Serikat. '
    'Dataset tahun 2022 dipilih karena: (1) skala besar yang cukup untuk melatih model '
    'DL yang stabil, (2) otoritas sumber yang diakui WHO sebagai benchmark global, '
    '(3) cakupan fitur gaya hidup yang relevan secara universal.'
)
SP()

dataset_stats = [
    ['Atribut', 'Detail'],
    ['Jumlah Sampel', '445.132 responden'],
    ['Jumlah Fitur (asli)', '40 variabel perilaku kesehatan'],
    ['Target Variabel', 'HadHeartAttack (binary: 0/1)'],
    ['Distribusi Target', '5,6% positif (24.971 kasus) — 94,4% negatif'],
    ['Sumber', 'CDC BRFSS 2022 via Kaggle (dataset publik, dapat diverifikasi)'],
    ['Tahun Data', '2022 (survei terakhir yang tersedia publik saat proyek dimulai)'],
    ['Lisensi', 'Public Domain — CC0'],
]
flow.append(tbl(dataset_stats, [5, 12]))
SP(10)

P('3.2 Distribusi Target', 'H2')
P(
    'Class imbalance 5,6% positif merupakan tantangan utama dalam proyek ini. '
    'Visualisasi distribusi target menunjukkan dominasi kelas negatif yang signifikan, '
    'yang jika tidak ditangani akan menyebabkan model bias ke prediksi "tidak berisiko".'
)
SP(4)
flow.append(img(FIGS / 'target_distribution.png', 14, 7))
P('<i>Gambar 3.1. Distribusi target HadHeartAttack — 94,4% negatif, 5,6% positif.</i>', 'Note')
SP(10)

P('3.3 Pemilihan Fitur untuk Form Input', 'H2')
P(
    'Dari 40+ kolom dataset, 10 fitur dipilih untuk form input berdasarkan kriteria: '
    '(1) dapat diketahui sendiri oleh pengguna tanpa peralatan medis, '
    '(2) memiliki SHAP importance yang signifikan, '
    '(3) meminimalkan missing value dari pengguna awam.'
)
SP()

feature_sel = [
    ['#', 'Fitur Form', 'Kolom Dataset', 'SHAP Global Rank', 'Dapat Dimodifikasi?'],
    ['1', 'Kondisi Kesehatan Umum', 'GeneralHealth', '#1 (0.111)', 'Indikator keseluruhan'],
    ['2', 'Usia', 'AgeCategory', '#3 (0.076)', 'Tidak (non-modifiable)'],
    ['3', 'Diabetes', 'HadDiabetes', '#5 (0.058)', 'Dapat dikelola'],
    ['4', 'Konsumsi Alkohol', 'AlcoholDrinkers', '#6 (0.048)', 'Ya'],
    ['5', 'Aktivitas Fisik', 'PhysicalActivities', '#8 (0.039)', 'Ya'],
    ['6', 'Jam Tidur', 'SleepHours', '#15 (0.016)', 'Ya'],
    ['7', 'Status Merokok', 'SmokerStatus', '~#20', 'Ya'],
    ['8', 'Jenis Kelamin', 'Sex', '#16 (0.013)', 'Tidak'],
    ['9', 'Tinggi Badan', 'HeightInMeters', '#12 (0.019)', 'Input BMI'],
    ['10', 'Berat Badan', 'WeightInKilograms', '#18 (0.011)', 'Input BMI'],
]
flow.append(tbl(feature_sel, [0.7, 4.5, 3.5, 3.3, 5]))
SP(6)
P(
    '<b>Catatan:</b> Fitur klinis dengan SHAP tinggi (HadAngina #4, HadStroke) tidak '
    'ditanyakan karena pengguna awam sering tidak mengetahuinya — nilai di-default ke 0 '
    '(tidak ada riwayat), yang merupakan pendekatan konservatif dan aman.',
    'Note',
)
flow.append(PageBreak())


# ═══════════════════════════════════════════════════════════════════════════
# 4. DATA WRANGLING
# ═══════════════════════════════════════════════════════════════════════════
P('4. Data Wrangling & Preprocessing', 'H1')
HR()
P(
    'Pipeline data wrangling dirancang untuk menghasilkan dataset bersih dan konsisten '
    'yang dapat direproduksi. Semua langkah didokumentasikan dalam '
    '<font face="Courier">notebooks/01_data_wrangling.ipynb</font>.'
)
SP()
P('4.1 Langkah-Langkah Preprocessing', 'H2')

wrangling_steps = [
    ['Langkah', 'Aksi', 'Alasan'],
    ['Duplikat', 'Drop 11 baris duplikat identik', 'Menghindari bias training dari data identik'],
    ['Missing Values', 'Imputasi median (numerik), modus (kategorikal)', 'Preservasi distribusi; BRFSS sudah bersih (~0.3% missing)'],
    ['BMI Capping', 'Cap BMI ke [14.51, 40.91] (1st–99th percentile)', 'Menghilangkan outlier ekstrem yang tidak medis-valid'],
    ['Encoding', 'One-hot encoding untuk SmokerStatus & AgeCategory; binary encoding untuk Yes/No', 'Mengubah semua fitur kategorikal ke numerik'],
    ['Scaling', 'StandardScaler (fit pada X_train, transform X_test)', 'DL sensitif terhadap skala fitur; scaler disimpan sebagai scaler.pkl'],
    ['Train/Test Split', '80/20 stratified split; random_state=42', 'Preservasi distribusi class imbalance di kedua set'],
]
flow.append(tbl(wrangling_steps, [3, 4.5, 9.5]))
SP(10)

P('4.2 Distribusi Numerik Sebelum Cleaning', 'H2')
SP(4)
flow.append(img(FIGS / 'numeric_distribution_before_cleaning.png', 17, 8))
P('<i>Gambar 4.1. Distribusi fitur numerik sebelum preprocessing — tampak outlier pada BMI dan SleepHours.</i>', 'Note')
SP(10)

P('4.3 Split Dataset Final', 'H2')
split_data = [
    ['Set', 'Jumlah Sampel', 'Proporsi Positif', 'Keterangan'],
    ['X_train', '356.105', '5,63%', 'Digunakan untuk training + SMOTE'],
    ['X_test', '89.027', '5,64%', 'Hold-out; tidak pernah dilihat selama training'],
    ['Total', '445.132', '5,64%', 'Stratified split mempertahankan rasio class'],
]
flow.append(tbl(split_data, [3, 4, 4, 7]))
flow.append(PageBreak())


# ═══════════════════════════════════════════════════════════════════════════
# 5. EXPLORATORY DATA ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
P('5. Exploratory Data Analysis', 'H1')
HR()
P(
    'EDA dilakukan untuk menjawab 5 pertanyaan bisnis utama yang relevan dengan '
    'konteks deteksi dini risiko jantung. Seluruh analisis tersedia di '
    '<font face="Courier">notebooks/02_eda.ipynb</font>.'
)
SP()

P('5.1 Distribusi Target & Korelasi Fitur', 'H2')
SP(4)
flow.append(img(FIGS / 'heatmap_correlation.png', 17, 9))
P('<i>Gambar 5.1. Heatmap korelasi antar fitur. GeneralHealth dan AgeCategory menunjukkan korelasi tertinggi dengan target.</i>', 'Note')
SP(10)

P('5.2 Q1: Apakah Aktivitas Fisik Berhubungan dengan Risiko Jantung?', 'H2')
SP(4)
flow.append(img(FIGS / 'q1_physical_activity_vs_heart_attack.png', 17, 6))
P('<i>Gambar 5.2. Distribusi risiko jantung berdasarkan aktivitas fisik. Kelompok tidak aktif memiliki proporsi serangan jantung lebih tinggi.</i>', 'Note')
SP(10)

P('5.3 Q2: Bagaimana Distribusi Risiko berdasarkan Usia?', 'H2')
SP(4)
flow.append(img(FIGS / 'q2_age_vs_heart_attack.png', 17, 6))
P('<i>Gambar 5.3. Risiko jantung meningkat drastis pada usia 55+ — justifikasi untuk memasukkan AgeCategory sebagai fitur utama form.</i>', 'Note')
SP(10)

P('5.4 Q3: Dampak Kombinasi Diabetes dan Merokok', 'H2')
SP(4)
flow.append(img(FIGS / 'q3_diabetes_smoke_combination.png', 17, 6))
P('<i>Gambar 5.4. Kombinasi diabetes dan merokok memiliki risiko tertinggi — mendukung keputusan memasukkan kedua fitur ini ke form.</i>', 'Note')
flow.append(PageBreak())

P('5.5 Q4: Hubungan BMI dengan Risiko Jantung', 'H2')
SP(4)
flow.append(img(FIGS / 'q4_bmi_vs_heart_attack.png', 17, 6))
P('<i>Gambar 5.5. BMI lebih tinggi berkorelasi positif dengan risiko — mendukung pembuatan fitur IsObese dan LifestyleRiskScore.</i>', 'Note')
SP(10)

P('5.6 Q5: Kondisi Kesehatan Umum dan Pola Tidur vs Risiko', 'H2')
SP(4)
flow.append(img(FIGS / 'q5_health_sleep_vs_heart_attack.png', 17, 6))
P('<i>Gambar 5.6. Kondisi kesehatan "Buruk/Sangat Buruk" dan sleep deprivation berhubungan dengan risiko lebih tinggi.</i>', 'Note')
SP(10)

P('5.7 Analisis Multivariat: Usia vs Aktivitas Fisik', 'H2')
SP(4)
flow.append(img(FIGS / 'multivariate_age_activity.png', 17, 7))
P('<i>Gambar 5.7. Pola multivariat: usia tua + tidak aktif = risiko tertinggi. Menunjukkan interaksi antar fitur yang non-linear.</i>', 'Note')
flow.append(PageBreak())


# ═══════════════════════════════════════════════════════════════════════════
# 6. FEATURE ENGINEERING
# ═══════════════════════════════════════════════════════════════════════════
P('6. Feature Engineering', 'H1')
HR()
P(
    'Enam fitur baru dibuat berdasarkan domain knowledge medis dan temuan EDA. '
    'Semua fitur divalidasi menggunakan SHAP global importance untuk memastikan '
    'kontribusi statistik yang nyata, bukan sekadar heuristik. '
    'Implementasi tersedia di <font face="Courier">notebooks/03_feature_engineering.ipynb</font>.'
)
SP()

P('6.1 Deskripsi Enam Fitur Baru', 'H2')
fe_data = [
    ['Fitur', 'Formula', 'Tipe', 'Justifikasi Medis'],
    ['BMI', 'berat(kg) / tinggi²(m)', 'Numerik kontinu', 'Indeks komposisi tubuh standar WHO; predictor CVD yang tervalidasi'],
    ['LifestyleRiskScore', 'Sum 5 flag gaya hidup negatif (0–5)', 'Ordinal 0–5', 'Composite indicator; SHAP rank #19 (0.0106) — membuktikan nilai tambah'],
    ['IsObese', 'BMI ≥ 30', 'Binary', 'Flag klinis untuk obesitas; threshold WHO standard'],
    ['IsSleepDeprived', 'SleepHours < 6', 'Binary', 'NIH: tidur < 6 jam meningkatkan risiko CVD 20–30%'],
    ['IsActiveSmoker', 'SmokerStatus ∈ {Current-some, Current-every}', 'Binary', 'Merokok aktif vs. mantan/tidak pernah — perbedaan klinis signifikan'],
    ['HasChronicCondition', 'diabetes ∨ stroke ∨ angina', 'Binary', 'Kondisi komorbid yang diketahui memperbesar risiko CVD'],
]
flow.append(tbl(fe_data, [3.8, 5.2, 2.5, 5.5]))
SP(10)

P('6.2 Distribusi LifestyleRiskScore', 'H2')
SP(4)
flow.append(img(FIGS / 'lifestyle_risk_score.png', 17, 7))
P('<i>Gambar 6.1. Distribusi LifestyleRiskScore 0–5. Skor 0 = tidak ada faktor risiko gaya hidup. Korelasi positif dengan target terlihat jelas.</i>', 'Note')
SP(10)

P('6.3 Top-10 Korelasi Fitur vs Target', 'H2')
SP(4)
flow.append(img(FIGS / 'top10_feature_correlation.png', 17, 6))
P('<i>Gambar 6.2. Top-10 fitur dengan korelasi tertinggi terhadap HadHeartAttack. LifestyleRiskScore masuk daftar — validasi kontribusi feature engineering.</i>', 'Note')
flow.append(PageBreak())


# ═══════════════════════════════════════════════════════════════════════════
# 7. A/B TESTING
# ═══════════════════════════════════════════════════════════════════════════
P('7. A/B Testing — Validasi Hipotesis Epidemiologis', 'H1')
HR()
P(
    'Empat hipotesis diuji secara statistik untuk memvalidasi bahwa fitur-fitur yang '
    'dipilih untuk form input memiliki hubungan yang signifikan dengan target. '
    'Pengujian dilakukan di <font face="Courier">notebooks/04_ab_testing.ipynb</font>.'
)
SP()

P('7.1 Ringkasan Hasil A/B Testing', 'H2')
ab_data = [
    ['Hipotesis', 'Uji Statistik', 'p-value', 'Effect Size', 'Kesimpulan'],
    ['H1: Aktivitas fisik ↓ risiko jantung', 'Mann-Whitney U', '< 0.001', 'Medium (η²=0.023)', 'TOLAK H0 ✓'],
    ['H2: BMI tinggi ↑ risiko jantung', 'Mann-Whitney U', '< 0.001', 'Small-Medium (η²=0.012)', 'TOLAK H0 ✓'],
    ['H3: Merokok aktif ↑ risiko jantung', 'Chi-square', '< 0.001', 'Cramér\'s V = 0.087', 'TOLAK H0 ✓'],
    ['H4: Tidur cukup (≥6 jam) ↓ risiko', 'Mann-Whitney U', '< 0.05', 'Small (η²=0.006)', 'TOLAK H0 ✓'],
]
flow.append(tbl(ab_data, [6.5, 3, 2, 3.5, 3]))
SP(6)
P(
    '<b>Catatan metodologi:</b> Mann-Whitney U dipilih (bukan t-test) karena distribusi '
    'tidak memenuhi asumsi normalitas (uji Shapiro-Wilk). Chi-square untuk H3 karena '
    'kedua variabel kategorikal. Semua pengujian two-tailed dengan α=0.05.',
    'Note',
)
SP(10)

P('7.2 Visualisasi H1: Aktivitas Fisik vs Risiko', 'H2')
SP(4)
flow.append(img(FIGS / 'ab_test_h1_physical_activity.png', 17, 7))
P('<i>Gambar 7.1. Distribusi PhysicalActivities pada kelompok serangan jantung vs tidak. Kelompok dengan aktivitas fisik rendah memiliki proporsi risiko tinggi yang signifikan.</i>', 'Note')
SP(10)

P('7.3 Visualisasi H2: BMI vs Risiko', 'H2')
SP(4)
flow.append(img(FIGS / 'ab_test_h2_bmi.png', 17, 7))
P('<i>Gambar 7.2. Distribusi BMI pada kedua kelompok. Kelompok berisiko memiliki median BMI lebih tinggi secara statistik signifikan.</i>', 'Note')
SP(10)

P('7.4 Implikasi untuk Model', 'H2')
P(
    'Semua 4 hipotesis terkonfirmasi signifikan. Ini berarti fitur-fitur yang dimasukkan '
    'ke form input (aktivitas fisik, BMI, merokok, tidur) tidak dipilih secara arbitrer — '
    'melainkan terbukti secara statistik berpengaruh pada target. '
    'Temuan ini juga mendukung desain LifestyleRiskScore sebagai composite indicator '
    'yang mencakup semua 4 dimensi gaya hidup yang telah divalidasi.'
)
flow.append(PageBreak())


# ═══════════════════════════════════════════════════════════════════════════
# 8. ML BASELINE MODELING
# ═══════════════════════════════════════════════════════════════════════════
P('8. ML Baseline Modeling', 'H1')
HR()
P(
    'Tiga model baseline dilatih dan dievaluasi untuk menentukan benchmark performa '
    'sebelum menggunakan Deep Learning. Semua model menggunakan preprocessing yang sama '
    '(StandardScaler) dan dievaluasi pada X_test yang sama.'
)
SP()

P('8.1 Perbandingan Model Baseline vs Deep Learning', 'H2')

lr  = ML['Logistic Regression']
dt  = ML['Decision Tree']
rf  = ML['Random Forest']

benchmark_data = [
    ['Model', 'Accuracy', 'Recall', 'Precision', 'F1', 'ROC-AUC', 'Train Time'],
    ['Logistic Regression',
     f'{lr["accuracy"]*100:.1f}%', f'{lr["recall_pos"]*100:.1f}%',
     f'{lr["precision_pos"]*100:.1f}%', f'{lr["f1_pos"]*100:.1f}%',
     f'{lr["roc_auc"]:.4f}', f'{lr["train_seconds"]:.0f}s'],
    ['Decision Tree',
     f'{dt["accuracy"]*100:.1f}%', f'{dt["recall_pos"]*100:.1f}%',
     f'{dt["precision_pos"]*100:.1f}%', f'{dt["f1_pos"]*100:.1f}%',
     f'{dt["roc_auc"]:.4f}', f'{dt["train_seconds"]:.0f}s'],
    ['Random Forest',
     f'{rf["accuracy"]*100:.1f}%', f'{rf["recall_pos"]*100:.1f}%',
     f'{rf["precision_pos"]*100:.1f}%', f'{rf["f1_pos"]*100:.1f}%',
     f'{rf["roc_auc"]:.4f}', f'{rf["train_seconds"]:.0f}s'],
    ['DL + SMOTE (Final)',
     f'{DL["test_accuracy"]*100:.1f}%', f'{DL["test_recall_pos"]*100:.1f}%',
     f'{DL["test_precision_pos"]*100:.1f}%', f'{DL["test_f1_pos"]*100:.1f}%',
     f'{DL["test_roc_auc"]:.4f}', '~300s'],
]
bench_tbl = tbl(benchmark_data, [4.5, 2.5, 2.5, 2.5, 2, 2.5, 2.5],
    extra_style=[
        ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#EEF2FF')),
        ('FONTNAME',   (0, 4), (-1, 4), 'Helvetica-Bold'),
        ('TEXTCOLOR',  (1, 4), (1, 4), EMERALD),
        ('TEXTCOLOR',  (2, 4), (2, 4), EMERALD),
        ('TEXTCOLOR',  (6, 4), (6, 4), EMERALD),
    ])
flow.append(bench_tbl)
SP(8)

P(
    f'<b>Kenapa Random Forest (Accuracy {rf["accuracy"]*100:.1f}%) tidak dipilih?</b> '
    f'Accuracy Random Forest tampak tinggi karena model memprediksi mayoritas kelas (tidak berisiko). '
    f'Recall-nya hanya {rf["recall_pos"]*100:.1f}% — artinya dari 100 orang berisiko, RF hanya '
    f'mendeteksi {rf["recall_pos"]*100:.0f}. Untuk medical screening, False Negative (gagal deteksi '
    f'orang berisiko) jauh lebih berbahaya dari False Positive. '
    f'Deep Learning dengan SMOTE mendeteksi {DL["test_recall_pos"]*100:.0f} dari 100 orang berisiko '
    f'sambil mempertahankan Accuracy {DL["test_accuracy"]*100:.1f}% dan ROC-AUC tertinggi.',
)
SP(10)

P('8.2 Visualisasi Perbandingan Model', 'H2')
SP(4)
flow.append(img(FIGS / 'ml_model_comparison.png', 17, 7))
P('<i>Gambar 8.1. Perbandingan metrik semua model. Kolom Recall adalah metrik kritis — DL+SMOTE unggul signifikan.</i>', 'Note')
SP(10)

P('8.3 ROC Curve Comparison', 'H2')
SP(4)
flow.append(img(FIGS / 'ml_roc_curves.png', 14, 8))
P('<i>Gambar 8.2. ROC curve semua model. Area di bawah kurva (AUC) DL+SMOTE = 0.8812, tertinggi di antara semua model.</i>', 'Note')
flow.append(PageBreak())


# ═══════════════════════════════════════════════════════════════════════════
# 9. DEEP LEARNING
# ═══════════════════════════════════════════════════════════════════════════
P('9. Deep Learning — Arsitektur & Training', 'H1')
HR()
P('9.1 Arsitektur Model', 'H2')
P(
    'Model menggunakan TensorFlow Functional API dengan arsitektur feedforward '
    'yang dirancang khusus untuk data tabular dengan class imbalance ekstrem. '
    'Setiap layer tersusun atas Dense → BatchNormalization → Dropout untuk '
    'stabilitas training dan regularisasi.'
)
SP()

arch_data = [
    ['Layer', 'Konfigurasi', 'Fungsi'],
    ['Input', '46 fitur (setelah encoding & engineering)', 'Terima feature vector yang sudah di-scale'],
    ['Dense 1', '256 unit, ReLU', 'Transformasi high-level — cukup lebar untuk 46 fitur'],
    ['BatchNorm 1', 'Momentum=0.99, Epsilon=0.001', 'Stabilisasi distribusi aktivasi antar batch'],
    ['Dropout 1', 'rate=0.30', 'Regularisasi — mencegah co-adaptation antar neuron'],
    ['Dense 2', '128 unit, ReLU', 'Kompresi hierarchical — representasi mid-level'],
    ['BatchNorm 2', 'Momentum=0.99, Epsilon=0.001', 'Normalisasi ulang setelah non-linearity'],
    ['Dropout 2', 'rate=0.30', 'Regularisasi ke-2'],
    ['Dense 3', '64 unit, ReLU', 'Representasi compact — abstraksi high-order'],
    ['BatchNorm 3', 'Momentum=0.99, Epsilon=0.001', 'Normalisasi final sebelum output'],
    ['Dropout 3', 'rate=0.30', 'Regularisasi ke-3'],
    ['Output', '1 unit, Sigmoid', 'Probabilitas kelas positif ∈ [0, 1]'],
]
flow.append(tbl(arch_data, [2.5, 6, 8.5]))
SP(10)

P('9.2 Komponen Custom', 'H2')
P(
    '<b>Focal Loss (γ=2.0, α=0.25):</b> '
    'Standard binary cross-entropy memberi bobot sama untuk semua sampel, '
    'sehingga model terdistorsi oleh easy negatives (sampel negatif yang mudah diprediksi, '
    'mendominasi dataset 94,4%). Focal Loss menambahkan faktor penalti '
    '(1-p_t)^γ yang secara otomatis mengurangi kontribusi easy examples dan '
    'memfokuskan training pada hard examples (positif yang sulit terdeteksi).'
)
SP()
P(
    '<b>EarlyStoppingByRecall (patience=10):</b> '
    'Standard EarlyStopping berbasis val_loss atau val_accuracy tidak cocok untuk '
    'imbalanced dataset karena keduanya dapat membaik hanya dengan memprediksi lebih '
    'banyak negatif. Custom callback ini memonitor val_recall dan menghentikan '
    'training jika recall tidak membaik dalam 10 epoch berturut-turut — '
    'memastikan model tidak "mundur" ke perilaku prediksi mayoritas.'
)
SP(10)

P('9.3 Strategi Handling Class Imbalance (4 Lapis)', 'H2')
imbalance_data = [
    ['Strategi', 'Detail', 'Efek pada Training'],
    ['SMOTE', 'sampling_strategy=0.3; oversampling minoritas ke 30% dari mayoritas', 'Training set lebih seimbang; model "melihat" lebih banyak contoh positif'],
    ['class_weight balanced', f'class 0: {DL["class_weight"]["0"]:.4f}, class 1: {DL["class_weight"]["1"]:.4f}', 'Loss untuk setiap prediksi positif yang salah dikalikan 2.17x lebih tinggi'],
    ['Focal Loss', 'γ=2.0, α=0.25 — penalti lebih besar untuk easy negatives', 'Fokus gradient pada hard-to-classify cases (positif)'],
    ['Threshold Tuning', 'Default 0.5 → 0.23 berdasarkan sweep eksperimental', 'Recall ↑ dari ~30% ke 71.15% tanpa retraining'],
]
flow.append(tbl(imbalance_data, [4, 6.5, 6.5]))
SP(10)

P('9.4 Hyperparameter Training', 'H2')
hp_data = [
    ['Parameter', 'Nilai', 'Justifikasi'],
    ['Optimizer', 'Adam (lr=1e-3)', 'Default yang stabil untuk tabular data; lr tidak diturunkan (ReduceLROnPlateau menyebabkan collapse ke all-negative)'],
    ['Batch size', '512', 'Keseimbangan antara kecepatan (besar) dan generalisasi (tidak terlalu besar)'],
    ['Max Epochs', '50', 'EarlyStoppingByRecall biasanya berhenti lebih awal (~25-35 epoch)'],
    ['Validation split', '0.20', 'Split dari X_train (setelah SMOTE); tidak mencemari test set'],
    ['Initialization', 'he_normal', 'Optimal untuk ReLU activation (Xavier tidak cocok)'],
    ['Random state', '42', 'Reproduksibilitas: numpy, TensorFlow, SMOTE, sklearn'],
]
flow.append(tbl(hp_data, [3.5, 4, 9.5]))
flow.append(PageBreak())


# ═══════════════════════════════════════════════════════════════════════════
# 10. EVALUASI & THRESHOLD
# ═══════════════════════════════════════════════════════════════════════════
P('10. Evaluasi Model & Threshold Tuning', 'H1')
HR()
P('10.1 Hasil Akhir Model DL + SMOTE', 'H2')

final_metrics = [
    ['Metrik', 'Nilai', 'Target Program', 'Status'],
    ['Accuracy', f'{DL["test_accuracy"]*100:.2f}%', '≥ 85%', 'LULUS ✓'],
    ['Recall (Kelas Positif)', f'{DL["test_recall_pos"]*100:.2f}%', '≥ 70%', 'LULUS ✓'],
    ['Precision (Kelas Positif)', f'{DL["test_precision_pos"]*100:.2f}%', '-', 'Dibatasi imbalance'],
    ['F1 Score (Kelas Positif)', f'{DL["test_f1_pos"]*100:.2f}%', '-', 'Matematically constrained'],
    ['ROC-AUC', f'{DL["test_roc_auc"]:.4f}', '≥ 0.80', 'LULUS ✓'],
    ['Threshold Operasional', f'{DL["best_threshold"]}', 'Sweet spot', 'DISEPAKATI ✓'],
]
flow.append(tbl(final_metrics, [5.5, 3.5, 3.5, 5],
    extra_style=[
        ('BACKGROUND', (3, 1), (3, 2), colors.HexColor('#C6F6D5')),
        ('BACKGROUND', (3, 5), (3, 5), colors.HexColor('#C6F6D5')),
        ('BACKGROUND', (3, 3), (3, 4), colors.HexColor('#FEF5E7')),
    ]))
SP(6)
P(
    f'<b>Catatan F1:</b> {DL["f1_note"]}',
    'Note',
)
SP(10)

P('10.2 Justifikasi Threshold 0.23', 'H2')
P(
    'Threshold default 0.5 berasumsi distribusi prediksi seimbang. Setelah SMOTE mengubah '
    'distribusi training, output probabilitas model tidak lagi terkalibrasi ke 0.5. '
    'Threshold 0.23 ditemukan melalui eksperimen sistematis (sweep 0.05–0.50 dengan step 0.005) '
    'dan disepakati tim sebagai nilai yang memenuhi kedua target program sekaligus:'
)
SP(4)

thresh_compare = [
    ['Threshold', 'Accuracy', 'Recall', 'Keterangan'],
    ['0.50 (default)', '~91%', '~30%', 'Terlalu bias ke mayoritas — 70 dari 100 orang berisiko terlewat'],
    ['0.23 (operasional)', f'{DL["test_accuracy"]*100:.2f}%', f'{DL["test_recall_pos"]*100:.2f}%', 'Sweet spot: memenuhi Acc ≥85% DAN Recall ≥70%'],
    ['0.10 (terlalu rendah)', '~60%', '~90%+', 'Terlalu banyak false positive — tidak praktis'],
]
flow.append(tbl(thresh_compare, [3.5, 3.5, 3.5, 7],
    extra_style=[('BACKGROUND', (0, 2), (-1, 2), LIGHT)]))
SP(10)

P('10.3 Kurva Threshold', 'H2')
SP(4)
flow.append(img(REPORTS / 'fig_threshold_curves.png', 17, 7))
P('<i>Gambar 10.1. Kurva metrik vs threshold. Garis hijau putus-putus menunjukkan sweet spot @ 0.23 yang memenuhi target Acc ≥85% dan Recall ≥70%.</i>', 'Note')
SP(10)

P('10.4 Confusion Matrix', 'H2')
SP(4)
flow.append(img(REPORTS / 'fig_confusion_matrix.png', 13, 9.5))
P('<i>Gambar 10.2. Confusion matrix pada threshold 0.23. TP = orang berisiko yang berhasil dideteksi; FN = orang berisiko yang terlewat (paling berbahaya).</i>', 'Note')
flow.append(PageBreak())


# ═══════════════════════════════════════════════════════════════════════════
# 11. SHAP INTERPRETABILITY
# ═══════════════════════════════════════════════════════════════════════════
P('11. SHAP Interpretability', 'H1')
HR()
P(
    'SHAP (SHapley Additive exPlanations) digunakan untuk menjelaskan output model '
    'secara ilmiah dan transparan. Berbeda dari feature importance tradisional, SHAP '
    'memberikan kontribusi per-fitur per-instance dengan arah (positif/negatif), '
    'membuatnya menjadi standar de facto untuk explainable AI di industri dan riset.'
)
SP()

P('11.1 Metodologi SHAP', 'H2')
shap_method = [
    ['Aspek', 'Detail'],
    ['Explainer type', 'TreeExplainer (efisien untuk tree-based model Random Forest yang digunakan untuk SHAP pre-computation)'],
    ['Sample size', f'{SHAP["sample_size"]} sampel dari training set (representatif, menghemat compute time dari >7000ms → 350ms)'],
    ['Computation', 'Pre-computed global importance; bukan per-request real-time (optimasi inference time produksi)'],
    ['Output format', 'Mean absolute SHAP value per fitur (global) + top-3 per prediction (instance-level di API)'],
]
flow.append(tbl(shap_method, [4, 13]))
SP(10)

P('11.2 Top-10 Global SHAP Importance', 'H2')
shap_top10 = list(SHAP['global_importance_top10'].items())
shap_data = [['Rank', 'Fitur', 'SHAP Mean |Value|', 'Interpretasi']]
interpretations = {
    'GeneralHealth':   'Kondisi kesehatan umum — strongest predictor; mencakup status kesehatan holistic',
    'RemovedTeeth':    'Proxy socioeconomic & overall health decay; correlates dengan CVD risk factors',
    'AgeCategory':     'Non-modifiable risk factor; risiko meningkat eksponensial setelah usia 55',
    'HadAngina':       'Gejala klinis langsung berhubungan dengan CAD (coronary artery disease)',
    'HadDiabetes':     'Diabetes meningkatkan risiko CVD 2–4x; masuk form sebagai input utama',
    'AlcoholDrinkers': 'Konsumsi alkohol — dual effect (moderate protective, heavy harmful)',
    'Race_White only, Non-Hispanic': 'Demografis dataset CDC BRFSS; tidak dimasukkan ke form (US-specific)',
    'PhysicalActivities': 'Aktivitas fisik — salah satu modifiable factor paling kuat',
    'HIVTesting':      'Proxy akses healthcare dan health-conscious behavior',
    'CovidPos':        'Riwayat COVID-19 meningkatkan risiko kardiovaskular jangka panjang',
}
for i, (feat, val) in enumerate(shap_top10, 1):
    shap_data.append([str(i), feat, f'{val:.4f}', interpretations.get(feat, '-')])
flow.append(tbl(shap_data, [1, 5.5, 3.5, 7]))
SP(6)
P(f'<b>LifestyleRiskScore</b> (fitur engineered) berada di posisi #19 dengan SHAP value 0.0106 — '
  f'membuktikan bahwa composite feature yang dibuat tim DS memberikan kontribusi statistik nyata.',
  'Note')
SP(10)

P('11.3 SHAP Summary Bar Plot', 'H2')
SP(4)
flow.append(img(REPORTS / 'shap_summary_bar.png', 17, 8))
P('<i>Gambar 11.1. SHAP global importance (mean absolute value). GeneralHealth mendominasi dengan SHAP 0.111.</i>', 'Note')
SP(10)

P('11.4 SHAP Beeswarm Plot', 'H2')
SP(4)
flow.append(img(REPORTS / 'shap_summary_beeswarm.png', 17, 9))
P('<i>Gambar 11.2. SHAP beeswarm — setiap titik = satu sample. Warna merah = nilai fitur tinggi, biru = rendah. Menunjukkan arah dan dispersi pengaruh per fitur.</i>', 'Note')
SP(10)

P('11.5 SHAP Dependence Plot: GeneralHealth', 'H2')
SP(4)
flow.append(img(REPORTS / 'shap_dependence_generalhealth.png', 14, 7))
P('<i>Gambar 11.3. Dependence plot GeneralHealth. Semakin buruk kondisi kesehatan umum (nilai lebih tinggi = lebih buruk), semakin besar SHAP contribution ke prediksi risiko.</i>', 'Note')
flow.append(PageBreak())


# ═══════════════════════════════════════════════════════════════════════════
# 12. ARSITEKTUR SISTEM
# ═══════════════════════════════════════════════════════════════════════════
P('12. Arsitektur Sistem & Deployment', 'H1')
HR()
P('12.1 Three-Layer Architecture', 'H2')
P(
    'Pulsevera menggunakan arsitektur tiga lapis yang memisahkan concern UI, '
    'business logic, dan ML inference. Pemisahan ini penting untuk keamanan '
    '(frontend tidak perlu tahu URL ML API), skalabilitas, dan maintainability.'
)
SP()

arch_sys = [
    ['Layer', 'Teknologi', 'Port', 'Tanggung Jawab'],
    ['Frontend', 'React 18 + Vite + Tailwind CSS', '5173 (dev)', 'UI, routing, form validation, visualisasi hasil, Axios calls'],
    ['Backend (Proxy)', 'Express.js + Node.js', '3001', 'Proxy aman ke ML API, CORS management, rate limiting, error handling'],
    ['ML API', 'FastAPI + Python 3.12', '8000', 'Preprocessing, DL inference, SHAP attribution, Gemini integration'],
]
flow.append(tbl(arch_sys, [2.5, 4.5, 2.5, 8]))
SP(10)

P('12.2 Alur Data End-to-End', 'H2')
P(
    '<font face="Courier" size="8">'
    'User Browser<br/>'
    '  ↓ (HTTPS POST + JSON form data)<br/>'
    'React Frontend (Vite + Tailwind)<br/>'
    '  ↓ (Axios POST /api/predict)<br/>'
    'Express.js Backend (proxy + CORS middleware)<br/>'
    '  ↓ (HTTP POST /predict)<br/>'
    'FastAPI ML API<br/>'
    '  ├── Pydantic validation (46 field types + ranges)<br/>'
    '  ├── Preprocessing (one-hot encode + StandardScaler.transform)<br/>'
    '  ├── DL Model Inference (keras .predict, batch=1)<br/>'
    '  ├── SHAP Attribution (pre-computed lookup by profile)<br/>'
    '  └── Gemini AI Recommendation (prompt engineering + fallback rule-based)<br/>'
    '  ↓ (JSON Response: risk_score, lifestyle, top_factors, recommendations)<br/>'
    'React ResultPage (Lifestyle Score + Risk Gauge + Recommendations)<br/>'
    '</font>',
)
SP(10)

P('12.3 Inferensi API', 'H2')
api_specs = [
    ['Endpoint', 'Method', 'Input', 'Output'],
    ['/predict', 'POST', 'JSON: 10 field dari form user', 'risk_score, lifestyle{score, habits}, top_risk_factors, recommendations'],
    ['/health', 'GET', '-', 'status: ok, model: loaded, inference_ready'],
]
flow.append(tbl(api_specs, [2.5, 2, 5.5, 8]))
SP(10)

P('12.4 Performa Inferensi', 'H2')
perf_data = [
    ['Komponen', 'Waktu', 'Keterangan'],
    ['Preprocessing', '~15ms', 'Pandas + numpy, single sample'],
    ['DL forward pass', '~50ms', 'Keras .predict, batch=1'],
    ['SHAP lookup', '~5ms', 'Pre-computed — bukan real-time calculation (dari 7000ms → 5ms)'],
    ['Gemini API (jika aktif)', '~280ms', 'Network latency ke Gemini API'],
    ['Total (dengan Gemini)', '~350ms', 'Sangat acceptable untuk web app (target < 1000ms)'],
    ['Total (tanpa Gemini)', '~70ms', 'Fallback rule-based recommendation'],
]
flow.append(tbl(perf_data, [4, 2.5, 10.5]))
SP(10)

P('12.5 Target Deployment', 'H2')
deploy_data = [
    ['Komponen', 'Platform Target', 'Tier', 'Catatan'],
    ['ML API (FastAPI)', 'Hugging Face Spaces', 'Free', 'Support Python + TensorFlow; 2 CPU, 16GB RAM'],
    ['Backend (Express)', 'Railway atau Render', 'Free tier', 'Auto-deploy dari GitHub; custom domain tersedia'],
    ['Frontend (React)', 'Vercel atau Netlify', 'Free tier', 'CI/CD otomatis; CDN global'],
]
flow.append(tbl(deploy_data, [4, 4, 2.5, 7]))
flow.append(PageBreak())


# ═══════════════════════════════════════════════════════════════════════════
# 13. LIMITASI & RENCANA
# ═══════════════════════════════════════════════════════════════════════════
P('13. Limitasi & Rencana ke Depan', 'H1')
HR()
P('13.1 Limitasi Saat Ini', 'H2')

limitations = [
    ('Dataset Bias',
     'CDC BRFSS 2022 adalah survei populasi dewasa Amerika Serikat. Faktor demografis '
     'spesifik AS (ras, sistem kesehatan, diet) mungkin tidak sepenuhnya representatif '
     'untuk populasi Indonesia. Fitur demografis AS-spesifik (ras) tidak dimasukkan ke form.'),
    ('Class Imbalance Residual',
     f'Precision masih rendah ({DL["test_precision_pos"]*100:.1f}%) — artinya tingkat false '
     f'positive cukup tinggi. Dalam konteks screening, ini dapat diterima karena false positive '
     'dapat diverifikasi dokter, sementara false negative berbahaya. Namun pengalaman UX '
     'pengguna yang sering mendapat "false alarm" perlu dipertimbangkan.'),
    ('Input Terbatas (10 Fitur)',
     'Fitur klinis dengan SHAP importance tinggi (HadAngina #4, HadStroke) tidak ditanyakan '
     'untuk alasan UX — pengguna awam sering tidak mengetahui riwayat angina. '
     'Nilai di-default ke 0 (tidak ada riwayat), yang konservatif tapi mengurangi akurasi '
     'untuk pengguna dengan riwayat klinis yang relevan.'),
    ('Tidak Ada Validasi Klinis',
     'Model belum divalidasi oleh tenaga medis profesional (dokter spesialis jantung). '
     'Tidak ada uji klinis prospektif yang membandingkan hasil Pulsevera dengan '
     'diagnosis dokter. Disclaimer "bukan pengganti dokter" harus selalu dipertahankan.'),
    ('No Longitudinal Data',
     'Dataset BRFSS adalah cross-sectional — tidak dapat melacak perubahan risiko '
     'individu dari waktu ke waktu. Pulsevera tidak dapat memberikan analisis '
     '"risiko Anda menurun 15% sejak 3 bulan lalu" tanpa fitur history tracking.'),
]
for title, desc in limitations:
    P(f'<b>{title}:</b> {desc}', 'LIM')
SP(10)

P('13.2 Rencana Pengembangan', 'H2')
roadmap_data = [
    ['Horizon', 'Inisiatif', 'Dampak'],
    ['Short-term (0–3 bulan)',
     'History tracking (opsional, opt-in)\nHalaman edukasi CVD\nOptimasi mobile UX',
     'Retensi user; edukasi berkelanjutan'],
    ['Mid-term (3–6 bulan)',
     'Kolaborasi validasi klinis (FKTP/puskesmas)\nDataset Indonesia untuk fine-tuning\nXGBoost + DL ensemble',
     'Kepercayaan medis; relevansi lokal'],
    ['Long-term (6–12 bulan)',
     'API integrasi sistem rekam medis (ICD-10)\nMobile app (React Native)\nKemitraan BPJS program preventif',
     'Dampak sistemik pada kesehatan publik'],
]
flow.append(tbl(roadmap_data, [4, 7.5, 6]))
SP(20)

HR()
SP(6)
P(
    f'<i>Laporan ini dihasilkan secara otomatis dari '
    f'<font face="Courier">ml-api/generate_comprehensive_report.py</font>.<br/>'
    f'Dataset: CDC BRFSS 2022 · Model: DL+SMOTE @ threshold {DL["best_threshold"]} · '
    f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}<br/>'
    f'Pulsevera · CC26-PRU439 · DBS Foundation Coding Camp 2026</i>',
    'Note',
)

doc.build(flow)
print(f'PDF report generated: {pdf_path}')
print(f'Size: {pdf_path.stat().st_size / 1024:.1f} KB')
