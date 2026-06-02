import React, { useState, useMemo, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  ArrowLeft,
  ArrowRight,
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
  Info,
  Scale,
  Heart,
} from 'lucide-react'

const LOADING_MESSAGES = [
  'Menganalisis profil kesehatan...',
  'Memproses 46 faktor risiko...',
  'Menyiapkan rekomendasi personal...',
]

const AGE_OPTIONS = [
  { value: 1, label: '18 – 24 tahun' },
  { value: 2, label: '25 – 29 tahun' },
  { value: 3, label: '30 – 34 tahun' },
  { value: 4, label: '35 – 39 tahun' },
  { value: 5, label: '40 – 44 tahun' },
  { value: 6, label: '45 – 49 tahun' },
  { value: 7, label: '50 – 54 tahun' },
  { value: 8, label: '55 – 59 tahun' },
  { value: 9, label: '60 – 64 tahun' },
  { value: 10, label: '65 – 69 tahun' },
  { value: 11, label: '70 – 74 tahun' },
  { value: 12, label: '75 – 79 tahun' },
  { value: 13, label: '80 tahun ke atas' },
]

const SMOKER_OPTIONS = [
  { value: 'Never', label: 'Tidak pernah', hint: 'Belum pernah merokok seumur hidup' },
  { value: 'Former', label: 'Mantan perokok', hint: 'Pernah merokok, sekarang sudah berhenti total' },
  { value: 'Current-some', label: 'Kadang-kadang', hint: 'Masih merokok, tapi tidak setiap hari' },
  { value: 'Current-every', label: 'Setiap hari', hint: 'Merokok hampir setiap hari' },
]

const HEALTH_OPTIONS = [
  { value: 'Poor', label: 'Buruk', hint: 'Sering sakit / banyak keluhan kesehatan' },
  { value: 'Fair', label: 'Cukup', hint: 'Kadang sakit / ada beberapa keluhan' },
  { value: 'Good', label: 'Baik', hint: 'Jarang sakit / kondisi cukup oke' },
  { value: 'Very good', label: 'Sangat Baik', hint: 'Hampir tidak pernah sakit' },
  { value: 'Excellent', label: 'Sangat Baik Sekali', hint: 'Sehat total / fit prima' },
]

const DIABETES_OPTIONS = [
  { value: 'No', label: 'Tidak', hint: 'Belum pernah didiagnosis diabetes oleh dokter' },
  { value: 'Pre-diabetes', label: 'Pre-diabetes', hint: 'Gula darah di atas normal tapi belum diabetes' },
  { value: 'Yes', label: 'Ya', hint: 'Sudah didiagnosis diabetes oleh dokter' },
]

const STEPS = [
  {
    title: 'Profil Dasar',
    description: 'Jenis kelamin dan kategori usia Anda',
    fields: ['sex', 'age_category'],
  },
  {
    title: 'Antropometri',
    description: 'Tinggi dan berat badan untuk hitung BMI otomatis',
    fields: ['height_meters', 'weight_kg'],
    extras: ['bmi_preview'],
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
  const [loadingStep, setLoadingStep] = useState(0)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!loading) { setLoadingStep(0); return }
    const id = setInterval(() => setLoadingStep((s) => (s + 1) % LOADING_MESSAGES.length), 900)
    return () => clearInterval(id)
  }, [loading])

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
        height_meters: Number(data.height_meters) / 100,
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
                {currentStep.extras?.includes('bmi_preview') && (
                  <BMIPreview height={data.height_meters} weight={data.weight_kg} />
                )}
              </div>
            </motion.div>
          </AnimatePresence>

          {loading && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-8 flex items-center gap-4 rounded-2xl bg-pulse-50 p-4 ring-1 ring-pulse-200"
            >
              <span className="grid h-12 w-12 shrink-0 place-items-center rounded-xl bg-gradient-to-br from-pulse-600 to-pulse-800 text-white shadow-glow-blue">
                <Heart size={20} fill="white" strokeWidth={0} className="animate-pulse" />
              </span>
              <div>
                <p className="font-semibold text-pulse-800">{LOADING_MESSAGES[loadingStep]}</p>
                <p className="text-xs text-pulse-600/70">Biasanya selesai dalam 1–3 detik</p>
              </div>
            </motion.div>
          )}

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
                    Tunggu sebentar...
                  </>
                ) : (
                  <>
                    Lihat Hasil
                    <ArrowRight size={16} />
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
  return (
    <Cfg.component
      label={Cfg.label}
      icon={Cfg.icon}
      helpText={Cfg.helpText}
      value={value}
      onChange={onChange}
      {...Cfg.props}
    />
  )
}

/* ── BMI Auto Preview (Mentor poin 4: real-time feedback) ───────────── */

