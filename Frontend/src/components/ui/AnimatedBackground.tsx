import { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Tube, MeshDistortMaterial } from '@react-three/drei'
import * as THREE from 'three'

const AnimatedTube = () => {
  const tubeRef = useRef<THREE.Mesh>(null!)
  const groupRef = useRef<THREE.Group>(null!)
  
  const curve = useMemo(() => {
    const points = []
    for (let i = 0; i < 200; i++) {
      const angle = (i / 200) * Math.PI * 16
      const radius = 3 + Math.sin(angle * 1.5) * 1
      points.push(
        new THREE.Vector3(
          Math.cos(angle) * radius,
          Math.sin(angle * 2) * 3,
          (i - 100) * 0.2
        )
      )
    }
    return new THREE.CatmullRomCurve3(points)
  }, [])

  useFrame((state) => {
    if (tubeRef.current) {
      tubeRef.current.rotation.x = state.clock.elapsedTime * 0.05
      tubeRef.current.rotation.y = state.clock.elapsedTime * 0.1
    }
    
    if (groupRef.current) {
      // Scrolling animation - move the entire group along Z axis
      groupRef.current.position.z = (state.clock.elapsedTime * 2) % 20 - 10
      groupRef.current.rotation.z = state.clock.elapsedTime * 0.02
    }
  })

  return (
    <group ref={groupRef}>
      <Tube ref={tubeRef} args={[curve, 120, 0.3, 8, false]}>
        <MeshDistortMaterial
          color="#144ee3"
          transparent
          opacity={0.6}
          distort={0.3}
          speed={2}
          roughness={0}
          metalness={0.8}
        />
      </Tube>
      <Tube args={[curve, 120, 0.4, 8, false]} position={[2, 2, 0]}>
        <MeshDistortMaterial
          color="#b043ff"
          transparent
          opacity={0.4}
          distort={0.4}
          speed={1.5}
          roughness={0}
          metalness={0.8}
        />
      </Tube>
      <Tube args={[curve, 120, 0.2, 8, false]} position={[-2, -2, 0]}>
        <MeshDistortMaterial
          color="#ff5f5f"
          transparent
          opacity={0.5}
          distort={0.5}
          speed={2.5}
          roughness={0}
          metalness={0.8}
        />
      </Tube>
      <ambientLight intensity={0.2} />
      <pointLight position={[10, 10, 10]} intensity={1} color="#144ee3" />
      <pointLight position={[-10, -10, -10]} intensity={1} color="#b043ff" />
      <pointLight position={[0, 0, 15]} intensity={0.8} color="#ff5f5f" />
    </group>
  )
}

const AnimatedBackground = () => {
  return (
    <div className="fixed inset-0 -z-10">
      <Canvas
        camera={{ position: [0, 0, 8], fov: 75 }}
        dpr={[1, 2]}
        performance={{ min: 0.5 }}
      >
        <fog attach="fog" args={['#000000', 5, 25]} />
        <AnimatedTube />
      </Canvas>
    </div>
  )
}

export default AnimatedBackground