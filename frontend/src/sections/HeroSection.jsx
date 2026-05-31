import React from 'react'
import { motion } from 'framer-motion'
import { ArrowUpRight, Sparkles, ShieldCheck, Activity } from 'lucide-react'
import HeartScene from '../components/three/HeartScene'

export default function HeroSection({ onCheckRisk }) {
  return (
    <section
      id="home"
      className="relative pt-28 pb-12 sm:pt-32 sm:pb-16 overflow-hidden"
    >
      {/* Watermark background text */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-x-0 -top-4 select-none text-center"
      >
        <h1 className="font-display font-extrabold text-[18vw] sm:text-[16vw] leading-none text-white/40 tracking-tighter">
          PULSEVERA
        </h1>
      </div>

      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="glass rounded-[2.5rem] p-6 sm:p-10 lg:p-14 overflow-hidden">
          <div className="grid lg:grid-cols-2 gap-10 items-center">
            {/* Left — copy */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7 }}
              className="relative z-10"
            >
              <span className="badge mb-6">
                <Sparkles size={12} className="text-mint-500" />
                Powered by AI · 445K+ data point CDC BRFSS
              </span>

              <h2 className="font-display text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight leading-[0.95] text-balance">
                Predict.{' '}
                <span className="text-gradient">Prevent.</span>
                <br />
                Prevail.
              </h2>

              <p className="mt-6 max-w-xl text-base sm:text-lg text-ink-900/70 text-balance">
                Pulsevera memprediksi risiko penyakit jantung Anda dalam{' '}
                <strong>15 detik</strong> berdasarkan 10 pertanyaan gaya hidup
                — didukung machine learning dengan akurasi tinggi dan
                penjelasan SHAP yang transparan.
              </p>

              <div className="mt-8 flex flex-wrap items-center gap-3">
                <button onClick={onCheckRisk} className="btn-primary">
                  Mulai Cek Risiko
                  <ArrowUpRight size={16} />
                </button>
                <a href="#how" className="btn-secondary">Cara kerjanya</a>
              </div>

              {/* Floating mini-stats */}
              <div className="mt-10 grid grid-cols-3 gap-3 max-w-md">
                <Stat icon={Activity} value="85%+" label="Akurasi model" />
                <Stat icon={ShieldCheck} value="100%" label="Privasi data" />
                <Stat icon={Sparkles} value="3" label="Algoritma ML" />
              </div>
            </motion.div>

            {/* Right — 3D Heart */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.9, delay: 0.2 }}
              className="relative h-[440px] sm:h-[520px] lg:h-[600px]"
            >
              {/* Glow background behind heart */}
              <div
                aria-hidden
                className="absolute inset-8 rounded-full bg-gradient-to-br from-pulse-200/50 via-pulse-100/30 to-mint-400/20 blur-3xl"
              />

              <div className="relative h-full w-full">
                <HeartScene />
              </div>

              {/* Floating UI badges */}
              <FloatBadge
                position="top-8 right-2 sm:right-6"
                title="BPM Avg"
                value="72"
                accent="bg-coral-500"
                delay={0.4}
              />
              <FloatBadge
                position="bottom-20 left-0 sm:left-2"
                title="Risk Predicted"
                value="Low"
                accent="bg-mint-500"
                delay={0.6}
              />
              <FloatBadge
                position="top-1/2 left-4 sm:left-10"
                title="ML Confidence"
                value="93%"
                accent="bg-pulse-600"
                delay={0.8}
              />
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  )
}

function Stat({ icon: Icon, value, label }) {
  return (
    <div className="rounded-2xl bg-white/80 p-3 shadow-soft ring-1 ring-pulse-100/60 backdrop-blur">
      <Icon size={16} className="text-pulse-600 mb-1" />
      <p className="font-display text-lg font-bold leading-none">{value}</p>
      <p className="text-[10px] text-ink-900/60 uppercase tracking-wider mt-1">{label}</p>
    </div>
  )
}

function FloatBadge({ position, title, value, accent, delay }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5 }}
      className={`absolute ${position} glass rounded-2xl px-3 py-2 flex items-center gap-2 animate-float`}
      style={{ animationDelay: `${delay}s` }}
    >
      <span className={`grid h-7 w-7 place-items-center rounded-full ${accent} text-white text-xs font-bold`}>
        ❤
      </span>
      <div>
        <p className="text-[10px] uppercase tracking-wider text-ink-900/60">{title}</p>
        <p className="text-sm font-semibold leading-none">{value}</p>
      </div>
    </motion.div>
  )
}
