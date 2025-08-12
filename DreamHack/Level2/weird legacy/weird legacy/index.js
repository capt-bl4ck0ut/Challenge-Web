const express = require("express");
const node_fetch = require("node-fetch");
const app = express();
const PORT = 3000;
const FLAG = "DH{dummy}";

app.get("/", async (req, res) => {
  res.sendFile(__dirname + "/views/index.html");
});

app.get("/fetch", async (req, res) => {
  const url = req.query.url;

  if (!url) return res.send("?url=<br>ex) http://localhost:3000/");

  let host;
  try {
    const urlObject = new URL(url);
    host = urlObject.hostname;

    if (host !== "localhost" && !host.endsWith("localhost")) return res.send("rejected");
  } catch (error) {
    return res.send("Invalid Url");
  }

  try {
    let result = await node_fetch(url, {
      method: "GET",
      headers: { "Cookie": `FLAG=${FLAG}` },
    });
    const data = await result.text();
    res.send(data);
  } catch {
    return res.send("Request Failed");
  }
});

app.listen(PORT, () => {
  console.log(`Server Running on ${PORT}`);
});