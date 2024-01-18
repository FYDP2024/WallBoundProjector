import React, { useState, useRef } from "react";
import { exportComponentAsPNG } from "react-component-export-image";
import html2canvas from "html2canvas";
import Canvas from "./components/Canvas";
import Sidebar from "./components/Sidebar";
import Stats from "./components/Stats";
import AddImageModal from "./components/AddImageModal";
import "./App.css";

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
  const [drafts, setDrafts] = useState([]);

  const handleShow = () => setShowModal(true);

  const handleClose = () => setShowModal(false);

  // add image modal - uploaded a new image
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

  // add image modal - selected from previously uploaded images
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

  // delete an image from the canvas
  const deleteCurrentImage = (name) => {
    const images = currentImages;
    const updatedImages = images.filter((image) => image.url !== name);
    setCurrentImages(updatedImages);
  };

  // save the current canvas as a draft
  const saveDraft = async () => {
    // save json
    await fetch("http://localhost:3001/saveDraft", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ images: currentImages }),
    });
    // save png
    const canvas = await html2canvas(componentRef.current, {
      scale: 5,
    });
    const imageData = canvas.toDataURL("image/jpeg");
    await fetch(`http://localhost:3001/saveCanvasImage`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ imageData }),
    });
    // get a new list of the drafts
    const getJson = await fetch("http://localhost:3001/getDrafts");
    const jsonData = await getJson.json();
    setDrafts(jsonData.drafts);
  };

  // load a previous draft
  const loadImagesFromDraft = async (fileName) => {
    const response = await fetch(`http://localhost:3001/getDraft/${fileName}`);
    const data = await response.json();
    setCurrentImages(data.images);
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
          <button onClick={() => saveDraft()}>Save</button>
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
          <Stats
            drafts={drafts}
            loadImagesFromDraft={(draft) => loadImagesFromDraft(draft)}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
