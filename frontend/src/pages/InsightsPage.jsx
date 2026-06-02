import React from 'react'
import { motion } from 'framer-motion'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell,
} from 'recharts'
import {
  ArrowLeft, Heart, AlertTriangle, Info, Activity,
  HeartPulse, Stethoscope, TrendingUp, ArrowRight,
  BarChart2, BookOpen, Sparkles,
} from 'lucide-react'

// ── Static data ───────────────────────────────────────────────────────────────

const INDONESIA_STATS = [
  {
    value: '635.000',
    unit: 'kematian/tahun',
    label: 'akibat penyakit kardiovaskular di Indonesia',
    source: 'WHO 2023',
    color: 'coral',
  },
  {
    value: '40%',
    unit: 'serangan fatal',
    label: 'terjadi sebelum pasien sempat mencapai rumah sakit',
    source: 'AHA 2024',
    color: 'coral',
  },
  {
    value: '1 dari 3',
    unit: 'penderita',
    label: 'tidak menyadari faktor risiko jantung mereka',
    source: 'Riskesdas 2019',
    color: 'amber',
  },
  {
    value: 'Rp 30–150 jt',
    unit: 'per episode',
    label: 'biaya perawatan CVD; 10-50x lebih mahal dari pencegahan',
    source: 'BPJS 2022',
    color: 'amber',
  },
]

// SHAP global importance dari shap_metadata.json (top-10)
const SHAP_DATA = [
  { name: 'Kondisi Kesehatan Umum', shap: 0.111, inForm: true },
  { name: 'Kesehatan Gigi (Proxy)', shap: 0.080, inForm: false },
  { name: 'Kategori Usia', shap: 0.076, inForm: true },
  { name: 'Riwayat Angina', shap: 0.063, inForm: false },
  { name: 'Diabetes', shap: 0.058, inForm: true },
  { name: 'Konsumsi Alkohol', shap: 0.048, inForm: true },
  { name: 'Aktivitas Fisik', shap: 0.039, inForm: true },
  { name: 'Jam Tidur', shap: 0.016, inForm: true },
  { name: 'Jenis Kelamin', shap: 0.013, inForm: true },
  { name: 'Skor Gaya Hidup*', shap: 0.011, inForm: false },
]

const CLINICAL_FACTORS = [
  {
    label: 'Angina Pektoris (Nyeri Dada)',
    rank: 'SHAP #4',
    desc: 'Nyeri dada saat aktivitas fisik adalah tanda khas penyakit arteri koroner. SHAP importance #4 membuktikan ini adalah prediktor kuat, namun tidak kami tanyakan karena membutuhkan diagnosis dokter.',
    action: 'Jika pernah mengalami nyeri dada saat aktivitas, segera konsultasikan ke dokter jantung.',
    icon: HeartPulse,
  },
  {
    label: 'Riwayat Stroke',
    rank: 'Komorbid',
    desc: 'Stroke dan serangan jantung berbagi faktor risiko yang sama: hipertensi, aterosklerosis, diabetes, dan gaya hidup sedentari. Riwayat stroke meningkatkan risiko kejadian kardiovaskular berikutnya.',
    action: 'Penderita riwayat stroke perlu monitoring kardiovaskular intensif.',
    icon: Activity,
  },
  {
    label: 'Penyakit Paru Obstruktif (COPD)',
    rank: 'Komorbid',
    desc: 'Inflamasi kronik pada COPD meningkatkan beban kerja jantung kanan dan mempercepat aterosklerosis sistemik. Hubungan COPD–CVD sering diremehkan.',
    action: 'Penderita COPD dianjurkan evaluasi kardiovaskular rutin minimal 1× per tahun.',
    icon: Stethoscope,
  },
  {
    label: 'Penyakit Ginjal Kronis',
    rank: 'Komorbid',
    desc: 'Hubungan dua arah yang kuat: kerusakan ginjal dan jantung saling memperburuk melalui retensi cairan, tekanan darah, dan inflamasi sistemik.',
    action: 'Periksa fungsi ginjal (creatinine, GFR) secara rutin jika ada riwayat hipertensi atau diabetes.',
    icon: HeartPulse,
  },
  {
    label: 'Kesehatan Gigi & Mulut',
    rank: 'SHAP #2',
    desc: 'Mengejutkan: SHAP importance #2 (0.080). Riset AHA menunjukkan bakteri periodontal memicu inflamasi arteri koroner. Gigi yang tidak sehat adalah proxy kesehatan sistemik secara keseluruhan.',
    action: 'Perawatan gigi rutin (scaling & pemeriksaan 6 bulan sekali) adalah bagian dari kesehatan jantung.',
    icon: TrendingUp,
  },
]

