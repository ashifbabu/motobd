const functions = require('firebase-functions');
const admin = require('firebase-admin');
const { spawn } = require('child_process');
const path = require('path');

// Initialize Firebase Admin with credentials
admin.initializeApp({
  credential: admin.credential.applicationDefault()
});

// Create and deploy function that runs the Python handler
exports.api = functions.https.onRequest((req, res) => {
  console.log('Received request:', {
    method: req.method,
    path: req.path,
    query: req.query
  });

  // Set up environment variables for Python process
  const envVars = {
    ...process.env,
    TESTING: 'false',
    ENVIRONMENT: 'production',
    REQUEST_METHOD: req.method,
    PATH_INFO: req.path,
    QUERY_STRING: req.url.split('?')[1] || '',
    PYTHONPATH: __dirname
  };

  // Try to find Python executable
  const pythonPaths = [
    process.env.PYTHON_PATH,
    '/usr/bin/python3',
    '/usr/bin/python',
    'python3',
    'python'
  ].filter(Boolean);

  let pythonProcess = null;
  let pythonError = null;

  // Try each Python path until one works
  for (const pythonPath of pythonPaths) {
    try {
      pythonProcess = spawn(pythonPath, ['handler.py'], {
        cwd: __dirname,
        env: envVars,
        stdio: ['pipe', 'pipe', 'pipe']
      });
      console.log(`Successfully spawned Python process using: ${pythonPath}`);
      break;
    } catch (error) {
      console.error(`Failed to spawn Python process using ${pythonPath}:`, error);
      pythonError = error;
    }
  }

  if (!pythonProcess) {
    console.error('Failed to start Python process with any available Python path');
    res.status(500).json({
      error: 'Internal Server Error',
      message: 'Failed to start Python process',
      details: pythonError ? pythonError.message : 'No Python interpreter found'
    });
    return;
  }

  let dataString = '';
  let errorString = '';

  pythonProcess.stdout.on('data', (data) => {
    const output = data.toString();
    console.log('Python stdout:', output);
    dataString += output;
  });

  pythonProcess.stderr.on('data', (data) => {
    const error = data.toString();
    console.error('Python stderr:', error);
    errorString += error;
  });

  pythonProcess.on('error', (error) => {
    console.error('Python process error:', error);
    res.status(500).json({
      error: 'Internal Server Error',
      message: 'Python process error',
      details: error.message
    });
  });

  // Set a timeout to kill the process if it takes too long
  const timeout = setTimeout(() => {
    console.error('Python process timed out');
    pythonProcess.kill();
    res.status(504).json({
      error: 'Gateway Timeout',
      message: 'Request timed out'
    });
  }, 30000); // 30 seconds timeout

  pythonProcess.on('close', (code) => {
    clearTimeout(timeout);
    console.log('Python process exited with code:', code);
    console.log('Full stdout:', dataString);
    console.log('Full stderr:', errorString);
    
    if (code !== 0) {
      console.error('Python process error output:', errorString);
      res.status(500).json({
        error: 'Internal Server Error',
        message: 'Python process error',
        details: errorString || 'Unknown error occurred'
      });
      return;
    }

    try {
      const responseData = JSON.parse(dataString.trim());
      res.status(200).json(responseData);
    } catch (error) {
      console.error('Failed to parse Python output:', error);
      console.error('Raw output:', dataString);
      res.status(500).json({
        error: 'Internal Server Error',
        message: 'Failed to parse response',
        details: error.message,
        rawOutput: dataString
      });
    }
  });

  // Handle client disconnection
  req.on('close', () => {
    clearTimeout(timeout);
    if (pythonProcess) {
      pythonProcess.kill();
    }
  });
}); 