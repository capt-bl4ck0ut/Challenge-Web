const router = require("express").Router()
const { sign, verify } = require("../utils/jwt")
const { genReceipt } = require("../utils/genReceipt")
const { auth } = require("../middleware/auth")

module.exports = (database) => {
  let db = database

  router.get("/login", (req, res) => {
    return res.render("login", { layout: false })
  })

  router.post("/login", async (req, res) => {
    const name = req.body.name
    const password = req.body.password

    const user = await db.checkUser(name, password)
    if (user === undefined) {
      return res
        .status(401)
        .render("login", { layout: false, loginFailed: true })
    } else {
      const jwt = await sign({name: user.name, isLogin: true })
      res.cookie("session", jwt, { maxAge: 3600000 })
      return res.redirect("/")
    }
  })

  router.get("/mypage", auth, async (req, res) => {
    const user = await db.getUser(req.user.name)
    return res.render("mypage", { user: user, name: user.name })
  })

  router.get("/", auth, async (req, res) => {
    const products = await db.getProducts()
    if (req.user !== undefined) {
      return res.render("index", { products: products, name: req.user.name })
    }
  })
  return router
}
