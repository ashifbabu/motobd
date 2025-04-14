const functions = require('firebase-functions');
const admin = require('firebase-admin');
const { spawn } = require('child_process');

// Initialize Firebase Admin with credentials
admin.initializeApp({
  credential: admin.credential.applicationDefault()
});

// Create and deploy function that runs the FastAPI server
exports.api = functions.https.onRequest((req, res) => {
  // Set up environment variables for Python process
  const envVars = {
    ...process.env,
    TESTING: 'false',
    GOOGLE_APPLICATION_CREDENTIALS: process.env.GOOGLE_APPLICATION_CREDENTIALS
  };

  // Spawn Python process
  const process = spawn('python', ['main.py'], {
    cwd: __dirname,
    env: envVars
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