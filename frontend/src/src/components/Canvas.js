import React, { useState, useEffect } from "react";
import CanvasImage from "./CanvasImage";


const Canvas = ({images}) => {

    

    return (
        <div className="canvas">
            
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
};

export default Canvas;