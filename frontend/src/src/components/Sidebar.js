import React, { useState, useEffect } from "react";

const Sidebar = ({images}) => {

    return (
        <div className="sidebar">
            <h3>Images</h3>
            {
                images.map((img,index) =>(
                    <div className="image-preview" key={index}>
                        <h3>{index+1}.</h3>
                        <div className="prev-row">
                        <img className="thumbnail" src={img.url} alt={index}/>
                        <div>
                        <p><b>Name: </b>{img.url}</p>
                        <p><b>x position:</b> {img.x_pos}</p>
                        <p><b>y position:</b> {img.y_pos}</p>
                        <p><b>Width:</b> {img.width} cm</p>
                        <p><b>Height:</b> {img.height} cm</p>
                        </div>
                        </div>
                        
                    </div>

                ))
            }

        </div>
    );
};

export default Sidebar;