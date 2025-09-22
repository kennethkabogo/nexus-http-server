import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Stars } from '@react-three/drei';

function RotatingBox() {
  const mesh = useRef();
  useFrame(() => {
    if (mesh.current) {
      mesh.current.rotation.x += 0.001;
      mesh.current.rotation.y += 0.001;
    }
  });
  return (
    <mesh ref={mesh} position={[0, 0, 0]}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color={'#8e44ad'} />
    </mesh>
  );
}

function ThreeDBackground() {
  return (
    <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', zIndex: -1 }}>
      <Canvas>
        <ambientLight intensity={0.5} />
        <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
        <pointLight position={[-10, -10, -10]} />
        <Stars />
        <RotatingBox />
      </Canvas>
    </div>
  );
}

export default ThreeDBackground;