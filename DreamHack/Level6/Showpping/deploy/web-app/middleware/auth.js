const { sign, verify } = require("../utils/jwt")

const auth = async (req, res, next) => {
  try {
    if (req.cookies.session === undefined) {
      return res.redirect("/login")
    } else {
      let userData = await verify(req.cookies.session)
      req.user = userData
      next()
    }
  } catch (error) {
    console.log(error)
    return res.status(500).send("Internal server error.")
  }
}

module.exports = {
  auth,
}
