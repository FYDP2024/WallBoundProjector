import React from "react";

const Sidebar = ({ images, deleteCurrentImage }) => {
  return (
    <div>
      <h3>Images</h3>
      {images.map((img, index) => (
        <div className="image-preview" key={index}>
          <button onClick={() => deleteCurrentImage(img.url)}>X</button>
          <h3>{index + 1}.</h3>
          <div className="prev-row">
            <img className="thumbnail" src={"imgs/" + img.url} alt={index} />
            <div>
              <div>
                <b>Name: </b>
                {img.url}
              </div>
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
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
export default Sidebar;
