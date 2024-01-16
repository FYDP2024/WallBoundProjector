import './App.css';
import Canvas from './components/Canvas';
import Sidebar from './components/Sidebar';
import Stats from './components/Stats';
import React, { useState, useRef } from 'react';
import AddImageModal from './components/AddImageModal';

import { exportComponentAsPNG } from "react-component-export-image";

function App() {
  const [imageDimensions, setImageDimensions] = useState({
    "terraria.png": {width: 160, height: 200},
    "poster.png": {width: 140, height: 200}
  })
  const [currentImages, setCurrentImages] = useState([
    {url: "imgs/terraria.png", width: 160, height: 200, x_pos: 200, y_pos: 80},
    {url: "imgs/poster.png", width: 140, height: 200, x_pos: 50, y_pos: 150},
  ])
  const [showModal, setShowModal] = useState(false);
  const handleShow = () => setShowModal(true);
  const handleClose = () => {setShowModal(false)};
  const addImageDimensions = (name, w, h) => {
    setImageDimensions({...imageDimensions, [name]: { width: Number(w), height: Number(h) }});
    let images = currentImages
    images.push({url: "imgs/" + name, width: w, height: h, x_pos: 0, y_pos: 0})
    setCurrentImages(images)
  }

const componentRef = useRef();
console.log(imageDimensions)

  return (
    <div className="app">
      <div className="left-column">
        <div className="scrollable-div">
          <Sidebar images={currentImages}/>
        </div>
      </div>
      <div className="middle-column">
        <h3>Canvas</h3>
          <div>
          <button onClick={() => handleShow()}>
          Add Image
          </button>
          <button onClick={() => exportComponentAsPNG(componentRef)}>
          Export As PNG
          </button>
        </div>
        <div>
        <AddImageModal showModal={showModal} handleClose={handleClose} onDone={(name, w, h) => addImageDimensions(name, w, h)}/>
        </div>
          <Canvas images={currentImages} ref={componentRef}/>
      </div>
      <div className="right-column">
        <div className="scrollable-div">
        <Stats />
        </div>
      </div>
    </div>
  );
}

export default App;
