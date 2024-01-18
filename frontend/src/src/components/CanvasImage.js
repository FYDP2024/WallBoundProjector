import React from "react";

const CanvasImage = ({ dimensions, scaleFactor }) => {
  return (
    <div
      className="canvas-image"
      // assumses x_pos and y_pos are in cm
      style={{
        position: "abosolute",
        left: `${dimensions.x_pos * scaleFactor}px`,
        top: `${dimensions.y_pos * scaleFactor}px`,
        width: `${dimensions.width * scaleFactor}px`,
        height: `${dimensions.height * scaleFactor}px`,
        backgroundImage: `url("imgs/${dimensions.url}")`,
      }}
    ></div>
  );
};

export default CanvasImage;
