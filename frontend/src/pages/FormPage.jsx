import React, { useState, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  ArrowLeft,
  ArrowRight,
  ArrowUpRight,
  User,
  Calendar,
  Ruler,
  Weight,
  Moon,
  Dumbbell,
  Cigarette,
  Wine,
  HeartPulse,
  Droplet,
  Sparkles,
} from 'lucide-react'

const AGE_OPTIONS = [
  { value: 1, label: '18 – 24' },
  { value: 2, label: '25 – 29' },
  { value: 3, label: '30 – 34' },
  { value: 4, label: '35 – 39' },
  { value: 5, label: '40 – 44' },
  { value: 6, label: '45 – 49' },
  { value: 7, label: '50 – 54' },
  { value: 8, label: '55 – 59' },
  { value: 9, label: '60 – 64' },
  { value: 10, label: '65 – 69' },
  { value: 11, label: '70 – 74' },
  { value: 12, label: '75 – 79' },
  { value: 13, label: '80+' },
]

const SMOKER_OPTIONS = [
  { value: 'Never', label: 'Tidak pernah' },
  { value: 'Former', label: 'Mantan perokok' },
  { value: 'Current-some', label: 'Perokok (kadang)' },
  { value: 'Current-every', label: 'Perokok (setiap hari)' },
]

const HEALTH_OPTIONS = [
  { value: 'Poor', label: 'Buruk' },
  { value: 'Fair', label: 'Cukup' },
  { value: 'Good', label: 'Baik' },
  { value: 'Very good', label: 'Sangat Baik' },
  { value: 'Excellent', label: 'Sangat Baik Sekali' },
]

const DIABETES_OPTIONS = [
  { value: 'No', label: 'Tidak' },
  { value: 'Pre-diabetes', label: 'Pre-diabetes' },
  { value: 'Yes', label: 'Ya' },
]

const STEPS = [
  {
    title: 'Profil Dasar',
    description: 'Jenis kelamin dan kategori usia Anda',
    fields: ['sex', 'age_category'],
  },
  {
    title: 'Antropometri',
    description: 'Tinggi dan berat badan untuk hitung BMI',
    fields: ['height_meters', 'weight_kg'],
  },
  {
    title: 'Gaya Hidup',
    description: 'Aktivitas fisik dan pola tidur Anda',
    fields: ['physical_activities', 'sleep_hours'],
  },
  {
    title: 'Konsumsi',
    description: 'Status merokok dan konsumsi alkohol',
    fields: ['smoker_status', 'alcohol'],
  },
  {
    title: 'Kondisi Kesehatan',
    description: 'Kesehatan umum dan riwayat diabetes',
    fields: ['general_health', 'diabetes'],
  },
]

const INITIAL = {
  sex: '',
  age_category: '',
  height_meters: '',
  weight_kg: '',
  physical_activities: '',
  sleep_hours: 7,
  smoker_status: '',
  alcohol: '',
  general_health: '',
  diabetes: 'No',
}

