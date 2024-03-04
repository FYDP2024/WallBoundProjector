import React, { useState, useEffect } from "react";
import CanvasImage from "./CanvasImage";

const Canvas = React.forwardRef(({ images, onImageUpdate }, ref) => {
  // actual wall dimensions are 250 cm by 250 cm
  // canvas is 700 px by 700 px
  // assumes that the wall dimension : canvas size has the same width/height scaling factor
  const scaleFactor = 700 / 250;

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
