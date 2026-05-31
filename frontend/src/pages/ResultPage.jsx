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

const LABEL_DESCRIPTION = {
  Rendah: {
    title: 'Pertahankan gaya hidup sehat Anda.',
    desc: 'Berdasarkan profil Anda, risiko penyakit jantung tergolong rendah. Tetap konsisten dengan kebiasaan sehat dan check-up rutin tahunan.',
  },
  Sedang: {
    title: 'Ada beberapa faktor risiko yang perlu diperhatikan.',
    desc: 'Profil Anda menunjukkan beberapa faktor yang bisa meningkatkan risiko. Lakukan perubahan gaya hidup yang disarankan dan pertimbangkan konsultasi dokter.',
  },
  Tinggi: {
    title: 'Sebaiknya konsultasi dengan dokter sesegera mungkin.',
    desc: 'Beberapa faktor risiko jantung Anda berada pada level yang perlu perhatian medis. Hasil ini bukan diagnosis — segera lakukan pemeriksaan klinis.',
  },
}

export default function ResultPage({ result, formData, onBack, onRetake }) {
  if (!result) return null

  const { risk_score, risk_percent, risk_label, top_risk_factors, recommendations, model_used, inference_ms } = result
  const labelMeta = LABEL_DESCRIPTION[risk_label] || LABEL_DESCRIPTION.Sedang

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

        {/* Hero result */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-3xl p-6 sm:p-12"
        >
          <div className="grid lg:grid-cols-2 gap-10 items-center">
            <div>
              <span className="badge mb-4">
                <span className="h-1.5 w-1.5 rounded-full bg-mint-500" />
                Hasil Analisis Anda
              </span>
              <h1 className="font-display text-3xl sm:text-5xl font-bold tracking-tight leading-tight text-balance">
                {labelMeta.title}
              </h1>
              <p className="mt-4 text-ink-900/70 leading-relaxed text-balance">
                {labelMeta.desc}
              </p>

              <div className="mt-6 flex flex-wrap gap-2 text-xs text-ink-900/60">
                <span className="badge">Model: {model_used}</span>
                <span className="badge">Inference: {inference_ms?.toFixed?.(0) ?? '~'} ms</span>
              </div>
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
          transition={{ delay: 0.2 }}
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
                  transition={{ delay: 0.3 + i * 0.1 }}
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
          transition={{ delay: 0.5 }}
          className="mt-8 glass rounded-3xl p-6 sm:p-10"
        >
          <div className="flex items-center gap-3 mb-6">
            <span className="grid h-12 w-12 place-items-center rounded-2xl bg-mint-500 text-white shadow-soft">
              <Lightbulb size={20} />
            </span>
            <div>
              <h2 className="font-display text-2xl font-bold">Rekomendasi untuk Anda</h2>
              <p className="text-sm text-ink-900/60">Dipersonalisasi berdasarkan profil Anda</p>
            </div>
          </div>

          <ol className="space-y-3">
            {recommendations?.map((rec, i) => (
              <motion.li
                key={i}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.6 + i * 0.08 }}
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

        {/* Disclaimer */}
        <div className="mt-6 flex gap-3 rounded-2xl bg-amber-50 p-4 ring-1 ring-amber-100">
          <AlertTriangle size={18} className="text-amber-600 shrink-0 mt-0.5" />
          <p className="text-xs text-amber-900 leading-relaxed">
            <strong>Disclaimer medis:</strong> Hasil prediksi ini bersifat indikatif berdasarkan
            data populasi dan model machine learning. Tidak dimaksudkan untuk menggantikan
            diagnosis, konsultasi, atau perawatan medis profesional. Selalu konsultasikan
            kondisi kesehatan Anda dengan dokter atau tenaga medis berkualifikasi.
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
