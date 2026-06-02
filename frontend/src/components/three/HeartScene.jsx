import React, { useRef, useMemo, Suspense, Component } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import {
  Float,
  Sparkles,
  MeshDistortMaterial,
  Environment,
  ContactShadows,
  Sphere,
  Torus,
} from '@react-three/drei'
import * as THREE from 'three'

/**
 * Procedural 3D heart-like shape made dari dua sphere yang menyatu +
 * efek distortion organic dan emisi glow.
 */
function HeartShape() {
  const groupRef = useRef()

  useFrame((state) => {
    const t = state.clock.getElapsedTime()
    if (groupRef.current) {
      // Detak jantung — pulse scale
      const pulse = 1 + Math.sin(t * 2.4) * 0.04 + Math.sin(t * 4.8) * 0.02
      groupRef.current.scale.setScalar(pulse)
      groupRef.current.rotation.y = t * 0.25
      groupRef.current.rotation.x = Math.sin(t * 0.4) * 0.1
    }
  })

  return (
    <group ref={groupRef}>
      {/* Lobus kiri */}
      <Sphere args={[1.05, 64, 64]} position={[-0.65, 0.35, 0]}>
        <MeshDistortMaterial
          color="#EF4444"
          attach="material"
          distort={0.32}
          speed={2.4}
          roughness={0.15}
          metalness={0.4}
          emissive="#7F1D1D"
          emissiveIntensity={0.35}
        />
      </Sphere>

      {/* Lobus kanan */}
      <Sphere args={[1.05, 64, 64]} position={[0.65, 0.35, 0]}>
        <MeshDistortMaterial
          color="#DC2626"
          attach="material"
          distort={0.32}
          speed={2.4}
          roughness={0.15}
          metalness={0.4}
          emissive="#7F1D1D"
          emissiveIntensity={0.35}
        />
      </Sphere>

      {/* Apex (puncak bawah) — kerucut */}
      <mesh position={[0, -1.05, 0]} rotation={[Math.PI, 0, 0]}>
        <coneGeometry args={[1.45, 1.8, 64]} />
        <MeshDistortMaterial
          color="#B91C1C"
          attach="material"
          distort={0.18}
          speed={2}
          roughness={0.2}
          metalness={0.5}
          emissive="#450A0A"
          emissiveIntensity={0.3}
        />
      </mesh>

      {/* Aorta — torus kecil di atas */}
      <Torus args={[0.25, 0.08, 16, 64]} position={[0, 1.3, 0]} rotation={[Math.PI / 2, 0, 0]}>
        <meshStandardMaterial color="#FCA5A5" roughness={0.3} metalness={0.7} />
      </Torus>
    </group>
  )
}

/**
 * Pulse ring yang membesar dan memudar terus menerus — visualisasi detak jantung.
 */
function PulseRing({ delay = 0, color = '#3B82F6' }) {
  const ref = useRef()

  useFrame((state) => {
    const t = (state.clock.getElapsedTime() + delay) % 3
    if (ref.current) {
      const scale = 1.6 + t * 0.9
      ref.current.scale.set(scale, scale, scale)
      ref.current.material.opacity = Math.max(0, 0.6 - t * 0.22)
    }
  })

  return (
    <Torus ref={ref} args={[1.2, 0.015, 16, 100]} rotation={[Math.PI / 2, 0, 0]}>
      <meshBasicMaterial color={color} transparent opacity={0.6} />
    </Torus>
  )
}

/**
 * Orbiting molecule — sphere kecil mengitari heart, memberi kesan "data".
 */
function OrbitParticles({ count = 18 }) {
  const ref = useRef()

  const positions = useMemo(() => {
    return Array.from({ length: count }).map((_, i) => {
      const angle = (i / count) * Math.PI * 2
      const r = 2.4 + Math.random() * 0.5
      const y = (Math.random() - 0.5) * 1.5
      return { angle, r, y, speed: 0.3 + Math.random() * 0.3 }
    })
  }, [count])

  useFrame((state) => {
    const t = state.clock.getElapsedTime()
    if (!ref.current) return
    ref.current.children.forEach((child, i) => {
      const p = positions[i]
      child.position.x = Math.cos(p.angle + t * p.speed) * p.r
      child.position.z = Math.sin(p.angle + t * p.speed) * p.r
      child.position.y = p.y + Math.sin(t * 1.5 + i) * 0.15
    })
  })

  return (
    <group ref={ref}>
      {positions.map((_, i) => (
        <mesh key={i}>
          <sphereGeometry args={[0.04, 16, 16]} />
          <meshStandardMaterial
            color={i % 3 === 0 ? '#10B981' : '#3B82F6'}
            emissive={i % 3 === 0 ? '#10B981' : '#3B82F6'}
            emissiveIntensity={1.5}
          />
        </mesh>
      ))}
    </group>
  )
}

class WebGLBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { failed: false }
  }
  static getDerivedStateFromError() {
    return { failed: true }
  }
  render() {
    if (this.state.failed) {
      return (
        <div
          style={{
            width: '100%',
            height: '100%',
            borderRadius: '2rem',
            background: 'radial-gradient(ellipse at 40% 40%, #BFDBFE 0%, #EFF6FF 50%, #F0FDFA 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <svg width="160" height="160" viewBox="0 0 160 160" fill="none">
            <path
              d="M80 140 C80 140 20 100 20 55 C20 35 36 18 56 18 C66 18 75 23 80 32 C85 23 94 18 104 18 C124 18 140 35 140 55 C140 100 80 140 80 140Z"
              fill="url(#hg)"
              opacity="0.85"
            />
            <defs>
              <linearGradient id="hg" x1="20" y1="18" x2="140" y2="140" gradientUnits="userSpaceOnUse">
                <stop stopColor="#EF4444" />
                <stop offset="1" stopColor="#B91C1C" />
              </linearGradient>
            </defs>
          </svg>
        </div>
      )
    }
    return this.props.children
  }
}

/**
 * Hero scene — heart + rings + particles + lighting.
 */
export default function HeartScene() {
  return (
    <WebGLBoundary>
      <Canvas
        camera={{ position: [0, 0.4, 5.6], fov: 42 }}
        dpr={[1, 1.5]}
        gl={{ antialias: false, alpha: true, powerPreference: 'low-power' }}
        style={{ background: 'transparent' }}
      >
        <Suspense fallback={null}>
          <ambientLight intensity={0.5} />
          <directionalLight position={[5, 5, 5]} intensity={1.2} color="#FFFFFF" />
          <pointLight position={[-4, 2, 3]} intensity={1.5} color="#3B82F6" />
          <pointLight position={[4, -2, 3]} intensity={1.2} color="#EF4444" />

          <Float speed={1.5} rotationIntensity={0.3} floatIntensity={0.4}>
            <group position={[0, -0.1, 0]} scale={0.85}>
              <HeartShape />
            </group>
          </Float>

          <PulseRing delay={0} color="#3B82F6" />
          <PulseRing delay={1} color="#60A5FA" />
          <PulseRing delay={2} color="#10B981" />

          <OrbitParticles count={20} />

          <Sparkles count={60} scale={6} size={2} speed={0.4} opacity={0.6} color="#93C5FD" />

          <ContactShadows position={[0, -2.2, 0]} opacity={0.25} scale={6} blur={2.5} far={3} color="#1E3A8A" />

          <Environment preset="city" />
        </Suspense>
      </Canvas>
    </WebGLBoundary>
  )
}
