import React, { useState, useEffect } from "react";
import CanvasImage from "./CanvasImage";

const Canvas = React.forwardRef(({ images, onImageUpdate }, ref) => {
  // actual wall dimensions are 400 cm by 400 cm
  // canvas is 440 px by 440 px
  // assumes that the wall dimension : canvas size has the same width/height scaling factor
  const scaleFactor = 440 / 400;

  return (
    <div className="canvas" ref={ref}>
      {images.map((img, index) => (
        <CanvasImage
          key={index}
          dimensions={img}
          scaleFactor={scaleFactor}
          onImageUpdate={(image) => onImageUpdate(image)}
        />
      ))}
    </div>
  );
});

export default Canvas;