export default function FormPage({ onBack, onSubmit }) {
  const [step, setStep] = useState(0)
  const [data, setData] = useState(INITIAL)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const currentStep = STEPS[step]
  const isLast = step === STEPS.length - 1

  const stepValid = useMemo(() => {
    return currentStep.fields.every((f) => {
      const v = data[f]
      return v !== '' && v !== undefined && v !== null
    })
  }, [data, currentStep.fields])

  const update = (field) => (value) => setData((d) => ({ ...d, [field]: value }))

  const next = () => {
    if (!stepValid) return
    setStep((s) => Math.min(STEPS.length - 1, s + 1))
  }

  const prev = () => {
    if (step === 0) return onBack()
    setStep((s) => Math.max(0, s - 1))
  }

  const submit = async () => {
    if (!stepValid) return
    setLoading(true)
    setError(null)
    try {
      const payload = {
        ...data,
        age_category: Number(data.age_category),
        height_meters: Number(data.height_meters),
        weight_kg: Number(data.weight_kg),
        sleep_hours: Number(data.sleep_hours),
      }
      await onSubmit(payload)
    } catch (e) {
      setError(e?.response?.data?.error || e?.message || 'Terjadi kesalahan tak terduga.')
      setLoading(false)
    }
  }

  const progress = ((step + 1) / STEPS.length) * 100

  return (
    <div className="min-h-screen bg-gradient-pulse py-10 px-4 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-3xl">
        {/* Top bar */}
        <div className="flex items-center justify-between mb-8">
          <button onClick={prev} className="btn-secondary">
            <ArrowLeft size={16} />
            {step === 0 ? 'Beranda' : 'Sebelumnya'}
          </button>
          <span className="badge">
            Langkah {step + 1} / {STEPS.length}
          </span>
        </div>

        {/* Progress bar */}
        <div className="mb-8 h-2 rounded-full bg-white shadow-soft overflow-hidden ring-1 ring-pulse-100">
          <motion.div
            className="h-full bg-gradient-to-r from-pulse-600 to-mint-500"
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.4 }}
          />
        </div>

        {/* Form card */}
        <div className="glass rounded-3xl p-6 sm:p-10">
          <AnimatePresence mode="wait">
            <motion.div
              key={step}
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -30 }}
              transition={{ duration: 0.25 }}
            >
              <h2 className="font-display text-3xl sm:text-4xl font-bold mb-2">
                {currentStep.title}
              </h2>
              <p className="text-ink-900/70 mb-8">{currentStep.description}</p>

              <div className="space-y-6">
                {currentStep.fields.map((field) => (
                  <Field key={field} name={field} value={data[field]} onChange={update(field)} />
                ))}
              </div>
            </motion.div>
          </AnimatePresence>

          {error && (
            <div className="mt-6 rounded-2xl bg-coral-500/10 px-4 py-3 text-sm text-coral-600 ring-1 ring-coral-500/20">
              {error}
            </div>
          )}

          <div className="mt-10 flex items-center justify-between gap-3">
            <button onClick={prev} className="btn-secondary">
              <ArrowLeft size={16} />
              Kembali
            </button>

            {!isLast ? (
              <button onClick={next} disabled={!stepValid} className="btn-primary disabled:opacity-40 disabled:cursor-not-allowed">
                Lanjut
                <ArrowRight size={16} />
              </button>
            ) : (
              <button
                onClick={submit}
                disabled={!stepValid || loading}
                className="btn-primary disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <>
                    <Sparkles size={16} className="animate-spin" />
                    Menganalisis...
                  </>
                ) : (
                  <>
                    Cek Risiko Saya
                    <ArrowUpRight size={16} />
                  </>
                )}
              </button>
            )}
          </div>
        </div>

        <p className="mt-6 text-center text-xs text-ink-900/60">
          🔒 Data Anda tidak disimpan. Diproses real-time dan langsung dilupakan.
        </p>
      </div>
    </div>
  )
}

/* ──────────────────────────────────────────────────────────────────── */

function Field({ name, value, onChange }) {
  const Cfg = FIELD_CONFIG[name]
  if (!Cfg) return null
  return <Cfg.component label={Cfg.label} icon={Cfg.icon} value={value} onChange={onChange} {...Cfg.props} />
}

/* ── Reusable inputs ────────────────────────────────────────────────── */

function RadioCards({ label, icon: Icon, value, onChange, options }) {
  return (
    <div>
      <label className="label flex items-center gap-2">
        {Icon && <Icon size={16} className="text-pulse-700" />}
        {label}
      </label>
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
        {options.map((opt) => (
          <button
            type="button"
            key={opt.value}
            onClick={() => onChange(opt.value)}
            className={`rounded-2xl px-4 py-3 text-sm font-medium shadow-soft ring-1 transition-all ${
              value === opt.value
                ? 'bg-pulse-700 text-white ring-pulse-700 shadow-glow-blue'
                : 'bg-white text-ink-900 ring-pulse-100 hover:ring-pulse-300'
            }`}
          >
            {opt.label}
          </button>
        ))}
      </div>
    </div>
  )
}

