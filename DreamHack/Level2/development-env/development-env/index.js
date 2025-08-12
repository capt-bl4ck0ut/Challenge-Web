const express = require("express");
const cryptolib = require("./libs/customcrypto");
var cookieParser = require("cookie-parser");
var parsetrace = require("parsetrace");

const isDevelopmentEnv = true;

const app = express();
const port = 3000;

const flag = "DH{FAKE_FLAG}";
app.set("view engine", "ejs");

app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

let database = {
  guest: "guestPW",
  admin: cryptolib.generateRandomString(15),
}; //don't try to guess admin password

app.get("/", async (req, res) => {
  try {
    let token = req.cookies.auth || "";
    const payloadData = await cryptolib.readJWT(token, "FAKE_KEY");
    if (payloadData) {
      userflag = payloadData["uid"] == "admin" ? flag : "You are not admin";
      res.render("main", { username: payloadData["uid"], flag: userflag });
    } else {
      res.render("login");
    }
  } catch (e) {
    if (isDevelopmentEnv) {
      res.json(JSON.parse(parsetrace(e, { sources: true }).json()));
    } else {
      res.json({ message: "error" });
    }
  }
});

app.post("/validate", async (req, res) => {
  try {
    let contentType = req.header("Content-Type").split(";")[0];
    if (
      ["multipart/form-data", "application/x-www-form-urlencoded"].indexOf(
        contentType
      ) === -1
    ) {
      throw new Error("content type not supported");
    } else {
      let bodyKeys = Object.keys(req.body);
      if (bodyKeys.indexOf("id") === -1 || bodyKeys.indexOf("pw") === -1) {
        throw new Error("missing required parameter");
      } else {
        if (
          typeof database[req.body["id"]] !== "undefined" &&
          database[req.body["id"]] === req.body["pw"]
        ) {
          if (
            req.get("User-Agent").indexOf("MSIE") > -1 ||
            req.get("User-Agent").indexOf("Trident") > -1
          )
            throw new Error("IE is not supported");
          jwt = await cryptolib.generateJWT(req.body["id"], "FAKE_KEY");
          res
            .cookie("auth", jwt, {
              maxAge: 30000,
            })
            .send(
              "<script>alert('success');document.location.href='/'</script>"
            );
        } else {
          res.json({ message: "error", detail: "invalid id or password" });
        }
      }
    }
  } catch (e) {
    if (isDevelopmentEnv) {
      res.status(500).json({
        message: "devError",
        detail: JSON.parse(parsetrace(e, { sources: true }).json()),
      });
    } else {
      res.json({ message: "error", detail: e });
    }
  }
});

app.listen(port);
