import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Plus, Minus } from 'lucide-react'

const FAQS = [
  {
    q: 'Apakah hasil prediksi ini bisa menggantikan diagnosis dokter?',
    a: 'Tidak. Pulsevera adalah alat skrining indikatif berbasis data populasi. Hasil prediksi tinggi sebaiknya ditindaklanjuti dengan konsultasi medis profesional dan pemeriksaan klinis.',
  },
  {
    q: 'Seberapa akurat model Pulsevera?',
    a: 'Model kami mencapai akurasi >85% dengan recall kelas positif >70% pada data uji 89.000+ sampel. Detail metrik tersedia di /api/v1/metadata.',
  },
  {
    q: 'Bagaimana model menangani data yang tidak seimbang?',
    a: 'Kami menggunakan SMOTE (Synthetic Minority Over-sampling) ditambah class weighting untuk machine learning, dan custom Focal Loss untuk deep learning.',
  },
  {
    q: 'Apakah data saya disimpan?',
    a: 'Tidak. Pulsevera berjalan stateless: input Anda diproses real-time dan tidak disimpan di database mana pun.',
  },
  {
    q: 'Apa itu SHAP dan kenapa penting?',
    a: 'SHAP (SHapley Additive exPlanations) menjelaskan kontribusi setiap fitur pada prediksi individual. Anda jadi tahu kenapa risiko Anda dinilai tinggi/rendah, bukan hanya angka saja.',
  },
]

export default function FAQSection() {
  const [open, setOpen] = useState(0)

  return (
    <section id="faq" className="py-16 sm:py-24">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-10">
          <span className="badge mb-4">
            <span className="h-1.5 w-1.5 rounded-full bg-pulse-600" />
            Frequently Asked
          </span>
          <h2 className="h-section text-balance">
            Pertanyaan yang sering <span className="text-gradient">ditanyakan</span>
          </h2>
        </div>

        <div className="space-y-3">
          {FAQS.map((item, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
              className="card overflow-hidden"
            >
              <button
                onClick={() => setOpen(open === i ? -1 : i)}
                className="w-full flex items-center justify-between gap-4 text-left"
              >
                <span className="font-semibold text-base">{item.q}</span>
                <span className="grid h-9 w-9 place-items-center rounded-full bg-pulse-50 text-pulse-700 shrink-0">
                  {open === i ? <Minus size={16} /> : <Plus size={16} />}
                </span>
              </button>

              <AnimatePresence>
                {open === i && (
                  <motion.p
                    initial={{ opacity: 0, height: 0, marginTop: 0 }}
                    animate={{ opacity: 1, height: 'auto', marginTop: 12 }}
                    exit={{ opacity: 0, height: 0, marginTop: 0 }}
                    transition={{ duration: 0.25 }}
                    className="text-sm text-ink-900/70 leading-relaxed overflow-hidden"
                  >
                    {item.a}
                  </motion.p>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
