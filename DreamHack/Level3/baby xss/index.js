const express = require('express');
const crypto = require("crypto");
const puppeteer = require('puppeteer');
const cookieParser = require('cookie-parser');
const app = express();
const PORT = 3000;
const delay = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));
const FLAG = process.env.FLAG ?? "DH{dummy}";
const cookies = [
  { name: 'flag', value: FLAG, domain: '127.0.0.1' },
];
const saved = new Map();

app.use(express.json());
app.use(cookieParser());

app.get("/", (req, res) => {
  res.sendFile(__dirname + '/views/index.html');
})

app.get("/music", (req, res) => {
  res.sendFile(__dirname + '/views/music.html');
})

app.post("/save", (req, res) => {
  const id = crypto.randomBytes(20).toString('hex');
  saved.set(id, req.body.age);
  res.send(`saved! Remember your id: ${id}`);
})

app.get("/saved", (req, res) => {
  res.sendFile(__dirname + '/views/saved.html');
})

app.post("/saved", (req, res) => {
  const age = saved.get(req.body.id);
  res.send(age ? age : 'false');
})

app.get("/report", (req, res) => {
  res.sendFile(__dirname + '/views/report.html');
})

app.post("/report", (req, res) => {
  (async () => {
    const browser = await puppeteer.launch({
      executablePath: '/usr/bin/google-chrome',
      args: ["--no-sandbox"]
    });
    const page = await browser.newPage();
    await page.setCookie(...cookies);

    await page.goto(req.body.url);
    await delay(500);

    await browser.close();
  })();
  res.end('Reported!');
})

app.listen(PORT, () => {
  console.log('Running at ' + PORT);
})