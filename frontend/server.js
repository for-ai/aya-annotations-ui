import path from "path";
import { fileURLToPath } from "url";
import compression from "compression";
import dotenv from "dotenv";
import express from "express";

import routes from "./routes.js";

dotenv.config();

// Get current file's path and directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Create an Express app instance
const app = express();

// Use compression middleware
app.use(compression());

// Serve the static files from the React app
app.use(express.static(path.join(__dirname, "dist")));

// Add routes
app.use(routes);

// Handles any requests that don't match the ones above
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname + "/dist/index.html"));
});

// Set the app's listening port
const port = process.env.PORT || 80;
app.listen(port);

// Log information
console.log("App is listening on port " + port);
console.log("ENVIRONMENT: " + process.env.ENVIRONMENT);
console.log("PORT: " + process.env.PORT);
console.log("BACKEND_URL: " + process.env.BACKEND_URL);
console.log("GOOGLE_ANALYTICS_ID: " + process.env.GOOGLE_ANALYTICS_ID);
