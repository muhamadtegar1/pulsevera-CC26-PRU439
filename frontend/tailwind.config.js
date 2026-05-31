/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // Medical-inspired palette (Nuvica-style adapted untuk Pulsevera)
        ink: {
          50: '#F8FAFC',
          100: '#F1F5F9',
          900: '#0F172A',
          950: '#020617',
        },
        pulse: {
          50: '#EFF6FF',
          100: '#DBEAFE',
          200: '#BFDBFE',
          300: '#93C5FD',
          400: '#60A5FA',
          500: '#3B82F6',
          600: '#2563EB',
          700: '#1D4ED8',
          800: '#1E3A8A',
          900: '#172554',
        },
        mint: {
          400: '#34D399',
          500: '#10B981',
          600: '#059669',
        },
        coral: {
          400: '#FB7185',
          500: '#EF4444',
          600: '#DC2626',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['"Space Grotesk"', 'Inter', 'system-ui', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-pulse': 'linear-gradient(135deg, #DBEAFE 0%, #EFF6FF 50%, #F0FDFA 100%)',
        'gradient-hero': 'radial-gradient(ellipse at top, #BFDBFE 0%, #EFF6FF 45%, #FFFFFF 100%)',
        'gradient-card': 'linear-gradient(180deg, rgba(255,255,255,0.7) 0%, rgba(255,255,255,0.3) 100%)',
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.12)',
        'soft': '0 4px 24px -8px rgba(15, 23, 42, 0.08)',
        'glow-blue': '0 0 40px -8px rgba(37, 99, 235, 0.45)',
        'glow-red': '0 0 40px -8px rgba(239, 68, 68, 0.45)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
        'spin-slow': 'spin 18s linear infinite',
        'fade-up': 'fadeUp 0.6s ease-out',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-14px)' },
        },
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}
