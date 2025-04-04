/*
Auto-generated by: https://github.com/pmndrs/gltfjsx
*/

import React, { useRef } from 'react'
import { useGLTF } from '@react-three/drei'

export default function Ball(props) {
  const group = useRef()
  const { nodes, materials } = useGLTF('/models/Ball.glb')

  // quick experiment if we wanted to go more "tron"
  // console.log(materials)
  // materials.Ball.wireframe = true;

  return (
    <group ref={group} {...props} dispose={null}>
      <mesh
        castShadow
        receiveShadow
        geometry={nodes.Ball.geometry}
        material={materials['Ball']}
      />
    </group>
  )
}

useGLTF.preload('/models/Ball.glb')
