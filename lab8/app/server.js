const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({
    message: '🚀 DevOps Lab 8 — CD Pipeline',
    version: '2.0.0',
    env: process.env.NODE_ENV || 'development',
    timestamp: new Date().toISOString(),
    host: require('os').hostname(),
    author: 'Nguyen Van Nam - DTC235180129'
  });
});

app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

app.listen(PORT, () => console.log(`App running on port :${PORT}`));
