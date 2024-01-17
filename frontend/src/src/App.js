import "./App.css";
import Canvas from "./components/Canvas";
import Sidebar from "./components/Sidebar";
import Stats from "./components/Stats";
import React, { useState, useRef } from "react";
import AddImageModal from "./components/AddImageModal";

import { exportComponentAsPNG } from "react-component-export-image";

function App() {
  const [imageDimensions, setImageDimensions] = useState({
    "terraria.png": { width: 160, height: 200 },
    "poster.png": { width: 140, height: 200 },
  });
  const [currentImages, setCurrentImages] = useState([
    { url: "terraria.png", width: 160, height: 200, x_pos: 200, y_pos: 80 },
    { url: "poster.png", width: 140, height: 200, x_pos: 50, y_pos: 150 },
  ]);
  const [showModal, setShowModal] = useState(false);

  const handleShow = () => setShowModal(true);

  const handleClose = () => setShowModal(false);

  const newImageUploaded = (name, w, h) => {
    setImageDimensions({
      ...imageDimensions,
      [name]: { width: Number(w), height: Number(h) },
    });
    const images = currentImages;
    images.push({ url: name, width: w, height: h, x_pos: 0, y_pos: 0 });
    setCurrentImages(images);
    setShowModal(false);
  };

  const previousImageAdded = (name) => {
    const imageToAdd = imageDimensions[name];
    const images = currentImages;
    images.push({
      url: name,
      width: imageToAdd.width,
      height: imageToAdd.height,
      x_pos: 0,
      y_pos: 0,
    });
    setCurrentImages(images);
    setShowModal(false);
  };

  const deleteCurrentImage = (name) => {
    const images = currentImages;
    const updatedImages = images.filter((image) => image.url !== name);
    setCurrentImages(updatedImages);
  };

  const componentRef = useRef();

  return (
    <div className="app">
      <div className="left-column">
        <div className="scrollable-div">
          <Sidebar
            images={currentImages}
            deleteCurrentImage={(name) => deleteCurrentImage(name)}
          />
        </div>
      </div>
      <div className="middle-column">
        <h3>Canvas</h3>
        <div>
          <button onClick={() => handleShow()}>Add Image</button>
          <button onClick={() => exportComponentAsPNG(componentRef)}>
            Export As PNG
          </button>
        </div>
        <div>
          <AddImageModal
            showModal={showModal}
            handleClose={handleClose}
            newImageUploaded={(name, w, h) => newImageUploaded(name, w, h)}
            previousImageAdded={(name) => previousImageAdded(name)}
            currentImages={currentImages}
          />
        </div>
        <div className="canvas-container">
          <Canvas images={currentImages} ref={componentRef} />
        </div>
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
