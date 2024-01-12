import logo from './logo.svg';
import { useRef } from 'react';
import './App.css';
import Canvas from './components/Canvas';
import Sidebar from './components/Sidebar';
import Stats from './components/Stats';

import {
  exportComponentAsJPEG,
  exportComponentAsPDF,
  exportComponentAsPNG
} from "react-component-export-image";

function App() {


  const images = [
    {
        url: "imgs/sample_img.png",
        width: 100,
        height: 100,
        x_pos: 300,
        y_pos: 300
    },
    {
        url: "imgs/terraria.png",
        width: 160,
        height: 200,
        x_pos: 200,
        y_pos: 80
    },
    {
      url: "imgs/poster.png",
      width: 140,
      height: 200,
      x_pos: 100,
      y_pos: 300
  },
]

const componentRef = useRef();

  return (
    <div className="App">
      <Sidebar images={images}/>
      <div className='workspace'>
        <h1>Canvas</h1>
        <button onClick={() => exportComponentAsPNG(componentRef)}>
        Export As PNG
        </button>
        <Canvas images={images} ref={componentRef}/>
      </div>
      <Stats />
      
    </div>
  );
}

export default App;
