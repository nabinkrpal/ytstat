// server.js
const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
function isValidYouTubeUrl(url) {
    const ytRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[a-zA-Z0-9_-]{11}$/;
    return ytRegex.test(url);
}

app.post('/analyze', (req, res) => {
    const url = req.body.url;

    // Check if the URL is a valid YouTube video URL
    if (!isValidYouTubeUrl(url)) {
        return res.status(400).json({ error: 'Invalid YouTube URL' });
    }

    // Spawn Python process if URL is valid
    const pythonProcess = spawn('python3', ['sentiment_analysis.py', url]);

    pythonProcess.stdout.on('data', (data) => {
        const result = data.toString();
        res.json({ result });
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code ${code}`);
    });
});

// app.post('/analyze', (req, res) => {
//     const url = req.body.url;

//     // Spawn a Python process to run the sentiment analysis
//     const pythonProcess = spawn('python', ['sentiment_analysis.py', url]);

//     let result = '';

//     pythonProcess.stdout.on('data', (data) => {
//         result += data.toString();
//         console.log(result);
//     });

//     pythonProcess.stderr.on('data', (data) => {
//         console.error(`Error: ${data}`);
//     });

//     pythonProcess.on('close', (code) => {
//         if (code === 0) {
//             try {
//                 const analysis = JSON.parse(result); // Parse the Python output
//                 console.log(analysis);
//                 res.json(analysis);
//             } catch (error) {
//                 res.status(500).json({ error: 'Error parsing analysis result' });
//             }
//         } else {
//             res.status(500).json({ error: 'Python script execution failed' });
//         }
//     });
// });

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port http://localhost:${PORT}`));