// ── Custom recharts tooltip ───────────────────────────────────────────────────

function SHAPTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const item = payload[0].payload
  return (
    <div className="rounded-2xl bg-white p-3 shadow-soft ring-1 ring-pulse-100 text-xs max-w-[200px]">
      <p className="font-bold text-ink-900 mb-1">{item.name}</p>
      <p className="text-pulse-700 font-mono">SHAP: {item.shap.toFixed(4)}</p>
      <p className={`mt-1 ${item.inForm ? 'text-mint-700' : 'text-slate-500'}`}>
        {item.inForm ? '✓ Ada di form screening' : 'Tidak di form (perlu dokter)'}
      </p>
    </div>
  )
}

// ── Stat card colors ─────────────────────────────────────────────────────────

const STAT_COLOR = {
  coral: 'bg-coral-50 ring-coral-200 text-coral-900',
  amber: 'bg-amber-50 ring-amber-200 text-amber-900',
}

// ── Page ─────────────────────────────────────────────────────────────────────

export default function InsightsPage({ onBack, onCheckRisk }) {
  return (
    <div className="min-h-screen bg-gradient-pulse">
      {/* ── Header ── */}
      <header className="sticky top-0 z-50 border-b border-white/40 bg-white/70 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3 sm:px-6">
          <button onClick={onBack} className="btn-secondary">
            <ArrowLeft size={16} />
            Beranda
          </button>
          <div className="flex items-center gap-2 font-display font-bold">
            <span className="grid h-8 w-8 place-items-center rounded-xl bg-gradient-to-br from-pulse-600 to-pulse-800 text-white">
              <Heart size={15} fill="white" strokeWidth={0} />
            </span>
            <span className="hidden sm:inline">Pulsevera</span>
          </div>
          <button onClick={onCheckRisk} className="btn-primary">
            Cek Risiko
            <ArrowRight size={16} />
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
        {/* ── Hero ── */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12 text-center"
        >
          <span className="badge mb-4">
            <BarChart2 size={12} />
            Wawasan Data
          </span>
          <h1 className="font-display text-4xl sm:text-5xl font-bold tracking-tight mb-4">
            Wawasan Risiko Jantung
          </h1>
          <p className="mx-auto max-w-2xl text-ink-900/70 leading-relaxed">
            Data & insight dari CDC BRFSS 2022 (445.132 responden) dan analisis SHAP model Pulsevera.
            Pahami faktor apa yang paling berpengaruh, serta mengapa deteksi dini itu penting.
          </p>
        </motion.div>

        {/* ── SECTION 1: Statistik Indonesia ── */}
        <section className="mb-16">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <div className="flex items-center gap-3 mb-6">
              <span className="grid h-10 w-10 place-items-center rounded-2xl bg-coral-500/10 text-coral-600">
                <AlertTriangle size={20} />
              </span>
              <div>
                <h2 className="font-display text-2xl font-bold">Skala Masalah di Indonesia</h2>
                <p className="text-sm text-ink-900/60">Penyakit jantung adalah pembunuh #1, dan sebagian besar dapat dicegah</p>
              </div>
            </div>

            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {INDONESIA_STATS.map((stat, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.15 + i * 0.08 }}
                  className={`rounded-3xl p-6 ring-1 ${STAT_COLOR[stat.color]}`}
                >
                  <p className="font-display text-4xl font-bold mb-1">{stat.value}</p>
                  <p className="text-sm font-semibold mb-2">{stat.unit}</p>
                  <p className="text-xs leading-snug opacity-80">{stat.label}</p>
                  <p className="mt-3 text-[10px] font-mono opacity-60">Sumber: {stat.source}</p>
                </motion.div>
              ))}
            </div>

            <div className="mt-5 rounded-2xl bg-white/80 p-4 ring-1 ring-pulse-100 flex gap-3 items-start">
              <Info size={18} className="text-pulse-600 shrink-0 mt-0.5" />
              <p className="text-sm text-ink-900/80 leading-relaxed">
                <strong>Fakta penting:</strong> Penyakit jantung sangat <em>preventable</em>: 80%
                kematian CVD prematur dapat dicegah dengan gaya hidup sehat dan deteksi dini.
                Namun mayoritas orang tidak menyadari risikonya sampai sudah terlambat.
              </p>
            </div>
          </motion.div>
        </section>

        {/* ── SECTION 2: SHAP Risk Factors ── */}
        <section className="mb-16">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <div className="flex items-center gap-3 mb-6">
              <span className="grid h-10 w-10 place-items-center rounded-2xl bg-pulse-100 text-pulse-700">
                <TrendingUp size={20} />
              </span>
              <div>
                <h2 className="font-display text-2xl font-bold">Top 10 Faktor Risiko</h2>
                <p className="text-sm text-ink-900/60">Berdasarkan SHAP global importance model Pulsevera (CDC BRFSS 2022)</p>
              </div>
            </div>

            <div className="glass rounded-3xl p-6 sm:p-8">
              {/* Legend */}
              <div className="flex flex-wrap gap-4 mb-6 text-xs">
                <div className="flex items-center gap-2">
                  <span className="h-3 w-3 rounded-sm bg-pulse-600" />
                  <span className="text-ink-900/80">Ada di form screening Pulsevera</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="h-3 w-3 rounded-sm bg-slate-400" />
                  <span className="text-ink-900/80">Tidak di form (konsultasi dokter)</span>
                </div>
              </div>

              <ResponsiveContainer width="100%" height={340}>
                <BarChart
                  data={SHAP_DATA}
                  layout="vertical"
                  margin={{ left: 4, right: 40, top: 4, bottom: 4 }}
                >
                  <XAxis
                    type="number"
                    domain={[0, 0.12]}
                    tickFormatter={(v) => v.toFixed(3)}
                    tick={{ fontSize: 11 }}
                    tickLine={false}
                    axisLine={false}
                  />
                  <YAxis
                    type="category"
                    dataKey="name"
                    width={175}
                    tick={{ fontSize: 11.5 }}
                    tickLine={false}
                    axisLine={false}
                  />
                  <Tooltip content={<SHAPTooltip />} cursor={{ fill: 'rgba(79,70,229,0.05)' }} />
                  <Bar dataKey="shap" radius={[0, 6, 6, 0]}>
                    {SHAP_DATA.map((entry, i) => (
                      <Cell
                        key={i}
                        fill={entry.inForm ? '#4F46E5' : '#94A3B8'}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>

              <p className="mt-4 text-xs text-ink-900/50 leading-relaxed">
                * <strong>Skor Gaya Hidup</strong> adalah fitur engineered oleh tim DS Pulsevera.
                Masuk top-20 SHAP (0.011), membuktikan feature engineering menambah nilai prediktif.
                <br />
                SHAP (SHapley Additive exPlanations) mengukur kontribusi rata-rata setiap fitur
                terhadap output prediksi model, dihitung pada 200 sampel representatif.
              </p>
            </div>
          </motion.div>
        </section>

        {/* ── SECTION 3: Clinical Factors ── */}
        <section className="mb-16">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <div className="flex items-center gap-3 mb-3">
              <span className="grid h-10 w-10 place-items-center rounded-2xl bg-amber-100 text-amber-700">
                <BookOpen size={20} />
              </span>
              <div>
                <h2 className="font-display text-2xl font-bold">Faktor yang Tidak Kami Tanyakan</h2>
                <p className="text-sm text-ink-900/60">Ada di dataset, tapi membutuhkan diagnosis dokter, bukan pengetahuan awam</p>
              </div>
            </div>
            <p className="mb-6 text-sm text-ink-900/70 leading-relaxed ml-[52px]">
              Form Pulsevera sengaja hanya berisi 10 pertanyaan dari keseharian.
              Beberapa faktor klinis penting berikut tidak kami tanyakan karena
              pengguna awam sering tidak mengetahuinya tanpa diagnosis dokter.
              Jika Anda memiliki kondisi di bawah ini, informasikan ke dokter Anda.
            </p>

            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {CLINICAL_FACTORS.map((factor, i) => {
                const Icon = factor.icon
                return (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.35 + i * 0.07 }}
                    className="glass rounded-2xl p-5 hover:shadow-glow-blue transition-shadow"
                  >
                    <div className="flex items-start justify-between gap-2 mb-3">
                      <span className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-pulse-600 to-pulse-800 text-white shadow-soft shrink-0">
                        <Icon size={18} />
                      </span>
                      <span className="rounded-full bg-pulse-100 px-2 py-0.5 text-[10px] font-semibold text-pulse-700 shrink-0">
                        {factor.rank}
                      </span>
                    </div>
                    <h3 className="font-bold text-base mb-2">{factor.label}</h3>
                    <p className="text-xs text-ink-900/70 leading-relaxed mb-3">{factor.desc}</p>
                    <div className="rounded-xl bg-amber-50 px-3 py-2 ring-1 ring-amber-100">
                      <p className="text-xs text-amber-800 leading-snug">
                        <strong>Saran:</strong> {factor.action}
                      </p>
                    </div>
                  </motion.div>
                )
              })}
            </div>
          </motion.div>
        </section>

        {/* ── CTA ── */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="glass rounded-3xl p-8 sm:p-12 text-center mb-10"
        >
          <span className="badge mb-4">
            <Sparkles size={12} />
            Siap untuk cek risiko Anda?
          </span>
          <h2 className="font-display text-3xl sm:text-4xl font-bold mb-4">
            Kenali Risiko Jantung Anda
          </h2>
          <p className="mx-auto max-w-xl text-ink-900/70 mb-8 leading-relaxed">
            Isi 10 pertanyaan tentang gaya hidup sehari-hari dan dapatkan
            Skor Gaya Hidup + Estimasi Risiko berbasis AI dalam kurang dari 2 menit.
          </p>
          <button onClick={onCheckRisk} className="btn-primary text-base px-8 py-3">
            Mulai Screening Sekarang
            <ArrowRight size={18} />
          </button>
        </motion.div>

        {/* ── Disclaimer ── */}
        <div className="flex gap-3 rounded-2xl bg-amber-50 p-4 ring-1 ring-amber-100">
          <AlertTriangle size={18} className="text-amber-600 shrink-0 mt-0.5" />
          <p className="text-xs text-amber-900 leading-relaxed">
            <strong>Disclaimer:</strong> Seluruh data statistik bersumber dari lembaga resmi (WHO, AHA, BPJS, Riskesdas).
            Analisis SHAP dihitung pada dataset CDC BRFSS 2022 menggunakan model Random Forest Pulsevera.
            Konten ini bersifat edukatif dan tidak menggantikan konsultasi, diagnosis, atau
            perawatan medis profesional.
          </p>
        </div>
      </main>
    </div>
  )
}
