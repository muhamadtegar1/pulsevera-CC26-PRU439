import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { Heart, Menu, X, ArrowUpRight, BarChart2 } from 'lucide-react'

const NAV_ITEMS = [
  { label: 'Beranda', href: '#home' },
  { label: 'Fitur', href: '#features' },
  { label: 'Cara Kerja', href: '#how' },
  { label: 'Tentang', href: '#about' },
  { label: 'FAQ', href: '#faq' },
  { label: 'Wawasan Data', to: '/insights' },
]

export default function Navbar({ onCheckRisk }) {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 16)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className={`fixed inset-x-0 top-0 z-50 transition-all ${
        scrolled ? 'py-2' : 'py-4'
      }`}
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <nav
          className={`flex items-center justify-between rounded-full px-4 py-2.5 sm:px-6 transition-all ${
            scrolled ? 'glass' : 'bg-white/40 backdrop-blur ring-1 ring-white/30'
          }`}
        >
          {/* Logo */}
          <a href="#home" className="flex items-center gap-2 font-display text-lg font-bold">
            <span className="grid h-9 w-9 place-items-center rounded-xl bg-gradient-to-br from-pulse-600 to-pulse-800 text-white shadow-glow-blue">
              <Heart size={18} fill="white" strokeWidth={0} />
            </span>
            <span className="hidden sm:block">Pulsevera</span>
          </a>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-1">
            {NAV_ITEMS.map((item) =>
              item.to ? (
                <Link key={item.to} to={item.to} className="btn-ghost flex items-center gap-1">
                  <BarChart2 size={14} />
                  {item.label}
                </Link>
              ) : (
                <a key={item.href} href={item.href} className="btn-ghost">
                  {item.label}
                </a>
              )
            )}
          </div>

          {/* CTA */}
          <div className="flex items-center gap-2">
            <button onClick={onCheckRisk} className="btn-primary">
              Cek Risiko
              <ArrowUpRight size={16} />
            </button>
            <button
              className="md:hidden btn-ghost"
              onClick={() => setOpen((v) => !v)}
              aria-label="Toggle menu"
            >
              {open ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>
        </nav>

        {/* Mobile menu */}
        {open && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-2 md:hidden glass rounded-3xl p-4 flex flex-col gap-1"
          >
            {NAV_ITEMS.map((item) =>
              item.to ? (
                <Link
                  key={item.to}
                  to={item.to}
                  className="flex items-center gap-2 rounded-2xl px-4 py-2.5 text-sm font-medium hover:bg-pulse-50"
                  onClick={() => setOpen(false)}
                >
                  <BarChart2 size={14} className="text-pulse-600" />
                  {item.label}
                </Link>
              ) : (
                <a
                  key={item.href}
                  href={item.href}
                  className="rounded-2xl px-4 py-2.5 text-sm font-medium hover:bg-pulse-50"
                  onClick={() => setOpen(false)}
                >
                  {item.label}
                </a>
              )
            )}
          </motion.div>
        )}
      </div>
    </motion.header>
  )
}
