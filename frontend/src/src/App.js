import React, { useState, useRef, useEffect } from "react";
import { Button } from "react-bootstrap";
import html2canvas from "html2canvas";
import Canvas from "./components/Canvas";
import Sidebar from "./components/Sidebar";
import Stats from "./components/Stats";
import AddImageModal from "./components/AddImageModal";
import "./App.scss";

function App() {
  const [imageDimensions, setImageDimensions] = useState({});
  const [currentImages, setCurrentImages] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [drafts, setDrafts] = useState([]);

  useEffect(() => {
    fetch("http://localhost:3001/clear", { method: "GET" });
  }, []);

  const handleShow = () => setShowModal(true);

  const handleClose = () => setShowModal(false);

  // onEdit/onSave
  const handleEditAndSave = (image) => {
    if (image.isEdit === false) {
      setCurrentImages((prevImages) =>
        prevImages.map((i) =>
          i.url === image.url ? { ...image, isEdit: true } : i
        )
      );
    } else {
      let updatedImage = { ...image, isEdit: false };
      setCurrentImages((prevImages) =>
        prevImages.map((i) => (i.url === updatedImage.url ? updatedImage : i))
      );
    }
  };

  // update an image
  const onImageUpdate = (image) => {
    setCurrentImages((prevImages) =>
      prevImages.map((i) => (i.url === image.url ? image : i))
    );
  };

  // add image modal - uploaded a new image
  const newImageUploaded = (name, w, h) => {
    setImageDimensions({
      ...imageDimensions,
      [name]: { width: Number(w), height: Number(h) },
    });
    const images = currentImages;
    images.push({
      url: name,
      isEdit: false,
      width: w,
      height: h,
      x_pos: 0,
      y_pos: 0,
    });
    setCurrentImages(images);
    setShowModal(false);
  };

  // add image modal - selected from previously uploaded images
  const previousImageAdded = (name) => {
    const imageToAdd = imageDimensions[name];
    const images = currentImages;
    images.push({
      url: name,
      isEdit: false,
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
    <div className="app-container">
      <div>
        <AddImageModal
          showModal={showModal}
          handleClose={handleClose}
          newImageUploaded={(name, w, h) => newImageUploaded(name, w, h)}
          previousImageAdded={(name) => previousImageAdded(name)}
          currentImages={currentImages}
        />
      </div>
      <div className="left-column">
        <div className="scrollable-div">
          <Sidebar
            images={currentImages}
            deleteCurrentImage={(name) => deleteCurrentImage(name)}
            handleEditAndSave={(image) => {
              handleEditAndSave(image);
            }}
          />
        </div>
      </div>
      <div className="middle-column">
        <h4>Canvas</h4>
        <div>
          <Button
            className="add-image-btn"
            type="button"
            variant="secondary"
            onClick={() => handleShow()}
          >
            Add Image
          </Button>
          <Button type="button" variant="secondary" onClick={() => saveDraft()}>
            Save
          </Button>
        </div>
        <div className="canvas-container">
          <Canvas
            images={currentImages}
            onImageUpdate={(image) => onImageUpdate(image)}
            ref={componentRef}
          />
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
