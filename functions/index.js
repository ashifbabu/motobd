const functions = require('firebase-functions');
const admin = require('firebase-admin');

admin.initializeApp();

// Example HTTP function (you can remove this if not needed)
exports.helloWorld = functions.https.onRequest((request, response) => {
  response.json({message: "Hello from Firebase!"});
}); 