import React from 'react'
import { motion } from 'framer-motion'
import { FormInput, Cpu, FileBarChart2 } from 'lucide-react'

const STEPS = [
  {
    n: '01',
    icon: FormInput,
    title: 'Isi 10 pertanyaan',
    desc: 'Jenis kelamin, usia, BMI, jam tidur, status merokok, riwayat diabetes — kurang dari 1 menit.',
  },
  {
    n: '02',
    icon: Cpu,
    title: 'Model ML menganalisis',
    desc: 'Random Forest + Deep Learning memprediksi probabilitas serangan jantung berdasarkan 46 fitur lengkap.',
  },
  {
    n: '03',
    icon: FileBarChart2,
    title: 'Dapatkan hasil & saran',
    desc: 'Risk score (%), 3 faktor risiko utama (SHAP), dan rekomendasi gaya hidup personal yang actionable.',
  },
]

export default function HowItWorksSection() {
  return (
    <section id="how" className="py-16 sm:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <span className="badge mb-4">
            <span className="h-1.5 w-1.5 rounded-full bg-pulse-600" />
            Bagaimana cara kerjanya
          </span>
          <h2 className="h-section text-balance">
            Tiga langkah sederhana <span className="text-gradient">dari data ke insight</span>.
          </h2>
        </div>

        <div className="mt-12 grid md:grid-cols-3 gap-6 relative">
          {/* Connecting line */}
          <div
            aria-hidden
            className="hidden md:block absolute top-14 left-[16%] right-[16%] h-px bg-gradient-to-r from-transparent via-pulse-300 to-transparent"
          />
          {STEPS.map((s, i) => (
            <motion.div
              key={s.n}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.15 }}
              className="relative"
            >
              <div className="card hover:shadow-glow-blue">
                <div className="flex items-start justify-between mb-6">
                  <span className="grid h-14 w-14 place-items-center rounded-2xl bg-gradient-to-br from-pulse-600 to-pulse-800 text-white shadow-glow-blue">
                    <s.icon size={22} />
                  </span>
                  <span className="font-display text-3xl font-bold text-pulse-100">{s.n}</span>
                </div>
                <h3 className="font-display text-xl font-bold mb-2">{s.title}</h3>
                <p className="text-sm text-ink-900/70">{s.desc}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
