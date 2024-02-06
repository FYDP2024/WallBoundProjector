import React from "react";
import { Button } from "react-bootstrap";

const Stats = ({ drafts, loadImagesFromDraft }) => {
  const distance = 10;
  const tilt = [4, 6, 8];
  const getNumber = (fileName) => {
    const underscoreIndex = fileName.indexOf("_");
    const dotIndex = fileName.indexOf(".");
    return fileName.substring(underscoreIndex + 1, dotIndex);
  };
  return (
    <div className="stats-container">
      <div>
        <h4>Info</h4>
        <div>Distance: {distance}cm</div>
        <div>Roll (x): {tilt[0]}°</div>
        <div>Roll (y): {tilt[1]}°</div>
        <div>Roll (z): {tilt[2]}°</div>
      </div>
      <div className="stats-drafts">
        <h4>Drafts</h4>
        <div>
          {drafts.map((draft) => (
            <>
              <div className="image-preview">
                <div className="prev-row">
                  <img className="thumbnail" src={"drafts/" + draft.image} />
                </div>
              </div>
              <Button
                type="button"
                variant="secondary"
                onClick={() => loadImagesFromDraft(draft.draft)}
              >
                {"Draft " + getNumber(draft.draft)}
              </Button>
            </>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Stats;
