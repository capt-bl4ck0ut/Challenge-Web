const router = require("express").Router()
const { genReceipt } = require("../utils/genReceipt")
const { auth } = require("../middleware/auth")
const { exec } = require("child_process")
const { promisify } = require("util")
const execAsync = promisify(exec)

module.exports = (database) => {
  let db = database

  router.get("/:id", auth, async (req, res) => {
    const id = req.params.id
    const name = req.user.name
    return db.getUser(name).then(async (user) => {
      if (user === undefined) {
        return redirect("/login")
      }
      return db.getProduct(id).then(async (product) => {
        if (product === undefined) {
          return res.send({ msg: "Invalid product id." })
        }
        if (user.balance >= product.price) {
          const newBalance = user.balance - product.price
          db.setBalance(user.name, newBalance).then(async () => {
            const email = user.email
            const address = user.address
            if (product.product_name === "FLAG") {
              const { stdout: flag } = await execAsync("/flag")
              const pdf = await genReceipt(name, email, flag, product)
              res.contentType("application/pdf")
              return res.send(pdf)
            } else {
              const pdf = await genReceipt(name, email, address, product)
              res.contentType("application/pdf")
              return res.send(pdf)
            }
          })
        } else {
          return res.status(403).send({ msg: "Insufficient balance." })
        }
      })
    })
  })

  router.get("/non/:id", async (req, res) => {
    const id = req.params.id
    return res.render("form", { layout: false, id: id })
  })

  router.post("/non/:id", async (req, res) => {
    const id = req.params.id
    const name = req.body.name
    const email = req.body.email
    const address = req.body.address

    return db.getProduct(id).then(async (product) => {
      if (product === undefined) {
        return res.status(500).send({ msg: "Invalid product id." })
      }

      if (product.id === 1) {
        return res
          .status(403)
          .send({ msg: "Not allowed to buy the flag as non-member." })
      }

      const pdf = await genReceipt(name, email, address, product)
      res.contentType("application/pdf")
      return res.send(pdf)
    })
  })

  return router
}
