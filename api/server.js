const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(cors());

// Get your API key from an environment variable (set in Vercel)
// or fallback to the default.
const API_KEY = process.env.API_KEY || "vV7yhrHeM5SseeQHn7f-ndckmR8l4h4J";
const BASE_URL = "https://api.rbxstats.xyz/api";

// Helper function to proxy the request.
async function proxyRequest(targetUrl, res) {
  try {
    const response = await axios.get(targetUrl);
    // Set the content type header based on the remote response.
    res.set('Content-Type', response.headers['content-type'] || 'application/json');
    res.status(response.status).send(response.data);
  } catch (error) {
    res.status(500).send(`Error fetching data: ${error.message}`);
  }
}

// Define the endpoints.
app.get('/offsets', async (req, res) => {
  const targetUrl = `${BASE_URL}/offsets?api=${API_KEY}`;
  await proxyRequest(targetUrl, res);
});

app.get('/offsets/plain', async (req, res) => {
  const targetUrl = `${BASE_URL}/offsets/plain?api=${API_KEY}`;
  await proxyRequest(targetUrl, res);
});

app.get('/offsets/search/:name', async (req, res) => {
  const name = req.params.name;
  const targetUrl = `${BASE_URL}/offsets/search/${name}?api=${API_KEY}`;
  await proxyRequest(targetUrl, res);
});

// Export the Express app as a Vercel serverless function.
module.exports = app;
