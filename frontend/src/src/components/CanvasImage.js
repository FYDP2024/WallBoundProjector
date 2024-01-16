import React from "react";

const CanvasImage = ({dimensions}) => {
    return (
        <div className="canvas-image"
            style={{
                        position: "abosolute",
                        left: `${dimensions.x_pos}px`,
                        top: `${dimensions.y_pos}px`,
                        width: `${dimensions.width}px`,
                        height: `${dimensions.height}px`,
                        backgroundImage: `url("${dimensions.url}")`,
                    }}>
        </div>
    );
};

export default CanvasImage;