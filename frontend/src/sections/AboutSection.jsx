import React from 'react'
import { motion } from 'framer-motion'
import { Database, Cpu, BarChart2, Shield } from 'lucide-react'

const TECH = [
  { icon: Database, label: 'Dataset', value: 'CDC BRFSS 2022', desc: '445.132 responden' },
  { icon: Cpu, label: 'Model', value: 'Deep Learning', desc: 'TensorFlow Functional API + SMOTE' },
  { icon: BarChart2, label: 'Performa', value: '85.76%', desc: 'Accuracy + Recall 71.15%' },
  { icon: Shield, label: 'Interpretability', value: 'SHAP', desc: 'Per-prediction explanation' },
]

export default function AboutSection() {
  return (
    <section id="about" className="py-16 sm:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="glass rounded-3xl p-8 sm:p-12 overflow-hidden relative">
          {/* Decorative grid */}
          <div aria-hidden className="absolute inset-0 bg-grid opacity-40 pointer-events-none" />

          <div className="relative grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <span className="badge mb-4">
                <span className="h-1.5 w-1.5 rounded-full bg-mint-500" />
                Tentang Model
              </span>
              <h2 className="h-section mb-4 text-balance">
                Dibangun di atas <span className="text-gradient">data nyata, ilmu terbuka</span>.
              </h2>
              <p className="text-ink-900/70 leading-relaxed">
                Pulsevera menggunakan dataset publik <strong>CDC BRFSS 2022</strong> dengan
                <strong> 445.132 responden</strong> nyata. Model dilatih dengan kombinasi
                klasik (Logistic Regression, Random Forest, Decision Tree) dan{' '}
                <strong>Deep Learning (TensorFlow)</strong> menggunakan custom focal loss
                untuk mengatasi imbalance kelas (~5.6% kasus positif).
              </p>
              <p className="text-ink-900/70 leading-relaxed mt-4">
                Setiap prediksi disertai penjelasan <strong>SHAP</strong>, sehingga Anda tahu fitur mana
                yang paling berkontribusi terhadap risiko Anda secara spesifik, bukan
                generalisasi populasi.
              </p>

              <div className="mt-6 flex flex-wrap gap-2">
                {['Python', 'TensorFlow', 'Scikit-learn', 'SHAP', 'FastAPI', 'React', 'Three.js'].map((t) => (
                  <span key={t} className="badge text-xs">{t}</span>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              {TECH.map((t, i) => (
                <motion.div
                  key={t.label}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.08, duration: 0.4 }}
                  className="card hover:shadow-glow-blue"
                >
                  <span className="grid h-11 w-11 place-items-center rounded-xl bg-pulse-50 text-pulse-700 mb-3">
                    <t.icon size={20} />
                  </span>
                  <p className="text-xs uppercase tracking-wider text-ink-900/50 mb-1">{t.label}</p>
                  <p className="font-display text-lg font-bold leading-tight">{t.value}</p>
                  <p className="text-xs text-ink-900/60 mt-1">{t.desc}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
