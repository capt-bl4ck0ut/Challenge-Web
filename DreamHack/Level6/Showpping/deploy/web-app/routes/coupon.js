const router = require("express").Router()
const { auth } = require("../middleware/auth")
const axios = require("axios")

const HOST = process.env.HOST || "127.0.0.1"
const PORT = process.env.PORT || "8000"

const sleep = (ms)=>{
    return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = (database) =>{
    let db = database

    router.get("/use", auth, (req, res) => {
        return res.render("coupon", {name: req.user.name})
      })


    router.post("/use", auth, async (req, res) => {
        const name = req.user.name
        const coupon = req.body.coupon

        return db.getUser(name).then( async (user)=>{
            if (user.used === 1){
                return res.render("coupon", {msg: "Already used coupon.", name: name})
            }
            if (user.coupon !== coupon){
                return res.render("coupon", {msg: "Does not match the coupon you have.", name: name})
            }
            return db.getCoupon(coupon).then(async (coupon)=>{
                if (coupon === undefined){
                    return res.render("coupon", {msg: "Coupon does not exist.", name: name})
                }
                await sleep(50)
                return db.addBalance(name, coupon.value).then(()=>{
                    return db.setUsedCoupon(name).then(()=>{
                        return res.render("coupon", {msg: "Success.", name: name})
                    })
                })
            })

        })
      })
    
    
    router.get("/register", auth, (req, res) => {
        return res.render("coupon", { endpoint: "register", name: req.user.name })
      })

    
    router.post("/register", auth, async (req, res) => {
        const name = req.user.name
        const coupon = req.body.coupon
        try {
            let response = await axios.get(`http://${HOST}:${PORT}/verify?coupon=${coupon}`)
            const { result, coupon_data } = response.data

            if (result){
                if (coupon_data.admin === "1" && /^[1-9]\d*$/.test(coupon_data.value) && parseFloat(coupon_data.value) <= 2000){
                    return db.addCoupon(coupon, coupon_data.name, coupon_data.value, coupon_data.admin).then(()=>{
                        return db.setCoupon(name, coupon_data.coupon).then(()=>{
                            return res.render("coupon", {endpoint: "register", msg: "Success.", name: name})
                        })
                    }).catch((error)=>{return res.render("coupon", {endpoint: "register", msg: error, name: name})})
                }
                return res.render("coupon", {endpoint: "register", msg: "Invalid coupon data.", name: name})
            }
                return res.render("coupon", {endpoint: "register", msg: "Invalid coupon.", name: name})
        } catch (error) {
            console.log(error)
            return res.render("coupon", {endpoint: "register", msg: error, name: name})
        }
    })

    router.get("/reset", auth, async (req, res) => {
        return db.resetBCU(req.user.name).then(()=>{
            db.deleteCoupons().then(()=>{
                return res.json({result: true, msg: "OK."})
            })
        })
    })


    
    // router.post("/welcome", auth, async (req, res) => {
    //     const name = req.user.name
    //     try {
    //         let response = await axios.get(`http://${HOST}:${PORT}/key?file=key_0`)
    //         let key = response.data

    //         response = await axios.get(`http://${HOST}:${PORT}/get_coupon?key=${key.msg}`)
    //         let coupon = response.data
    //         if (coupon.result){
    //             db.addBalance(req.user.name, response.data.coupon_data.value).then(()=>{
    //                 return res.render("coupon", {msg: "Success.", name: name})
    //             })
    //         }
    //             return res.render("coupon", {msg: "Fail.", name: name})
    //     } catch (error) {
    //         console.log(error)
    //         return res.render("coupon", {msg: error, name: name})
    //     }
    //   })


    return router
}