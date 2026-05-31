import React from 'react'
import { motion } from 'framer-motion'

const STATS = [
  { value: '245K', suffix: '+', label: 'Kematian/tahun akibat penyakit jantung di Indonesia' },
  { value: '20', suffix: 'JT', label: 'Kasus jantung tercatat (2023)' },
  { value: '85', suffix: '%+', label: 'Akurasi prediksi model Pulsevera' },
  { value: '15', suffix: 's', label: 'Waktu yang dibutuhkan untuk cek risiko' },
]

export default function StatsSection() {
  return (
    <section className="py-12 sm:py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="glass rounded-3xl p-6 sm:p-10">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
            {STATS.map((s, i) => (
              <motion.div
                key={s.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                className="text-center"
              >
                <p className="font-display text-4xl sm:text-5xl font-bold text-gradient">
                  {s.value}
                  <span className="text-2xl sm:text-3xl">{s.suffix}</span>
                </p>
                <p className="mt-2 text-xs sm:text-sm text-ink-900/70 max-w-[240px] mx-auto text-balance">
                  {s.label}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
