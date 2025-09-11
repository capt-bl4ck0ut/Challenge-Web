const express = require("express");
const path = require("path");
const createToken = require("../../apis/token/createToken");
const checkXSS = require("../../apis/filter/check_xss");
const session = require("../../apis/session/session");
const router = express.Router();

const settingJWT = (user) => {
  const AccessToken = createToken.createAccessToken(user.id);
  if (AccessToken) {
    return {
      access: AccessToken,
      message: "success",
    };
  } else {
    return {
      status: 500,
      message: "Error",
    };
  }
};

const filter = (data, res) => {
  const isXSS = checkXSS(data);
  if (isXSS === true) {
    res.status(403).send("XSS filter");
    return true;
  }
};

router.use(express.static("../pages/css"));
router.use(express.static("../pages/js"));

router.get("/account", function (req, res) {
  res.sendFile(
    path.join(__dirname, "..", "..", "..", "/pages/html/account.html")
  );
});

router.post("/account", async function (req, res, next) {
  const isFilter = await filter(req.body, res);
  const isAccount = session.check(req.body.id, req.body.password);
  if (isFilter === true) {
    return;
  } else if (isAccount === true || isAccount === "ADMIN") {
    const result = settingJWT(
      isAccount === "ADMIN"
        ? { id: req.body.id["admin_id"] }
        : { id: req.body.id }
    );
    res
      .cookie("JWT", result.access)
      .json({
        message: result.message,
      })
      .status(200);
  } else if (isAccount === false) {
    const isAdded = session.add(req.body.id, req.body.password);
    res
      .json({
        message: isAdded === true ? "signup success" : "fail",
      })
      .status(403);
  } else {
    res
      .json({
        message: "Error or invalid account",
      })
      .status(403);
  }
});

module.exports = router;
