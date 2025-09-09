const jwt = require("jsonwebtoken");
const crypto = require("crypto");

const SECRET_KEY = crypto.randomBytes(32).toString("hex");

const sign = async (userData) =>{
    return jwt.sign(userData, SECRET_KEY, { algorithm: "HS256"});
}

const verify = (userData) =>{
    return jwt.verify(userData, SECRET_KEY, { algorithms: "HS256"});
}

module.exports = {
    sign, 
    verify
}