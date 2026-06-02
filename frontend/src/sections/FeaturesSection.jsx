import React from 'react'
import { motion } from 'framer-motion'
import { ArrowUpRight, Heart, Brain, Activity } from 'lucide-react'
import MiniBlobScene from '../components/three/MiniBlobScene'

const FEATURES = [
  {
    icon: Heart,
    title: 'Heart Risk Score',
    desc: 'Prediksi probabilitas serangan jantung dengan model machine learning yang dilatih di 445K data CDC BRFSS.',
    accent: '#EF4444',
    badge: 'AI',
  },
  {
    icon: Brain,
    title: 'Explainable AI',
    desc: 'Setiap prediksi disertai 3 faktor risiko teratas berdasarkan SHAP, sehingga Anda tahu kenapa, bukan hanya hasil.',
    accent: '#3B82F6',
    badge: 'SHAP',
  },
  {
    icon: Activity,
    title: 'Smart Recommendation',
    desc: 'Rekomendasi gaya hidup personal: pola tidur, olahraga, dan diet, disesuaikan dengan profil Anda.',
    accent: '#10B981',
    badge: 'Personal',
  },
]

export default function FeaturesSection({ onCheckRisk }) {
  return (
    <section id="features" className="py-16 sm:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-10">
          <div className="max-w-xl">
            <span className="badge mb-4">
              <span className="h-1.5 w-1.5 rounded-full bg-mint-500" />
              Apa yang Anda dapat
            </span>
            <h2 className="h-section text-balance">
              Bukan sekadar prediksi, melainkan <span className="text-gradient">deteksi dini</span> yang bisa Anda pahami.
            </h2>
          </div>
          <button onClick={onCheckRisk} className="btn-secondary self-start sm:self-end">
            Coba sekarang
            <ArrowUpRight size={16} />
          </button>
        </div>

        <div className="grid md:grid-cols-3 gap-5">
          {FEATURES.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className="card group relative overflow-hidden hover:-translate-y-1 hover:shadow-glow-blue"
            >
              {/* 3D blob accent */}
              <div className="absolute -top-12 -right-12 h-44 w-44 opacity-40 group-hover:opacity-70 transition">
                <MiniBlobScene color={f.accent} />
              </div>

              <div className="relative">
                <div className="flex items-center justify-between mb-6">
                  <span
                    className="grid h-12 w-12 place-items-center rounded-2xl text-white shadow-soft"
                    style={{ backgroundColor: f.accent }}
                  >
                    <f.icon size={22} />
                  </span>
                  <span className="badge">{f.badge}</span>
                </div>

                <h3 className="font-display text-xl font-bold mb-2">{f.title}</h3>
                <p className="text-sm text-ink-900/70 leading-relaxed">{f.desc}</p>

              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
