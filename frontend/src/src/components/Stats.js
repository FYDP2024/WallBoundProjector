import React, { useState, useEffect } from "react";

const Stats = ({}) => {

    const distance = 10;
    const tilt = [4,6,8];

    return (
        <div className="sidebar">
            <h1>Info</h1>
            <h2>Distance: {distance}cm</h2>
            <h2>Roll (x): {tilt[0]}°</h2>
            <h2>Roll (y): {tilt[1]}°</h2>
            <h2>Roll (z): {tilt[2]}°</h2>

            

        </div>
    );
};

export default Stats;