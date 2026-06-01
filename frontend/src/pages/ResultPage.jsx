import React from 'react'
import { motion } from 'framer-motion'
import {
  ArrowLeft,
  RefreshCw,
  Lightbulb,
  AlertTriangle,
  TrendingUp,
  Activity,
  Cigarette,
  Wine,
  Moon,
  Scale,
  Heart,
  HeartPulse,
  Calendar,
  Stethoscope,
  CheckCircle2,
  XCircle,
  Sparkles,
} from 'lucide-react'
import RiskGauge from '../components/RiskGauge'

const FACTOR_ICON = {
  AgeCategory: Calendar,
  BMI: Scale,
  IsObese: Scale,
  WeightInKilograms: Scale,
  SmokerStatus: Cigarette,
  IsActiveSmoker: Cigarette,
  AlcoholDrinkers: Wine,
  SleepHours: Moon,
  IsSleepDeprived: Moon,
  PhysicalActivities: Activity,
  GeneralHealth: Stethoscope,
  HadDiabetes: HeartPulse,
  LifestyleRiskScore: TrendingUp,
  HasChronicCondition: AlertTriangle,
}

const HABIT_ICON = {
  not_smoking: Cigarette,
  active: Activity,
  enough_sleep: Moon,
  healthy_weight: Scale,
  not_drinking: Wine,
}

const LIFESTYLE_GRADE_META = {
  'Sangat Sehat': {
    color: 'mint',
    title: 'Gaya hidup Anda luar biasa! Pertahankan ini.',
    desc: 'Semua kebiasaan harian Anda mendukung kesehatan jantung jangka panjang. Lanjutkan rutinitas ini dan tetap konsisten dengan check-up rutin tahunan.',
  },
  Sehat: {
    color: 'mint',
    title: 'Gaya hidup Anda sudah baik.',
    desc: 'Sebagian besar kebiasaan Anda mendukung kesehatan jantung. Ada satu hal kecil yang bisa diperbaiki untuk hasil lebih optimal.',
  },
  Cukup: {
    color: 'amber',
    title: 'Ada beberapa kebiasaan yang perlu ditingkatkan.',
    desc: 'Gaya hidup Anda di tengah-tengah. Beberapa kebiasaan kecil yang diperbaiki bisa memberi dampak besar untuk kesehatan jantung Anda di masa depan.',
  },
  'Perlu Perhatian': {
    color: 'coral',
    title: 'Saatnya perbaiki kebiasaan harian.',
    desc: 'Beberapa kebiasaan Anda dapat meningkatkan risiko penyakit jantung di masa depan. Mulai dengan satu perubahan kecil hari ini — efeknya kumulatif untuk jangka panjang.',
  },
  Berisiko: {
    color: 'coral',
    title: 'Banyak kebiasaan yang perlu diubah.',
    desc: 'Pola hidup Anda saat ini meningkatkan risiko jangka panjang. Walaupun risiko jangka pendek mungkin rendah, kebiasaan ini berakumulasi seiring waktu. Pertimbangkan konsultasi dengan dokter.',
  },
  'Berisiko Tinggi': {
    color: 'coral',
    title: 'Perlu perubahan gaya hidup segera.',
    desc: 'Hampir semua kebiasaan harian Anda berisiko tinggi terhadap kesehatan jantung. Konsultasikan dengan dokter dan mulai perubahan satu per satu.',
  },
}

const RISK_LABEL_META = {
  Rendah: {
    icon: '🟢',
    desc: 'Risiko serangan jantung dalam waktu dekat tergolong rendah.',
  },
  Sedang: {
    icon: '🟡',
    desc: 'Ada beberapa faktor yang dapat meningkatkan risiko.',
  },
  Tinggi: {
    icon: '🔴',
    desc: 'Sebaiknya konsultasi dengan dokter untuk evaluasi menyeluruh.',
  },
}

