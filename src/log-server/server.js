const express = require('express');
const cors = require('cors');
const Docker = require('dockerode');
const app = express();

app.use(cors()); // Enable CORS

const docker = new Docker({ socketPath: '/var/run/docker.sock' });

app.get('/logs', async (req, res) => {
    try {
        const container = docker.getContainer('clocktower-visualizer');
        const logsStream = await container.logs({
            follow: true,
            stdout: true,
            stderr: true,
            tail: 0
        });

        res.setHeader('Content-Type', 'text/event-stream');
        res.setHeader('Cache-Control', 'no-cache');
        res.setHeader('Connection', 'keep-alive');
        res.flushHeaders();

        logsStream.on('data', (chunk) => {
            // Decode the Docker log stream
            console.log('here');
            for (let i = 0; i < chunk.length; ) {
                const header = chunk.slice(i, i + 8); // Extract the 8-byte header
                const type = header.readUInt8(0); // First byte indicates stream type
                const length = header.readUInt32BE(4); // Next 4 bytes indicate message length

                // Extract the actual log message
                const message = chunk.slice(i + 8, i + 8 + length).toString('utf8');

                // Send the decoded log message to the client
                res.write(`data: ${message}\n\n`);

                i += 8 + length; // Move to the next log entry
            }
        });

        logsStream.on('end', () => res.end());
        req.on('close', () => logsStream.destroy());
    } catch (error) {
        res.status(500).send(error.message);
    }
});

const PORT = 3000;
app.listen(PORT, () => console.log(`Log server running on port ${PORT}`));