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

const imgsDir = path.join(__dirname, "../public/imgs");
const draftsDir = path.join(__dirname, "../public/drafts");

// function to delete all files in the imgs and drafts folders
const deleteAllFiles = () => {
  fs.readdir(imgsDir, (err, files) => {
    if (err) {
      return;
    }
    files.forEach((file) => {
      const filePath = path.join(imgsDir, file);
      fs.unlinkSync(filePath);
    });
  });
  fs.readdir(draftsDir, (err, files) => {
    if (err) {
      return;
    }
    files.forEach((file) => {
      const filePath = path.join(draftsDir, file);
      fs.unlinkSync(filePath);
    });
  });
};

// determine if the image name already exists and append (1), (2), ...
const storage = multer.diskStorage({
  destination: imgsDir,
  filename: function (req, file, cb) {
    const originalname = file.originalname;
    const extension = path.extname(originalname);
    const basename = path.basename(originalname, extension);
    let fileIndex = 1;
    let newFilename = originalname;
    while (fs.existsSync(path.join(imgsDir, newFilename))) {
      newFilename = `${basename} (${fileIndex++})${extension}`;
    }
    cb(null, newFilename);
  },
});

const upload = multer({ storage: storage });

// clear all files from imgs and drafts folders
app.get("/clear", (req, res) => {
  deleteAllFiles();
  res.json({ message: "All files cleared successfully" });
});

// upload new image
app.post("/upload", upload.single("image"), (req, res) => {
  const uploadedFilename = req.file.filename;
  res.json({ name: uploadedFilename });
});

// get a list of all images previously uploaded
app.get("/getImages", (req, res) => {
  const imgDir = imgsDir;
  fs.readdir(imgDir, (err, files) => {
    if (err) {
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

// get a list of all previous json drafts
const getDraftFiles = () => {
  return fs
    .readdirSync(draftsDir)
    .filter((file) => file.endsWith(".json"))
    .sort();
};

// determine the file name for the next draft
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

// save new draft as a json file
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

// get a list of all drafts (json file and png image)
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

// get a specific json file
app.get("/getDraft/:fileName", (req, res) => {
  const { fileName } = req.params;
  const filePath = path.join(draftsDir, fileName);
  const data = fs.readFileSync(filePath, "utf-8");
  const images = JSON.parse(data);
  res.json({ images });
});

// save an image of the canvas as a draft
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

// determine the file name for the next image draft
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

// get a list of all previous image drafts
const getDraftImageFiles = () => {
  return fs
    .readdirSync(draftsDir)
    .filter((file) => file.endsWith(".png"))
    .sort();
};

app.listen(port, () => {});

deleteAllFiles();
