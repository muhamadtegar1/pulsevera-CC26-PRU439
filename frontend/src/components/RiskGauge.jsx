import React, { useMemo } from 'react'
import { motion } from 'framer-motion'

const COLOR_BY_LABEL = {
  Rendah: { ring: '#10B981', glow: 'shadow-[0_0_60px_-8px_rgba(16,185,129,0.55)]', text: 'text-mint-500' },
  Sedang: { ring: '#F59E0B', glow: 'shadow-[0_0_60px_-8px_rgba(245,158,11,0.55)]', text: 'text-amber-500' },
  Tinggi: { ring: '#EF4444', glow: 'shadow-[0_0_60px_-8px_rgba(239,68,68,0.55)]', text: 'text-coral-500' },
}

/**
 * SVG gauge melengkung (semi-circle) dengan animasi pengisian.
 */
export default function RiskGauge({ score, label, percent }) {
  const radius = 110
  const stroke = 18
  const circumference = Math.PI * radius // semi-circle keliling

  const colorCfg = COLOR_BY_LABEL[label] || COLOR_BY_LABEL.Sedang
  const filled = useMemo(() => Math.min(1, Math.max(0, score)), [score])
  const offset = circumference * (1 - filled)

  return (
    <div className="flex flex-col items-center">
      <div className={`relative ${colorCfg.glow} rounded-full`}>
        <svg width={280} height={170} viewBox="0 0 280 170">
          {/* Track */}
          <path
            d={`M 30 150 A ${radius} ${radius} 0 0 1 250 150`}
            fill="none"
            stroke="#E2E8F0"
            strokeWidth={stroke}
            strokeLinecap="round"
          />
          {/* Filled */}
          <motion.path
            d={`M 30 150 A ${radius} ${radius} 0 0 1 250 150`}
            fill="none"
            stroke={colorCfg.ring}
            strokeWidth={stroke}
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.4, ease: 'easeOut' }}
          />
        </svg>

        {/* Number overlay */}
        <div className="absolute inset-0 flex flex-col items-center justify-end pb-2">
          <motion.p
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className={`font-display text-6xl font-bold ${colorCfg.text}`}
          >
            {Math.round(percent ?? score * 100)}
            <span className="text-3xl">%</span>
          </motion.p>
          <p className="text-sm text-ink-900/60 font-medium uppercase tracking-wider mt-1">
            Risk Score
          </p>
        </div>
      </div>

      {/* Label badge */}
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 1, type: 'spring' }}
        className="mt-6"
      >
        <span
          className="inline-flex items-center gap-2 rounded-full px-5 py-2 text-sm font-bold text-white shadow-soft"
          style={{ backgroundColor: colorCfg.ring }}
        >
          Risiko {label}
        </span>
      </motion.div>
    </div>
  )
}