function Dropdown({ label, icon: Icon, value, onChange, options, placeholder = 'Pilih...' }) {
  return (
    <div>
      <label className="label flex items-center gap-2">
        {Icon && <Icon size={16} className="text-pulse-700" />}
        {label}
      </label>
      <select
        className="input-field appearance-none cursor-pointer"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        <option value="">{placeholder}</option>
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>{opt.label}</option>
        ))}
      </select>
    </div>
  )
}

function NumberInput({ label, icon: Icon, value, onChange, min, max, step = 1, suffix }) {
  return (
    <div>
      <label className="label flex items-center gap-2">
        {Icon && <Icon size={16} className="text-pulse-700" />}
        {label}
      </label>
      <div className="relative">
        <input
          type="number"
          className="input-field pr-14"
          value={value}
          min={min}
          max={max}
          step={step}
          onChange={(e) => onChange(e.target.value)}
        />
        {suffix && (
          <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-ink-900/60 font-medium">
            {suffix}
          </span>
        )}
      </div>
      <p className="mt-1 text-xs text-ink-900/50">
        Rentang valid: {min} – {max} {suffix}
      </p>
    </div>
  )
}

function Slider({ label, icon: Icon, value, onChange, min, max, step = 1, suffix }) {
  return (
    <div>
      <label className="label flex items-center justify-between">
        <span className="flex items-center gap-2">
          {Icon && <Icon size={16} className="text-pulse-700" />}
          {label}
        </span>
        <span className="font-display text-2xl font-bold text-pulse-700">
          {value} <span className="text-sm font-medium text-ink-900/60">{suffix}</span>
        </span>
      </label>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full accent-pulse-700 cursor-pointer"
      />
      <div className="flex justify-between text-xs text-ink-900/50 mt-1">
        <span>{min} {suffix}</span>
        <span>{max} {suffix}</span>
      </div>
    </div>
  )
}

/* ── Field configuration ────────────────────────────────────────────── */

const FIELD_CONFIG = {
  sex: {
    label: 'Jenis Kelamin',
    icon: User,
    component: RadioCards,
    props: {
      options: [
        { value: 'Male', label: 'Laki-laki' },
        { value: 'Female', label: 'Perempuan' },
      ],
    },
  },
  age_category: {
    label: 'Kategori Usia',
    icon: Calendar,
    component: Dropdown,
    props: { options: AGE_OPTIONS, placeholder: 'Pilih rentang usia Anda' },
  },
  height_meters: {
    label: 'Tinggi Badan',
    icon: Ruler,
    component: NumberInput,
    props: { min: 1.0, max: 2.5, step: 0.01, suffix: 'm' },
  },
  weight_kg: {
    label: 'Berat Badan',
    icon: Weight,
    component: NumberInput,
    props: { min: 30, max: 200, step: 0.1, suffix: 'kg' },
  },
  physical_activities: {
    label: 'Apakah Anda melakukan aktivitas fisik rutin (selain pekerjaan)?',
    icon: Dumbbell,
    component: RadioCards,
    props: {
      options: [
        { value: 'Yes', label: 'Ya, rutin' },
        { value: 'No', label: 'Tidak / jarang' },
      ],
    },
  },
  sleep_hours: {
    label: 'Rata-rata Jam Tidur per Malam',
    icon: Moon,
    component: Slider,
    props: { min: 1, max: 14, step: 1, suffix: 'jam' },
  },
  smoker_status: {
    label: 'Status Merokok',
    icon: Cigarette,
    component: RadioCards,
    props: { options: SMOKER_OPTIONS },
  },
  alcohol: {
    label: 'Apakah Anda mengonsumsi alkohol?',
    icon: Wine,
    component: RadioCards,
    props: {
      options: [
        { value: 'Yes', label: 'Ya' },
        { value: 'No', label: 'Tidak' },
      ],
    },
  },
  general_health: {
    label: 'Bagaimana Anda menilai kondisi kesehatan Anda secara umum?',
    icon: HeartPulse,
    component: RadioCards,
    props: { options: HEALTH_OPTIONS },
  },
  diabetes: {
    label: 'Apakah Anda memiliki riwayat diabetes?',
    icon: Droplet,
    component: RadioCards,
    props: { options: DIABETES_OPTIONS },
  },
}