function BMIPreview({ height, weight }) {
  const h = parseFloat(height) / 100
  const w = parseFloat(weight)

  if (!h || !w || h <= 0 || w <= 0) {
    return (
      <div className="rounded-2xl bg-pulse-50 p-4 ring-1 ring-pulse-100">
        <div className="flex items-center gap-3 text-sm text-ink-900/60">
          <Scale size={18} className="text-pulse-600" />
          <span>BMI akan dihitung otomatis setelah Anda isi tinggi & berat</span>
        </div>
      </div>
    )
  }

  const bmi = w / (h * h)
  let category, color, advice
  if (bmi < 18.5) {
    category = 'Underweight'
    color = 'bg-amber-100 ring-amber-300 text-amber-900'
    advice = 'BMI di bawah ideal. Pertimbangkan konsultasi gizi.'
  } else if (bmi < 25) {
    category = 'Ideal'
    color = 'bg-mint-100 ring-mint-300 text-mint-900'
    advice = 'BMI Anda dalam rentang ideal. Pertahankan!'
  } else if (bmi < 30) {
    category = 'Overweight'
    color = 'bg-amber-100 ring-amber-300 text-amber-900'
    advice = 'Sedikit di atas ideal. Mulai aktivitas fisik rutin akan membantu.'
  } else {
    category = 'Obesitas'
    color = 'bg-coral-100 ring-coral-300 text-coral-900'
    advice = 'BMI tergolong obesitas. Konsultasi dokter untuk program penurunan berat sehat.'
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className={`rounded-2xl p-4 ring-1 ${color}`}
    >
      <div className="flex items-center justify-between gap-3 flex-wrap">
        <div className="flex items-center gap-3">
          <Scale size={20} />
          <div>
            <p className="text-xs uppercase tracking-wider opacity-70">BMI Anda</p>
            <p className="font-display text-3xl font-bold">{bmi.toFixed(1)}</p>
          </div>
        </div>
        <div className="text-right">
          <p className="font-bold">{category}</p>
          <p className="text-xs opacity-80 max-w-xs">{advice}</p>
        </div>
      </div>
      <div className="mt-3 text-xs opacity-70">
        <strong>Rentang BMI:</strong> &lt; 18.5 Kurus · 18.5–24.9 Ideal · 25–29.9 Lebih · ≥ 30 Obesitas
      </div>
    </motion.div>
  )
}

/* ── Reusable inputs (dengan help text support) ──────────────────────── */

function FieldLabel({ icon: Icon, label, helpText }) {
  return (
    <div className="mb-2">
      <label className="label flex items-center gap-2 mb-0">
        {Icon && <Icon size={16} className="text-pulse-700" />}
        {label}
      </label>
      {helpText && (
        <p className="mt-1 flex items-start gap-1.5 text-xs text-ink-900/55 leading-snug">
          <Info size={12} className="mt-0.5 shrink-0 text-pulse-500" />
          <span>{helpText}</span>
        </p>
      )}
    </div>
  )
}

