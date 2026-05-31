import React from 'react'
import { Heart, Github, Mail, Globe } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="relative mt-20 overflow-hidden">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="glass rounded-3xl p-8 sm:p-12">
          <div className="grid gap-10 lg:grid-cols-4">
            {/* Brand */}
            <div className="lg:col-span-2">
              <div className="flex items-center gap-2 mb-4">
                <span className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-pulse-600 to-pulse-800 text-white shadow-glow-blue">
                  <Heart size={20} fill="white" strokeWidth={0} />
                </span>
                <span className="font-display text-xl font-bold">Pulsevera</span>
              </div>
              <p className="max-w-md text-sm text-ink-900/70">
                Sistem prediksi risiko penyakit jantung berbasis machine learning,
                dirancang untuk meningkatkan kesadaran kesehatan masyarakat Indonesia.
              </p>
              <p className="mt-4 text-xs text-ink-900/50">
                CC26-PRU439 · Coding Camp 2026 powered by DBS Foundation
              </p>
            </div>

            {/* Links */}
            <div>
              <h4 className="text-sm font-semibold mb-3">Produk</h4>
              <ul className="space-y-2 text-sm text-ink-900/70">
                <li><a href="#features" className="hover:text-pulse-700">Fitur</a></li>
                <li><a href="#how" className="hover:text-pulse-700">Cara Kerja</a></li>
                <li><a href="#about" className="hover:text-pulse-700">Tentang Model</a></li>
                <li><a href="#faq" className="hover:text-pulse-700">FAQ</a></li>
              </ul>
            </div>

            <div>
              <h4 className="text-sm font-semibold mb-3">Tim</h4>
              <ul className="space-y-2 text-sm text-ink-900/70">
                <li>Data Science</li>
                <li>AI Engineer</li>
                <li>Full-Stack</li>
                <li className="pt-2 flex gap-2">
                  <a className="grid h-9 w-9 place-items-center rounded-full bg-white shadow-soft hover:shadow-glow-blue transition" href="#" aria-label="GitHub">
                    <Github size={16} />
                  </a>
                  <a className="grid h-9 w-9 place-items-center rounded-full bg-white shadow-soft hover:shadow-glow-blue transition" href="#" aria-label="Email">
                    <Mail size={16} />
                  </a>
                  <a className="grid h-9 w-9 place-items-center rounded-full bg-white shadow-soft hover:shadow-glow-blue transition" href="#" aria-label="Website">
                    <Globe size={16} />
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <div className="mt-8 border-t border-pulse-100 pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-ink-900/60">
            <p>© {new Date().getFullYear()} Pulsevera. Predict, Prevent, Prevail.</p>
            <p className="italic">
              Disclaimer: prediksi bersifat indikatif dan tidak menggantikan diagnosis medis.
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}
