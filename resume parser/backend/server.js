const express = require("express");
const multer = require("multer");
const cors = require("cors");
const { exec } = require("child_process");

const app = express();

// Enable CORS
app.use(cors());

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, "../uploads/");
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + "-" + file.originalname);
    }
});

const upload = multer({ storage: storage });

// ----------------------------
// Test Route
// ----------------------------
app.get("/", (req, res) => {
    res.send("Backend is working 🚀");
});

// ----------------------------
// Upload + Parse Route
// ----------------------------
app.post("/upload", upload.single("resume"), (req, res) => {
    if (!req.file) {
        return res.json({ error: "No file uploaded" });
    }

    const filePath = req.file.path;
    console.log("File received:", filePath);

    exec(`python parser.py "${filePath}"`, (error, stdout, stderr) => {
        console.log("STDOUT:", stdout);
        console.log("STDERR:", stderr);

        if (error) {
            console.error("Exec error:", error);
            return res.json({ error: "Parsing failed" });
        }

        try {
            const result = JSON.parse(stdout);
            res.json(result);
        } catch (parseError) {
            console.error("JSON Parse Error:", parseError);
            res.json({ error: "Invalid parser output" });
        }
    });
});
app.post("/upload-bulk", upload.array("resumes"), (req, res) => {

    const files = req.files;

    const results = [];
    let completed = 0;

    files.forEach((file, index) => {

        exec(`python parser.py "${file.path}"`, (error, stdout) => {

            if(error){
                results[index] = { error: true };
            } else {
                try{
                    results[index] = JSON.parse(stdout);
                } catch {
                    results[index] = { error: true };
                }
            }

            completed++;

            if(completed === files.length){
                res.json(results);
            }
        });

    });
});
// ----------------------------
// Start Server
// ----------------------------
app.listen(5000, () => {
    console.log("Server running on port 5000");
});