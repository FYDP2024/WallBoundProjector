import React, { useState, useEffect } from "react";
import CanvasImage from "./CanvasImage";



const Canvas = React.forwardRef(({images},ref) => {

    

    return (
        <div className="canvas" ref={ref}>
            
            <div className="reference_point">
                +
            </div>

            {
                images.map((img, index)=>(
                   <CanvasImage key={index} dimensions={img} /> 
                   
                ))
            }
            

        </div>
    );
});

export default Canvas;