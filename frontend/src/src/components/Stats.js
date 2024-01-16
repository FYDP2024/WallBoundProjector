import React, { useState, useEffect } from "react";

const Stats = ({}) => {

    const distance = 10;
    const tilt = [4,6,8];

    return (
        <div className="sidebar">
            <h3>Info</h3>
            <div>Distance: {distance}cm</div>
            <div>Roll (x): {tilt[0]}°</div>
            <div>Roll (y): {tilt[1]}°</div>
            <div>Roll (z): {tilt[2]}°</div>
        </div>
    );
};

export default Stats;