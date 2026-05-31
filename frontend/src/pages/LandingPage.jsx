import React from 'react'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import HeroSection from '../sections/HeroSection'
import StatsSection from '../sections/StatsSection'
import FeaturesSection from '../sections/FeaturesSection'
import HowItWorksSection from '../sections/HowItWorksSection'
import AboutSection from '../sections/AboutSection'
import FAQSection from '../sections/FAQSection'
import CTASection from '../sections/CTASection'

export default function LandingPage({ onCheckRisk }) {
  return (
    <div className="min-h-screen bg-gradient-pulse">
      <Navbar onCheckRisk={onCheckRisk} />
      <main>
        <HeroSection onCheckRisk={onCheckRisk} />
        <StatsSection />
        <FeaturesSection onCheckRisk={onCheckRisk} />
        <HowItWorksSection />
        <AboutSection />
        <CTASection onCheckRisk={onCheckRisk} />
        <FAQSection />
      </main>
      <Footer />
    </div>
  )
}
