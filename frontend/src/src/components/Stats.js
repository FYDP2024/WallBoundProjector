import React from "react";

const Stats = ({ drafts, loadImagesFromDraft }) => {
  const distance = 10;
  const tilt = [4, 6, 8];
  console.log(drafts);
  return (
    <div>
      <h3>Info</h3>
      <div>Distance: {distance}cm</div>
      <div>Roll (x): {tilt[0]}°</div>
      <div>Roll (y): {tilt[1]}°</div>
      <div>Roll (z): {tilt[2]}°</div>
      <h3>Drafts</h3>
      <div>
        {drafts.map((draft) => (
          <>
            <button onClick={() => loadImagesFromDraft(draft.draft)}>
              {draft.draft.slice(0, -5)}
            </button>
            <div className="image-preview">
              <div className="prev-row">
                <img className="thumbnail" src={"drafts/" + draft.image} />
              </div>
            </div>
          </>
        ))}
      </div>
    </div>
  );
};

export default Stats;
