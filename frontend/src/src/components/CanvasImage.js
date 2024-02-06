import React from "react";
import Draggable from "react-draggable";

const CanvasImage = ({ dimensions, scaleFactor, onImageUpdate }) => {
  const handleDrag = (e, data) => {
    const newXPos = data.x / scaleFactor;
    const newYPos = data.y / scaleFactor;
    onImageUpdate({
      ...dimensions,
      x_pos: Math.floor(newXPos),
      y_pos: Math.floor(newYPos),
    });
  };

  return (
    <Draggable
      onStop={handleDrag}
      bounds="parent"
      position={{
        x: dimensions.x_pos * scaleFactor,
        y: dimensions.y_pos * scaleFactor,
      }}
    >
      <div
        className="canvas-image"
        // assumses x_pos and y_pos are in cm
        style={{
          position: "abosolute",
          left: 0,
          top: 0,
          width: `${dimensions.width * scaleFactor}px`,
          height: `${dimensions.height * scaleFactor}px`,
          backgroundImage: `url("imgs/${dimensions.url}")`,
        }}
      ></div>
    </Draggable>
  );
};

export default CanvasImage;
