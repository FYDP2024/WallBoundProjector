import React, { useEffect, useState } from "react";

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

  return (
    <div>
      <h3>Images</h3>
      {editedImages.map((img, index) => (
        <div className="image-preview" key={index}>
          <button onClick={() => deleteCurrentImage(img.url)}>X</button>
          <button onClick={() => handleEditAndSave(img)}>
            {img.isEdit ? "Save" : "Edit"}
          </button>
          <h3>{index + 1}.</h3>
          <div className="prev-row">
            <img className="thumbnail" src={"imgs/" + img.url} alt={index} />
            <div>
              <div>
                <b>Name: </b>
                {img.url}
              </div>
              {img.isEdit && (
                <>
                  <div>
                    <b>x position:</b>
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
                    <b>y position:</b>
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
                    <b>Width:</b>
                    <input
                      type="number"
                      name="width"
                      value={img.width}
                      onChange={(e) =>
                        onChange({ ...img, width: e.target.value })
                      }
                    />
                  </div>
                  <div>
                    <b>Height:</b>
                    <input
                      type="number"
                      name="height"
                      value={img.height}
                      onChange={(e) =>
                        onChange({ ...img, height: e.target.value })
                      }
                    />
                  </div>
                </>
              )}
              {!img.isEdit && (
                <>
                  <div>
                    <b>x position:</b> {img.x_pos}
                  </div>
                  <div>
                    <b>y position:</b> {img.y_pos}
                  </div>
                  <div>
                    <b>Width:</b> {img.width} cm
                  </div>
                  <div>
                    <b>Height:</b> {img.height} cm
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
export default Sidebar;