function RadioCards({ label, icon: Icon, helpText, value, onChange, options }) {
  const selectedOpt = options.find((o) => o.value === value)
  return (
    <div>
      <FieldLabel icon={Icon} label={label} helpText={helpText} />
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
      {selectedOpt?.hint && (
        <motion.p
          initial={{ opacity: 0, y: -4 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-2 text-xs italic text-pulse-700/80"
        >
          ↳ {selectedOpt.hint}
        </motion.p>
      )}
    </div>
  )
}

function Dropdown({ label, icon: Icon, helpText, value, onChange, options, placeholder = 'Pilih...' }) {
  return (
    <div>
      <FieldLabel icon={Icon} label={label} helpText={helpText} />
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

function NumberInput({ label, icon: Icon, helpText, value, onChange, min, max, step = 1, suffix, exampleText }) {
  return (
    <div>
      <FieldLabel icon={Icon} label={label} helpText={helpText} />
      <div className="relative">
        <input
          type="number"
          className="input-field pr-14"
          value={value}
          min={min}
          max={max}
          step={step}
          onChange={(e) => onChange(e.target.value)}
          placeholder={exampleText}
        />
        {suffix && (
          <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-ink-900/60 font-medium">
            {suffix}
          </span>
        )}
      </div>
      <p className="mt-1 text-xs text-ink-900/50">
        Rentang valid: {min} – {max} {suffix}
        {exampleText && <span className="ml-2 text-pulse-600/80">· contoh: {exampleText}</span>}
      </p>
    </div>
  )
}

function Slider({ label, icon: Icon, helpText, value, onChange, min, max, step = 1, suffix, marks = [] }) {
  return (
    <div>
      <FieldLabel icon={Icon} label={label} helpText={helpText} />
      <div className="flex items-center justify-end mb-2">
        <span className="font-display text-2xl font-bold text-pulse-700">
          {value} <span className="text-sm font-medium text-ink-900/60">{suffix}</span>
        </span>
      </div>
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
      {marks.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-2">
          {marks.map((m) => (
            <span
              key={m.value}
              className={`text-[10px] rounded-full px-2 py-0.5 ring-1 ${
                value === m.value
                  ? 'bg-pulse-700 text-white ring-pulse-700'
                  : 'bg-white text-ink-900/60 ring-pulse-100'
              }`}
            >
              {m.value} {suffix} = {m.label}
            </span>
          ))}
        </div>
      )}
    </div>
  )
}

/* ── Field configuration (dengan helpText & contoh) ──────────────────── */

const FIELD_CONFIG = {
  sex: {
    label: 'Jenis Kelamin',
    icon: User,
    helpText: 'Pria umumnya berisiko lebih tinggi terhadap penyakit jantung di usia muda; wanita meningkat setelah menopause.',
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
    helpText: 'Risiko kardiovaskular meningkat seiring usia, terutama setelah 45 (pria) dan 55 (wanita).',
    component: Dropdown,
    props: { options: AGE_OPTIONS, placeholder: 'Pilih rentang usia Anda' },
  },
  height_meters: {
    label: 'Tinggi Badan',
    icon: Ruler,
    helpText: 'Masukkan tinggi badan dalam sentimeter, contoh: 165. Digunakan untuk menghitung BMI otomatis.',
    component: NumberInput,
    props: { min: 100, max: 250, step: 1, suffix: 'cm', exampleText: '165' },
  },
  weight_kg: {
    label: 'Berat Badan',
    icon: Weight,
    helpText: 'Berat dalam kilogram. Bersama tinggi badan akan otomatis dihitung BMI Anda.',
    component: NumberInput,
    props: { min: 30, max: 200, step: 0.1, suffix: 'kg', exampleText: '60' },
  },
  physical_activities: {
    label: 'Apakah Anda berolahraga atau aktivitas fisik di luar pekerjaan?',
    icon: Dumbbell,
    helpText: 'Minimal 150 menit/minggu aktivitas sedang (jalan cepat, sepeda, renang) dianggap rutin.',
    component: RadioCards,
    props: {
      options: [
        { value: 'Yes', label: 'Ya, rutin', hint: 'Olahraga ≥ 3x/minggu atau aktif bergerak setiap hari' },
        { value: 'No', label: 'Tidak / jarang', hint: 'Jarang berolahraga atau lebih banyak duduk' },
      ],
    },
  },
  sleep_hours: {
    label: 'Rata-rata Jam Tidur per Malam',
    icon: Moon,
    helpText: 'Rekomendasi orang dewasa: 7–9 jam. Kurang/lebih dari itu terkait peningkatan risiko jantung.',
    component: Slider,
    props: {
      min: 1,
      max: 14,
      step: 1,
      suffix: 'jam',
      marks: [
        { value: 5, label: 'Kurang' },
        { value: 7, label: 'Ideal' },
        { value: 10, label: 'Berlebihan' },
      ],
    },
  },
  smoker_status: {
    label: 'Status Merokok',
    icon: Cigarette,
    helpText: 'Termasuk rokok konvensional, vape, dan rokok elektrik. Pilih kondisi yang paling menggambarkan Anda saat ini.',
    component: RadioCards,
    props: { options: SMOKER_OPTIONS },
  },
  alcohol: {
    label: 'Apakah Anda mengonsumsi alkohol dalam 30 hari terakhir?',
    icon: Wine,
    helpText: 'Termasuk bir, anggur, atau minuman beralkohol lainnya — baik sesekali maupun rutin.',
    component: RadioCards,
    props: {
      options: [
        { value: 'Yes', label: 'Ya', hint: 'Pernah konsumsi alkohol dalam 30 hari terakhir' },
        { value: 'No', label: 'Tidak', hint: 'Tidak minum alkohol sama sekali dalam 30 hari terakhir' },
      ],
    },
  },
  general_health: {
    label: 'Bagaimana Anda menilai kondisi kesehatan Anda secara umum?',
    icon: HeartPulse,
    helpText: 'Self-assessment sederhana — pilih yang paling mendekati perasaan Anda tentang kesehatan saat ini.',
    component: RadioCards,
    props: { options: HEALTH_OPTIONS },
  },
  diabetes: {
    label: 'Riwayat Diabetes',
    icon: Droplet,
    helpText: 'Apakah dokter pernah mendiagnosis Anda diabetes atau pre-diabetes (gula darah di atas normal)?',
    component: RadioCards,
    props: { options: DIABETES_OPTIONS },
  },
}
