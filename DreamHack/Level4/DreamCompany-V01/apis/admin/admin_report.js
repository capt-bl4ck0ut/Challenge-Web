const report_list = {};

const reportInit = () => {
  const report_msg = [
    "[**SECRET_CONTENT**]",
    "[**SECRET_CONTENT**]",
    "[**SECRET_CONTENT**]",
    "[**SECRET_CONTENT**]",
    "[**SECRET_CONTENT**]",
    "[**SECRET_CONTENT**]",
    "[**SECRET_CONTENT**]",
  ];
  for (let i = 0; i < report_msg.length; i++) {
    report_list[i] = {
      id: i,
      type: "report",
      group: i < 3 ? "admin" : "super_admin",
      msg: report_msg[i],
      time: new Date().getTime(),
    };
  }
};

const getReportList = () => {
  const allReportList = JSON.parse(JSON.stringify(report_list));
  for (let report in allReportList) {
    if (allReportList[report].group == "super_admin") {
      allReportList[report].msg = "Access Denied";
    }
  }
  return allReportList;
};

const getReport = (report_id) => {
  let reportData = JSON.parse(JSON.stringify(report_list));
  try {
    return reportData[report_id];
  } catch (e) {
    return {};
  }
};

module.exports.init = reportInit;
module.exports.getReportList = getReportList;
module.exports.getReport = getReport;
