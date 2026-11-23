# The web stack

Read this file at step 12 of `three-d`. It covers the choice of stack, loading compressed files, and the performance rules for the build.

Evidence. The React Three Fiber performance rules (on-demand rendering, adaptive pixel ratio, instancing, no allocation in the frame loop, hide with `visible`, level of detail, cached loaders, gltfjsx, nested suspense) come from its "Scaling performance" and "Performance pitfalls" pages, read 2026-11-23. Library licenses come from the asset catalog, checked 2026-11-23. The code below is from memory of the three.js, React Three Fiber, drei and model-viewer APIs; it is UNTESTED in this kit. Pin versions and check each API against the installed version.

## 1. Choose the stack

| Stack | License | Best for | Watch out |
| --- | --- | --- | --- |
| A model-viewing web component | Apache-2.0 | Product viewers: orbit, zoom, AR, poster, hotspots, with little code | Limited scene control |
| three.js | MIT | Any custom scene in plain JavaScript | API changes between releases; pin the version |
| React Three Fiber with drei | MIT | Scenes in a React app; declarative, with many helpers | React version requirements; drei environment presets load from a CDN; self-host instead |
| Threlte | MIT | Scenes in a Svelte app | Smaller ecosystem |
| A browser 3D design tool's runtime | Proprietary | Fast designer-made scenes | Free-plan watermark; commercial terms not verified; lock-in |
| A library WebGL scene from a 3D connector | Per the connector's terms | A finished hero scene, recolored through its config | One scene per HTML file; tint only through its config map |

Choose:

1. Product viewer with rotate, zoom and AR: the web component.
2. Custom scene in a React app: React Three Fiber.
3. Custom scene with no framework, or in another framework: three.js, or that framework's binding.
4. A ready hero from a 3D library the user chose: the library scene, tinted through its config, with the library's guide leading.

A new runtime library is an outside asset. `find-assets` reads its license and records the exact version.

## 2. Loading compressed files

A file compressed with Meshopt, Draco or KTX2 needs the matching decoder in the loader.

| File uses | Loader needs |
| --- | --- |
| Meshopt geometry | The Meshopt decoder set on the glTF loader |
| Draco geometry | A Draco loader with its decoder files, self-hosted |
| KTX2 textures | A KTX2 loader with the Basis transcoder files, self-hosted, and a support check against the renderer |

three.js, from memory:

```js
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const renderer = new THREE.WebGLRenderer({ antialias: true, canvas });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;

const ktx2 = new KTX2Loader().setTranscoderPath('/vendor/basis/').detectSupport(renderer);
const loader = new GLTFLoader().setKTX2Loader(ktx2).setMeshoptDecoder(MeshoptDecoder);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(35, canvas.clientWidth / canvas.clientHeight, 0.1, 50);
const controls = new OrbitControls(camera, renderer.domElement);

function render() { renderer.render(scene, camera); }
controls.addEventListener('change', render);          // render on demand, not every frame

loader.load('/3d/chair/chair.glb', (gltf) => { scene.add(gltf.scene); render(); });
```

The model-viewing web component, from memory of its attributes:

```html
<model-viewer
  src="/3d/chair/chair.glb"
  poster="/3d/chair/poster.webp"
  alt="Oak dining chair with a woven seat, shown in three-quarter view"
  camera-controls
  camera-orbit="30deg 75deg 2m"
  min-camera-orbit="auto 20deg 0.6m"
  max-camera-orbit="auto 100deg 2.5m"
  environment-image="/3d/hdri/studio-1k.hdr"
  shadow-intensity="1"
  ar ar-modes="webxr scene-viewer quick-look"
  loading="lazy">
</model-viewer>
```

React Three Fiber with drei, from memory:

```jsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment, useGLTF, PerformanceMonitor } from '@react-three/drei';
import { Suspense, useState } from 'react';

function Chair(props) {
  const { scene } = useGLTF('/3d/chair/chair.glb');   // cached by URL
  return <primitive object={scene} {...props} />;
}

export function ChairViewer() {
  const [dpr, setDpr] = useState(1.5);
  return (
    <Canvas frameloop="demand" dpr={dpr} camera={{ position: [1.2, 1.1, 2], fov: 35 }}>
      <PerformanceMonitor onDecline={() => setDpr(1)} onIncline={() => setDpr(2)} />
      <Suspense fallback={null}>
        <Chair />
        <Environment files="/3d/hdri/studio-1k.hdr" />
      </Suspense>
      <OrbitControls makeDefault enableDamping minDistance={0.6} maxDistance={2.5}
                     minPolarAngle={0.35} maxPolarAngle={1.75} />
    </Canvas>
  );
}
```

`gltfjsx` turns a GLB into a component with named meshes and materials, which makes parts addressable for a configurator.

## 3. Performance rules for the build

| Rule | Why |
| --- | --- |
| Render on demand for a static scene | A loop that renders every frame drains the battery for no change |
| Cap the device pixel ratio at 1 to 2; lower it when frames drop | Pixel count grows with the square of the ratio |
| Reuse geometries and materials | Each new one costs memory and may add a draw call |
| Instance repeated objects | One instanced mesh can draw very many copies in one call |
| No object creation, allocation or state updates in the frame loop | They cause garbage collection and re-renders |
| Animate by mutating refs with the frame delta | Frame-rate independent and render-free |
| Hide with `visible`, do not unmount and remount | Remounting recompiles and re-uploads |
| Use level of detail for large scenes | Far objects use lighter meshes |
| Load through a cached loader | One request and one parse per file |
| Pause rendering off screen and in a hidden tab | No work nobody sees |
| Keep draw calls to a few hundred at most | Each call has a fixed CPU cost |

Pause when off screen, for a continuous loop:

```js
let visible = true;
new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(canvas);
renderer.setAnimationLoop(() => {
  if (!visible || document.hidden) return;
  controls.update();
  render();
});
```

## 4. Integration with the page

1. The canvas sits in a container with fixed dimensions, so the page does not shift when it loads.
2. The poster image fills the same box first.
3. Load the 3D library and the model after the page's main content: lazily, when the container nears the viewport, or after an interaction.
4. Text, prices and buttons are HTML outside or over the canvas. They never wait for WebGL.
5. Colors around the canvas (background, controls, hotspot labels) use the project's tokens.
6. Self-host the model, textures, environment map and decoder files. Do not hotlink a tool's result URL or a CDN preset.

## 5. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Always-on loop | The fan spins on a static product page | Render on demand |
| Missing decoder | A compressed model fails to load | Set the Meshopt, Draco or KTX2 decoder |
| CDN presets in production | The environment map loads from a third-party CDN | Self-host the HDR file |
| Allocation per frame | Stutter every few seconds | Reuse objects; mutate refs |
| Unbounded pixel ratio | A phone renders at 3x and drops frames | Cap at 1 to 2; adapt under load |
| Canvas shifts layout | The page jumps when the model loads | Fixed container; poster first |
| Unpinned library | A minor upgrade breaks the scene | Pin the exact version |
