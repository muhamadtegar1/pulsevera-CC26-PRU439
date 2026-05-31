import React, { Suspense, useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Float, MeshDistortMaterial, Environment } from '@react-three/drei'

/**
 * Mini decorative 3D blob — ringan, dipakai sebagai accent di card features.
 */
function Blob({ color = '#3B82F6' }) {
  const ref = useRef()
  useFrame((state) => {
    if (!ref.current) return
    ref.current.rotation.y = state.clock.getElapsedTime() * 0.3
    ref.current.rotation.x = Math.sin(state.clock.getElapsedTime() * 0.5) * 0.2
  })
  return (
    <mesh ref={ref}>
      <icosahedronGeometry args={[1, 24]} />
      <MeshDistortMaterial
        color={color}
        distort={0.45}
        speed={2.5}
        roughness={0.1}
        metalness={0.6}
        emissive={color}
        emissiveIntensity={0.25}
      />
    </mesh>
  )
}

export default function MiniBlobScene({ color = '#3B82F6' }) {
  return (
    <Canvas
      camera={{ position: [0, 0, 3.2], fov: 40 }}
      dpr={[1, 2]}
      gl={{ alpha: true, antialias: true }}
      style={{ background: 'transparent' }}
    >
      <Suspense fallback={null}>
        <ambientLight intensity={0.4} />
        <directionalLight position={[3, 3, 3]} intensity={1.4} />
        <pointLight position={[-3, -2, 2]} intensity={1.2} color={color} />
        <Float speed={2} rotationIntensity={0.5} floatIntensity={0.6}>
          <Blob color={color} />
        </Float>
        <Environment preset="studio" />
      </Suspense>
    </Canvas>
  )
}
