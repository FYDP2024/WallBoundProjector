import React, { useState, useEffect } from "react";
import CanvasImage from "./CanvasImage";

const Canvas = React.forwardRef(({ images }, ref) => {
  // actual wall dimensions are 400 cm by 400 cm
  // canvas is 450 px by 450 px
  // assumes that the wall dimension : canvas size has the same width/height scaling factor
  const scaleFactor = 450 / 400;

  return (
    <div className="canvas" ref={ref}>
      {images.map((img, index) => (
        <CanvasImage key={index} dimensions={img} scaleFactor={scaleFactor} />
      ))}
    </div>
  );
});

export default Canvas;
