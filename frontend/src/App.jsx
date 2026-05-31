import React, { useEffect } from 'react'
import {
  BrowserRouter,
  Routes,
  Route,
  useNavigate,
  useLocation,
  Navigate,
} from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import LandingPage from './pages/LandingPage'
import FormPage from './pages/FormPage'
import ResultPage from './pages/ResultPage'
import { predict } from './services/api'

function LandingRoute() {
  const navigate = useNavigate()
  return <LandingPage onCheckRisk={() => navigate('/check-risk')} />
}

function FormRoute() {
  const navigate = useNavigate()

  const handleSubmit = async (data) => {
    try {
      const res = await predict(data)
      navigate('/result', { state: { result: res, formData: data } })
    } catch (err) {
      throw err
    }
  }

  return <FormPage onBack={() => navigate('/')} onSubmit={handleSubmit} />
}

function ResultRoute() {
  const navigate = useNavigate()
  const location = useLocation()
  const state = location.state || {}

  if (!state.result) {
    return <Navigate to="/" replace />
  }

  return (
    <ResultPage
      result={state.result}
      formData={state.formData}
      onBack={() => navigate('/')}
      onRetake={() => navigate('/check-risk')}
    />
  )
}

function AnimatedRoutes() {
  const location = useLocation()

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, [location.pathname])

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.3 }}
      >
        <Routes location={location}>
          <Route path="/" element={<LandingRoute />} />
          <Route path="/check-risk" element={<FormRoute />} />
          <Route path="/result" element={<ResultRoute />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </motion.div>
    </AnimatePresence>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AnimatedRoutes />
    </BrowserRouter>
  )
}
