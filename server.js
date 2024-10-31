// server.js
const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.post('/analyze', (req, res) => {
    const url = req.body.url;

    // Spawn a Python process to run the sentiment analysis
    const pythonProcess = spawn('python', ['sentiment_analysis.py', url]);

    let result = '';

    pythonProcess.stdout.on('data', (data) => {
        result += data.toString();
        console.log(result);
    });

    pythonProcess.stderr.on('data', (data) => {
            console.error(`Error: ${data}`);
        });
    
        pythonProcess.on('close', (code) => {
                if (code === 0) {
            try {
                const analysis = JSON.parse(result); // Parse the Python output
                console.log(analysis);
                res.json(analysis);
            } catch (error) {
                    res.status(500).json({ error: 'Error parsing analysis result' });
            }
        } else {
                res.status(500).json({ error: 'Python script execution failed' });
            }
        });
    });
   
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port http://localhost:${PORT}`));
