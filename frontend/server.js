//Install express server
const express = require('express');
const path = require('path');

const app = express();

// Serve only the static files form the dist directory
app.use(express.static('./build'));

app.get('/*', (req, res) =>
    res.sendFile('index.html', { root: 'dist/' }),
);

const port = process.env.PORT || '4000';
app.listen(port, () => {
    console.log('Express server listening on port', port)
});