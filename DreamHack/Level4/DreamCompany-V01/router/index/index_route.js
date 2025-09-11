const accountRouter = require("../account_account/account_route");
const mainRouter = require("../main/mian_route");
const adminRouter = require("../onlyAdmin/admin_route");
const manageRouter = require("../onlyAdmin/manage_route");

module.exports.adminRouter = adminRouter;
module.exports.manageRouter = manageRouter;
module.exports.accountRouter = accountRouter;
module.exports.mainRouter = mainRouter;
