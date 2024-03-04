import React, { useEffect, useState } from "react";
import { Button, CloseButton, Form } from "react-bootstrap";

const Sidebar = ({ images, deleteCurrentImage, handleEditAndSave }) => {
  const [editedImages, setEditedImages] = useState([]);

  useEffect(() => {
    setEditedImages(images);
  }, [images]);

  const onChange = (image) => {
    setEditedImages((prevImages) =>
      prevImages.map((i) => (i.url === image.url ? image : i))
    );
  };

  const onChangeWidth = (img, value) => {
    let image = img;
    if (image.lockRatio) {
      image.height = Math.round(
        value * (image.ratio.height / image.ratio.width)
      );
    }
    image.width = value;
    setEditedImages((prevImages) =>
      prevImages.map((i) => (i.url === image.url ? image : i))
    );
  };

  const onChangeHeight = (img, value) => {
    let image = img;
    if (image.lockRatio) {
      image.width = Math.round(
        value * (image.ratio.width / image.ratio.height)
      );
    }
    image.height = value;
    setEditedImages((prevImages) =>
      prevImages.map((i) => (i.url === image.url ? image : i))
    );
  };

  const onChangeLockRatio = (img) => {
    let image = img;
    // we are locking
    if (!image.lockRatio) {
      // both fields are specified or width is specified
      if ((image.width !== "" && image.height !== "") || image.width !== "") {
        image.height = Math.round(
          image.width * (image.ratio.height / image.ratio.width)
        );
        // height is specified
      } else if (image.height !== "") {
        image.width = Math.round(
          image.height * (image.ratio.width / image.ratio.height)
        );
      }
    }
    image.lockRatio = !image.lockRatio;
    setEditedImages((prevImages) =>
      prevImages.map((i) => (i.url === image.url ? image : i))
    );
  };

  return (
    <div className="sidebar-container">
      <h4>Images</h4>
      {editedImages.map((img, index) => (
        <div className="image-preview" key={index}>
          <div className="preview-top">
            <h4>{index + 1}.</h4>
            <CloseButton
              onClick={() => deleteCurrentImage(img.url)}
              className="close-button"
            />
          </div>
          <div className="preview-middle">
            <img className="thumbnail" src={"imgs/" + img.url} alt={index} />
            <div>
              <div>Name: {img.url}</div>
              {img.isEdit && (
                <>
                  <div>
                    x position:
                    <input
                      type="number"
                      name="x_pos"
                      value={img.x_pos}
                      onChange={(e) =>
                        onChange({ ...img, x_pos: e.target.value })
                      }
                    />
                  </div>
                  <div>
                    y position:
                    <input
                      type="number"
                      name="y_pos"
                      value={img.y_pos}
                      onChange={(e) =>
                        onChange({ ...img, y_pos: e.target.value })
                      }
                    />
                  </div>
                  <div>
                    Width:
                    <input
                      type="number"
                      name="width"
                      value={img.width}
                      onChange={(e) => onChangeWidth(img, e.target.value)}
                    />
                  </div>
                  <div>
                    Height:
                    <input
                      type="number"
                      name="height"
                      value={img.height}
                      onChange={(e) => onChangeHeight(img, e.target.value)}
                    />
                  </div>
                  <Form.Group controlId="formLockAspectRatio" className="mb-3">
                    <Form.Check
                      type="checkbox"
                      label="Lock Aspect Ratio"
                      checked={img.lockRatio}
                      onChange={() => onChangeLockRatio(img)}
                      className="custom-checkbox"
                    />
                  </Form.Group>
                </>
              )}
              {!img.isEdit && (
                <>
                  <div>x position: {img.x_pos}</div>
                  <div>y position: {img.y_pos}</div>
                  <div>Width: {img.width} cm</div>
                  <div>Height: {img.height} cm</div>
                </>
              )}
            </div>
          </div>
          <div className="edit-image-btn">
            <Button
              type="button"
              variant="secondary"
              onClick={() => handleEditAndSave(img)}
            >
              {img.isEdit ? "Save" : "Edit"}
            </Button>
          </div>
        </div>
      ))}
    </div>
  );
};
export default Sidebar;
