const express = require("express");
const path = require("path");
const router = express.Router();
const checkToken = require("../../apis/token/checkToken");
const session = require("../../apis/session/session");

router.use(express.static("../pages/css"));
router.use(express.static("../pages/js"));

router.get("/", checkToken, function (req, res, next) {
  res.sendFile(
    path.join(__dirname, "..", "..", "..", "/pages/html/manage.html")
  );
});

router.get("/session", checkToken, function (req, res, next) {
  const all_session = session.all_session;
  res
    .json({
      session: all_session,
    })
    .status(200);
});

router.post("/", function (req, res, next) {});

module.exports = router;
