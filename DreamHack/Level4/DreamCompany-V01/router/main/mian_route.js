const express = require("express");
const path = require("path");
const router = express.Router();

router.use(express.static("../pages/css"));
router.use(express.static("../pages/js"));
router.use(express.static("../pages/image"));

router.get("/", function (req, res, next) {
  res.sendFile(
    path.join(__dirname, "..", "..", "..", "/pages/html/index.html")
  );
});

router.get("/description", function (req, res, next) {
  res.sendFile(
    path.join(__dirname, "..", "..", "..", "/pages/html/description.html")
  );
});

module.exports = router;
