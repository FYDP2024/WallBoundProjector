const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const cors = require("cors");

const app = express();
const port = 3001;
app.use(cors());
app.use(express.json({ limit: "10mb" }));
app.use(express.urlencoded({ extended: true, limit: "10mb" }));

const storage = multer.diskStorage({
  destination: path.join(__dirname, "../public/imgs"),
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  },
});
const upload = multer({ storage });
const draftsDir = path.join(__dirname, "../public/drafts");

app.post("/upload", upload.single("image"), (req, res) => {
  res.json({ message: "Image uploaded successfully" });
});

app.get("/getImages", (req, res) => {
  const imgDir = path.join(__dirname, "../public/imgs");
  fs.readdir(imgDir, (err, files) => {
    if (err) {
      console.error("Error reading images directory", err);
      res.status(500).json({ error: "Internal Server Error" });
    } else {
      const imageNames = files.filter(
        (file) =>
          file.endsWith(".jpg") ||
          file.endsWith(".jpeg") ||
          file.endsWith(".png")
      );
      res.json({ images: imageNames });
    }
  });
});

const getDraftFiles = () => {
  return fs
    .readdirSync(draftsDir)
    .filter((file) => file.endsWith(".json"))
    .sort();
};

const getNextDraftFileName = () => {
  const draftFiles = getDraftFiles();
  const lastFile = draftFiles[draftFiles.length - 1];
  if (!lastFile) {
    return "Draft_1.json";
  }
  const lastNumber = parseInt(lastFile.match(/\d+/)[0]);
  const nextNumber = lastNumber + 1;
  return `Draft_${nextNumber}.json`;
};

app.post("/saveDraft", (req, res) => {
  const { images } = req.body;
  const nextFileName = getNextDraftFileName();
  const jsonString = JSON.stringify(images, null, 2);
  fs.writeFile(path.join(draftsDir, nextFileName), jsonString, (err) => {
    if (err) {
      res.status(500).json({ error: "Internal Server Error" });
    } else {
      res.json({ message: "Draft saved successfully", fileName: nextFileName });
    }
  });
});

app.get("/getDrafts", (req, res) => {
  const draftFiles = getDraftFiles();
  const draftImages = getDraftImageFiles();
  if (draftFiles.length === draftFiles.length) {
    const result = draftFiles.map((draft, index) => ({
      draft: draft,
      image: draftImages[index],
    }));
    res.json({ drafts: result });
  } else {
    res.json({});
  }
});

app.get("/getDraft/:fileName", (req, res) => {
  const { fileName } = req.params;
  const filePath = path.join(draftsDir, fileName);
  const data = fs.readFileSync(filePath, "utf-8");
  const images = JSON.parse(data);
  res.json({ images });
});

app.post("/saveCanvasImage", (req, res) => {
  const { imageData } = req.body;
  const nextFileName = getNextDraftImageFileName();
  const filePath = path.join(draftsDir, nextFileName);
  try {
    const buffer = Buffer.from(imageData.split(",")[1], "base64");
    fs.writeFileSync(filePath, buffer);
    res.json({
      message: "Canvas image saved successfully",
      fileName: nextFileName,
    });
  } catch (error) {
    res.status(500).json({ error: "Internal Server Error" });
  }
});

const getNextDraftImageFileName = () => {
  const draftFiles = getDraftImageFiles();
  const lastFile = draftFiles[draftFiles.length - 1];
  if (!lastFile) {
    return "Draft_1.png";
  }
  const lastNumber = parseInt(lastFile.match(/\d+/)[0]);
  const nextNumber = lastNumber + 1;
  return `Draft_${nextNumber}.png`;
};

const getDraftImageFiles = () => {
  return fs
    .readdirSync(draftsDir)
    .filter((file) => file.endsWith(".png"))
    .sort();
};

app.listen(port, () => {});
