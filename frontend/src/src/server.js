const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const cors = require("cors");

const app = express();
const port = 3001;
app.use(cors());

const storage = multer.diskStorage({
  destination: path.join(__dirname, "../public/imgs"),
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  },
});

const upload = multer({ storage });

app.use(express.static(path.join(__dirname, "../public")));

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
      console.log("Images:", imageNames);
      res.json({ images: imageNames });
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
