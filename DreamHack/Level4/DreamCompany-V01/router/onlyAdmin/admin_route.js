const express = require("express");
const path = require("path");
const router = express.Router();
const checkToken = require("../../apis/token/checkToken");
const adminReport = require("../../apis/admin/admin_report");

router.get("/admin", checkToken, (req, res) => {
  res.sendFile(
    path.join(__dirname, "..", "..", "..", "/pages/html/admin.html")
  );
});

router.get("/admin/get/:report_id", checkToken, (req, res) => {
  const report_id = req.params.report_id;
  res.json({report: adminReport.getReport(report_id)}).status(200);
})

router.get("/admin/all", checkToken, (req, res) => {
  res.json({
    report: adminReport.getReportList()
  }).status(200);
});

module.exports = router;
