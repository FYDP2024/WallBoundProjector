import React, { useState, useEffect } from "react";
import { Modal, Button, Form, ListGroup, Tabs, Tab } from "react-bootstrap";

const AddImageModal = ({
  showModal,
  handleClose,
  newImageUploaded,
  previousImageAdded,
  currentImages,
}) => {
  const [activeTab, setActiveTab] = useState("upload");
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedFile, setuploadedFile] = useState("");
  const [width, setWidth] = useState("");
  const [height, setHeight] = useState("");
  const [lockRatio, setLockRatio] = useState(false);
  const [ratio, setRatio] = useState({ width: 0, height: 0 });
  const [previousUploadedImages, setPreviousUploadedImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState("");

  useEffect(() => {
    setActiveTab("upload");
    setSelectedFile(null);
    setuploadedFile("");
    setSelectedImage("");
    setWidth("");
    setHeight("");
    setLockRatio(false);
    setRatio({ width: 0, height: 0 });
    fetch("http://localhost:3001/getImages")
      .then((response) => response.json())
      .then((data) => {
        const filteredImages = data.images.filter((image) => {
          return !currentImages.some(
            (currentImage) => currentImage.url === image
          );
        });
        setPreviousUploadedImages(filteredImages);
      });
  }, [showModal]);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleWidthChange = (e) => {
    if (lockRatio) {
      setHeight(Math.round(e.target.value * (ratio.height / ratio.width)));
    }
    setWidth(e.target.value);
  };

  const handleHeightChange = (e) => {
    if (lockRatio) {
      setWidth(Math.round(e.target.value * (ratio.width / ratio.height)));
    }
    setHeight(e.target.value);
  };

  const handleTabSelect = (selectedTab) => {
    setActiveTab(selectedTab);
  };

  const handleUpload = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append("image", selectedFile);
      const response = await fetch("http://localhost:3001/upload", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setuploadedFile(data.name);
      setRatio(data.dimensions);
    }
  };

  const handleDone = () => {
    if (activeTab === "upload") {
      newImageUploaded(uploadedFile, width, height, lockRatio, ratio);
    } else if (activeTab === "previous") {
      previousImageAdded(selectedImage);
    }
  };

  const handleLockAspectRatio = () => {
    // we are locking
    if (!lockRatio) {
      // both fields are specified or width is specified
      if ((width !== "" && height !== "") || width !== "") {
        setHeight(Math.round(width * (ratio.height / ratio.width)));
        // height is specified
      } else if (height !== "") {
        setWidth(Math.round(height * (ratio.width / ratio.height)));
      }
    }
    setLockRatio(!lockRatio);
  };

  return (
    <Modal show={showModal} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Add Image</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Tabs
          activeKey={activeTab}
          onSelect={handleTabSelect}
          id="image-upload-tabs"
        >
          <Tab eventKey="upload" title="Upload New Image">
            <div style={{ marginTop: "40px" }}>
              <Form>
                <Form.Group controlId="formFile" className="mb-3">
                  <Form.Label>
                    Choose an image file (.jpg/.jpeg/.png):
                  </Form.Label>
                  <Form.Control type="file" onChange={handleFileChange} />
                  {uploadedFile && <p>Uploaded file: {uploadedFile}</p>}
                  <Button
                    type="button"
                    variant="secondary"
                    onClick={handleUpload}
                    className="mt-2"
                  >
                    Upload
                  </Button>
                </Form.Group>
                <Form.Group controlId="formWidth" className="mb-3">
                  <Form.Label>Width (cm):</Form.Label>
                  <Form.Control
                    type="number"
                    value={width}
                    onChange={handleWidthChange}
                  />
                </Form.Group>
                <Form.Group controlId="formHeight" className="mb-3">
                  <Form.Label>Height (cm):</Form.Label>
                  <Form.Control
                    type="number"
                    value={height}
                    onChange={handleHeightChange}
                  />
                </Form.Group>
                <Form.Group controlId="formLockAspectRatio" className="mb-3">
                  <Form.Check
                    type="checkbox"
                    label="Lock Aspect Ratio"
                    checked={lockRatio}
                    onChange={() => handleLockAspectRatio()}
                    className="custom-checkbox"
                  />
                </Form.Group>
              </Form>
            </div>
          </Tab>
          <Tab eventKey="previous" title="Previously Uploaded Images">
            <div style={{ marginTop: "40px" }}>
              <ListGroup>
                {previousUploadedImages.map((imageName, index) => (
                  <ListGroup.Item key={index}>
                    <Form.Check
                      className="custom-radio"
                      type="radio"
                      label={imageName}
                      name="previousImage"
                      id={`radio-${index}`}
                      value={imageName}
                      checked={selectedImage === imageName}
                      onChange={() => setSelectedImage(imageName)}
                    />
                  </ListGroup.Item>
                ))}
              </ListGroup>
            </div>
          </Tab>
        </Tabs>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={() => handleDone()}>
          Done
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default AddImageModal;
