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
import InsightsPage from './pages/InsightsPage'
import { predict } from './services/api'

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { error: null }
  }
  static getDerivedStateFromError(error) {
    return { error }
  }
  componentDidCatch(error, info) {
    console.error('[ErrorBoundary]', error, info)
  }
  render() {
    if (this.state.error) {
      return (
        <div style={{ padding: 32, fontFamily: 'monospace', background: '#fee2e2', minHeight: '100vh' }}>
          <h2 style={{ color: '#dc2626' }}>Runtime Error: buka DevTools (F12) untuk detail</h2>
          <pre style={{ whiteSpace: 'pre-wrap', color: '#7f1d1d', marginTop: 16 }}>
            {this.state.error.toString()}
          </pre>
        </div>
      )
    }
    return this.props.children
  }
}

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

function InsightsRoute() {
  const navigate = useNavigate()
  return <InsightsPage onBack={() => navigate('/')} onCheckRisk={() => navigate('/check-risk')} />
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
          <Route path="/insights" element={<InsightsRoute />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </motion.div>
    </AnimatePresence>
  )
}

export default function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <AnimatedRoutes />
      </BrowserRouter>
    </ErrorBoundary>
  )
}
