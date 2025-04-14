const functions = require('firebase-functions');
const { spawn } = require('child_process');

// Create and deploy function that runs the FastAPI server
exports.api = functions.https.onRequest((req, res) => {
  // Spawn Python process
  const process = spawn('python', ['main.py'], {
    cwd: __dirname,
    env: { ...process.env, TESTING: 'false' }
  });

  let dataString = '';

  process.stdout.on('data', (data) => {
    dataString += data.toString();
  });

  process.stderr.on('data', (data) => {
    console.error(`Error: ${data}`);
  });

  process.on('close', (code) => {
    if (code !== 0) {
      res.status(500).send('Server Error');
      return;
    }
    res.status(200).send(dataString);
  });
}); 