const express = require('express');
const basicAuth = require('express-basic-auth');
const fetch = require('node-fetch');
const fs = require('fs');

const app = express();
const port = 3000;
const flag = fs.readFileSync('flag.txt', 'utf8');


const genRanHex = size =>
  [...Array(size)].map(() => Math.floor(Math.random() * 16).toString(16)).join('');

const users = {
  'admin': genRanHex(16),
};


const loginRequired = basicAuth({
  authorizer: (username, password) => users[username] == password,
  unauthorizedResponse: 'Unauthorized',
});

const adminOnly = (req, res, next) => {
  if (req.auth?.user == 'admin') {
    return next();
  }
  return res.status(403).send('Only admin can access this resource');
};


app.get('/', (req, res) => {
  res.send('login with http://username:password@...');
});

app.get('/register', (req, res) => {
  res.send('Not implemented');
});

app.get('/report', loginRequired, (req, res) => {
  const path = req.query.path;

  if (!path) {
    return res.send("<form method='GET'>http://<input name='path' /><button>Submit</button></form>");
  }

  fetch(`https://admin:${users["admin"]}@${path}`)
    .then(() => res.send("Success"))
    .catch(() => res.send("Error"));
});

app.get('/admin', loginRequired, adminOnly, (req, res) => {
  res.send(flag);
});


app.listen(port, '0.0.0.0', () => {
  console.log(`Server listening at http://localhost:${port}`);
});