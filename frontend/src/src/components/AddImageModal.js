import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, ListGroup, Tabs, Tab } from 'react-bootstrap';

const AddImageModal = ({ showModal, handleClose, onDone }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedFileName, setUploadedFileName] = useState('')
  const [uploadedImages, setUploadedImages] = useState([]);
  const [width, setWidth] = useState('');
  const [height, setHeight] = useState('');
  const [selectedImage, setSelectedImage] = useState('');

  useEffect(() => {
    setSelectedFile(null)
    setUploadedFileName('')
    setSelectedImage('')
    setWidth('')
    setHeight('')
    fetch('http://localhost:3001/getImages')
      .then((response) => response.json())
      .then((data) => {
        setUploadedImages(data.images);
      })
  }, [showModal]);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleWidthChange = (e) => {
    setWidth(e.target.value);
  };

  const handleHeightChange = (e) => {
    setHeight(e.target.value);
  };

  const handleUpload = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append('image', selectedFile);
      const response = await fetch('http://localhost:3001/upload', {
        method: 'POST',
        body: formData,
      });
      setUploadedFileName(selectedFile.name);
    }
  };

  return (
    <Modal show={showModal} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Add Image</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Tabs defaultActiveKey="upload" id="image-upload-tabs">
          <Tab eventKey="upload" title="Upload New Image">
          <div style={{ marginTop: '40px' }}>
            <Form>
              <Form.Group controlId="formFile" className="mb-3">
                <Form.Label>Choose an image file (.jpg/.jpeg/.png):</Form.Label>
                <Form.Control type="file" onChange={handleFileChange} />
                {uploadedFileName && (
                  <p>Uploaded file: {uploadedFileName}</p>
                )}
                <Button variant="primary" onClick={handleUpload} className="mt-2">
                  Upload
                </Button>
              </Form.Group>
              <Form.Group controlId="formWidth" className="mb-3">
                <Form.Label>Width (cm):</Form.Label>
                <Form.Control type="number" value={width} onChange={handleWidthChange} />
              </Form.Group>
              <Form.Group controlId="formHeight" className="mb-3">
                <Form.Label>Height (cm):</Form.Label>
                <Form.Control type="number" value={height} onChange={handleHeightChange} />
              </Form.Group>
            </Form>
            </div>
          </Tab>
          <Tab eventKey="previous" title="Previously Uploaded Images">
          <div style={{ marginTop: '40px' }}>
            <ListGroup>
                  {uploadedImages.map((imageName, index) => (
                    <ListGroup.Item key={index}>
                      <Form.Check
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
        <Button variant="secondary" onClick={()=>{handleClose(); onDone(uploadedFileName, width, height)}}>
          Done
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default AddImageModal;
