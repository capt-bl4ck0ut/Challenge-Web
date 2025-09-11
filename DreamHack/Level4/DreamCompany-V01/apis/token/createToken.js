const jwt = require("jsonwebtoken");

module.exports.createAccessToken = function (user_id) {
  return (accessToken = jwt.sign(
    {
      id: user_id,
    },
    "[**SECRET_KEY**]",
    {
      expiresIn: "1h",
      issuer: "cotak",
    }
  ));
};
