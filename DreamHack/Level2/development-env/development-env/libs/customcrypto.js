const crypto = require("crypto").webcrypto;
const b64Lib = require("base64-arraybuffer");

const generateRandomString = (length) => {
  var q = "";
  for (var i = 0; i < length; i++) {
    q += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789".split(
      ""
    )[parseInt((crypto.getRandomValues(new Uint8Array(1))[0] / 255) * 61)];
  }
  return q;
};

const verifyJWT = async (token, key) => {
  try {
    let baseKey = await crypto.subtle.importKey(
      "raw",
      new TextEncoder().encode(key),
      { name: "HMAC", hash: "SHA-256" },
      false,
      ["verify"]
    );
    var splited = token.split(".");

    let sig = b64Lib.decode(decodeurlsafe(splited[2]));
    let isValid = await crypto.subtle.verify(
      { name: "HMAC" },
      baseKey,
      sig,
      new TextEncoder().encode(`${splited[0]}.${splited[1]}`)
    );
    return isValid;
  } catch (e) {
    return false;
  }
};

const readJWT = async(data,key) =>{
  const decoder = new TextDecoder()
  const isVerified = await verifyJWT(data,key)
  if(isVerified){
    let payload = data.split(".")[1]
    return JSON.parse(decoder.decode(b64Lib.decode(decodeurlsafe(payload))).replaceAll('\x00',''))
  }else{
    return false
  }
}

const generateJWT = async (userId, key) => {
  const strEncoder = new TextEncoder();
  let headerData = urlsafe(
    b64Lib.encode(
      strEncoder.encode(JSON.stringify({ alg: "HS256", typ: "JWT" }))
    )
  );
  let payload = urlsafe(
    b64Lib.encode(
      strEncoder.encode(
        JSON.stringify({
          uid: userId,
        })
      )
    )
  );

  let baseKey = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(key),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );

  let sig = await crypto.subtle.sign(
    { name: "HMAC" },
    baseKey,
    new TextEncoder().encode(`${headerData}.${payload}`)
  );

  return `${headerData}.${payload}.${urlsafe(
    b64Lib.encode(new Uint8Array(sig))
  )}`;
};

const urlsafe = (base) => {
  return base.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
};

const decodeurlsafe = (dat) => {
  dat += Array(5 - (dat.length % 4)).join("=");

  var data = dat.replace(/\-/g, "+").replace(/\_/g, "/");
  return data;
};

module.exports = {
  generateRandomString,
  readJWT,
  generateJWT,
};