function LifestyleGauge({ score, max = 5, color = 'mint' }) {
  const percent = (score / max) * 100
  const colorClasses = {
    mint: 'from-mint-400 to-mint-600',
    amber: 'from-amber-400 to-amber-600',
    coral: 'from-coral-400 to-coral-600',
  }

  return (
    <div className="flex flex-col items-center">
      <div className="relative">
        <svg width="220" height="220" viewBox="0 0 220 220">
          <circle
            cx="110"
            cy="110"
            r="90"
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="18"
          />
          <motion.circle
            cx="110"
            cy="110"
            r="90"
            fill="none"
            stroke={`url(#grad-${color})`}
            strokeWidth="18"
            strokeLinecap="round"
            strokeDasharray={`${2 * Math.PI * 90}`}
            initial={{ strokeDashoffset: 2 * Math.PI * 90 }}
            animate={{ strokeDashoffset: 2 * Math.PI * 90 * (1 - percent / 100) }}
            transition={{ duration: 1.2, ease: 'easeOut' }}
            transform="rotate(-90 110 110)"
          />
          <defs>
            <linearGradient id="grad-mint" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#34d399" />
              <stop offset="100%" stopColor="#059669" />
            </linearGradient>
            <linearGradient id="grad-amber" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#fbbf24" />
              <stop offset="100%" stopColor="#d97706" />
            </linearGradient>
            <linearGradient id="grad-coral" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#fb7185" />
              <stop offset="100%" stopColor="#e11d48" />
            </linearGradient>
          </defs>
        </svg>
        <div className="absolute inset-0 grid place-items-center text-center">
          <div>
            <div className="font-display text-6xl font-bold text-ink-900">
              {score}
              <span className="text-2xl text-ink-900/40">/{max}</span>
            </div>
            <div className="text-xs text-ink-900/60 mt-1 uppercase tracking-wider">
              Skor Gaya Hidup
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default function ResultPage({ result, formData, onBack, onRetake }) {
  if (!result) return null

  const {
    risk_score,
    risk_percent,
    risk_label,
    lifestyle,
    top_risk_factors,
    recommendations,
    recommendation_source,
    model_used,
    inference_ms,
  } = result

  const lifestyleMeta = LIFESTYLE_GRADE_META[lifestyle?.grade] || LIFESTYLE_GRADE_META.Cukup
  const riskMeta = RISK_LABEL_META[risk_label] || RISK_LABEL_META.Sedang

  return (
    <div className="min-h-screen bg-gradient-pulse py-10 px-4 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-5xl">
        {/* Top bar */}
        <div className="flex items-center justify-between mb-8">
          <button onClick={onBack} className="btn-secondary">
            <ArrowLeft size={16} />
            Beranda
          </button>
          <button onClick={onRetake} className="btn-secondary">
            <RefreshCw size={16} />
            Cek Ulang
          </button>
        </div>

        {/* Hero: Lifestyle Score */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-3xl p-6 sm:p-12"
        >
          <div className="grid lg:grid-cols-2 gap-10 items-center">
            <div>
              <span className="badge mb-4">
                <Sparkles size={12} />
                Hasil Analisis Gaya Hidup
              </span>
              <h1 className="font-display text-3xl sm:text-5xl font-bold tracking-tight leading-tight text-balance">
                {lifestyleMeta.title}
              </h1>
              <p className="mt-4 text-ink-900/70 leading-relaxed text-balance">
                {lifestyleMeta.desc}
              </p>
              <div className="mt-6 inline-flex items-center gap-2 rounded-full bg-white/80 px-4 py-2 ring-1 ring-pulse-100">
                <span className="text-sm font-semibold">{lifestyle?.grade}</span>
              </div>
            </div>

            <div className="flex justify-center">
              <LifestyleGauge
                score={lifestyle?.score ?? 0}
                max={lifestyle?.max_score ?? 5}
                color={lifestyleMeta.color}
              />
            </div>
          </div>
        </motion.div>

        {/* 5 Habits Checklist */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          className="mt-8 glass rounded-3xl p-6 sm:p-10"
        >
          <div className="flex items-center gap-3 mb-6">
            <span className="grid h-12 w-12 place-items-center rounded-2xl bg-gradient-to-br from-pulse-600 to-pulse-800 text-white shadow-soft">
              <Heart size={20} fill="white" strokeWidth={0} />
            </span>
            <div>
              <h2 className="font-display text-2xl font-bold">5 Kebiasaan Anda</h2>
              <p className="text-sm text-ink-900/60">
                Indikator gaya hidup yang berdampak ke kesehatan jantung
              </p>
            </div>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {lifestyle?.habits?.map((habit, i) => {
              const Icon = HABIT_ICON[habit.key] || Heart
              return (
                <motion.div
                  key={habit.key}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 + i * 0.05 }}
                  className={`flex items-center gap-3 rounded-2xl p-4 ring-1 ${
                    habit.good
                      ? 'bg-mint-500/10 ring-mint-500/30'
                      : 'bg-coral-500/10 ring-coral-500/30'
                  }`}
                >
                  <span
                    className={`grid h-10 w-10 place-items-center rounded-xl shadow-soft shrink-0 ${
                      habit.good ? 'bg-mint-500 text-white' : 'bg-coral-500 text-white'
                    }`}
                  >
                    <Icon size={18} />
                  </span>
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium text-ink-900 truncate">{habit.label}</p>
                  </div>
                  {habit.good ? (
                    <CheckCircle2 size={20} className="text-mint-600 shrink-0" />
                  ) : (
                    <XCircle size={20} className="text-coral-600 shrink-0" />
                  )}
                </motion.div>
              )
            })}
          </div>
        </motion.div>

        {/* Heart Attack Risk (SECONDARY) */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-8 glass rounded-3xl p-6 sm:p-10"
        >
          <div className="grid md:grid-cols-2 gap-6 items-center">
            <div>
              <span className="badge mb-3">Estimasi tambahan</span>
              <h2 className="font-display text-2xl font-bold mb-2">
                Estimasi Risiko Serangan Jantung
              </h2>
              <p className="text-ink-900/70 text-sm leading-relaxed">
                {riskMeta.icon} <strong>{risk_label}</strong> — {riskMeta.desc}
              </p>
              <p className="text-xs text-ink-900/50 mt-3 italic">
                Catatan: estimasi ini berdasarkan pola statistik populasi CDC BRFSS 2022.
                Risiko bisa tampak rendah untuk usia muda meski gaya hidup kurang sehat —
                karena itu fokus utama analisis ini adalah <strong>Skor Gaya Hidup</strong> di atas.
              </p>
            </div>
            <div className="flex justify-center">
              <RiskGauge score={risk_score} percent={risk_percent} label={risk_label} />
            </div>
          </div>
        </motion.div>

        {/* Top Risk Factors */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mt-8"
        >
          <div className="flex items-center justify-between mb-5">
            <h2 className="font-display text-2xl font-bold">3 Faktor Risiko Utama</h2>
            <span className="badge">Powered by SHAP</span>
          </div>
          <div className="grid md:grid-cols-3 gap-4">
            {top_risk_factors?.map((factor, i) => {
              const Icon = FACTOR_ICON[factor.feature] || Heart
              return (
                <motion.div
                  key={factor.feature}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 + i * 0.1 }}
                  className="card relative overflow-hidden hover:shadow-glow-blue"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <span className="grid h-12 w-12 place-items-center rounded-2xl bg-gradient-to-br from-pulse-600 to-pulse-800 text-white shadow-soft">
                      <Icon size={20} />
                    </span>
                    <span className="font-display text-3xl font-bold text-pulse-100">
                      0{i + 1}
                    </span>
                  </div>
                  <h3 className="font-bold text-lg mb-1">{factor.label}</h3>
                  <p className="text-xs text-ink-900/50 font-mono">{factor.feature}</p>
                  <p className="text-xs text-ink-900/60 mt-3">
                    Faktor ini memberi kontribusi signifikan terhadap skor risiko Anda.
                  </p>
                </motion.div>
              )
            })}
          </div>
        </motion.div>

        {/* Recommendations */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mt-8 glass rounded-3xl p-6 sm:p-10"
        >
          <div className="flex items-center gap-3 mb-6">
            <span className="grid h-12 w-12 place-items-center rounded-2xl bg-mint-500 text-white shadow-soft">
              <Lightbulb size={20} />
            </span>
            <div>
              <h2 className="font-display text-2xl font-bold">Rekomendasi untuk Anda</h2>
              <p className="text-sm text-ink-900/60">
                {recommendation_source === 'gemini'
                  ? 'Dipersonalisasi oleh AI berdasarkan profil Anda'
                  : 'Dipersonalisasi berdasarkan profil Anda'}
              </p>
            </div>
          </div>

          <ol className="space-y-3">
            {recommendations?.map((rec, i) => (
              <motion.li
                key={i}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.7 + i * 0.08 }}
                className="flex gap-4 rounded-2xl bg-white/80 p-4 ring-1 ring-pulse-100/60"
              >
                <span className="grid h-8 w-8 place-items-center rounded-full bg-pulse-700 text-white text-xs font-bold shrink-0">
                  {i + 1}
                </span>
                <p className="text-sm leading-relaxed text-ink-900/85">{rec}</p>
              </motion.li>
            ))}
          </ol>
        </motion.div>

        {/* Model info */}
        <div className="mt-6 flex flex-wrap gap-2 justify-center text-xs text-ink-900/60">
          <span className="badge">Model: {model_used}</span>
          <span className="badge">Inference: {inference_ms?.toFixed?.(0) ?? '~'} ms</span>
        </div>

        {/* Disclaimer */}
        <div className="mt-6 flex gap-3 rounded-2xl bg-amber-50 p-4 ring-1 ring-amber-100">
          <AlertTriangle size={18} className="text-amber-600 shrink-0 mt-0.5" />
          <p className="text-xs text-amber-900 leading-relaxed">
            <strong>Disclaimer medis:</strong> Pulsevera adalah alat <strong>edukasi kesadaran kesehatan</strong>,
            bukan alat diagnosis. Hasil analisis bersifat indikatif berdasarkan data populasi
            CDC BRFSS 2022 dan model machine learning. Tidak menggantikan konsultasi, diagnosis,
            atau perawatan medis profesional. Selalu konsultasikan kondisi kesehatan Anda
            dengan dokter atau tenaga medis berkualifikasi.
          </p>
        </div>

        <div className="mt-8 text-center">
          <button onClick={onRetake} className="btn-primary">
            Cek Ulang dengan Data Lain
            <RefreshCw size={16} />
          </button>
        </div>
      </div>
    </div>
  )
}
