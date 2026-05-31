import React from 'react'
import { motion } from 'framer-motion'
import { ArrowUpRight, Heart } from 'lucide-react'

export default function CTASection({ onCheckRisk }) {
  return (
    <section className="py-12">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="relative overflow-hidden rounded-[2rem] bg-gradient-to-br from-pulse-700 via-pulse-800 to-pulse-900 p-10 sm:p-16 text-white shadow-glow-blue"
        >
          {/* Decorative hearts */}
          <Heart
            size={200}
            className="absolute -top-10 -right-10 text-white/5"
            strokeWidth={1}
          />
          <Heart
            size={140}
            className="absolute -bottom-10 -left-10 text-white/5"
            strokeWidth={1}
          />

          <div className="relative max-w-2xl">
            <h2 className="font-display text-3xl sm:text-5xl font-bold leading-tight mb-4 text-balance">
              Mulai jaga jantung Anda hari ini, <br className="hidden sm:block" />
              <span className="text-mint-400">gratis & instan.</span>
            </h2>
            <p className="text-white/80 mb-8 max-w-lg">
              Tidak perlu sign-up. Tidak perlu kartu kredit. Cukup 10 pertanyaan
              dan dapatkan insight kesehatan jantung Anda dalam hitungan detik.
            </p>
            <button
              onClick={onCheckRisk}
              className="inline-flex items-center gap-2 rounded-full bg-white px-7 py-3.5 text-sm font-bold text-pulse-800 shadow-lg hover:bg-mint-400 hover:text-white transition-all active:scale-95"
            >
              Cek Risiko Saya Sekarang
              <ArrowUpRight size={18} />
            </button>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
