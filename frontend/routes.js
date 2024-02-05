// routes.js
import express from "express";

const router = express.Router();

// An endpoint to get the BACKEND_URL
router.get("/backend-url", (req, res) => {
  res.send({ backendUrl: process.env.BACKEND_URL });
});

export default router;
