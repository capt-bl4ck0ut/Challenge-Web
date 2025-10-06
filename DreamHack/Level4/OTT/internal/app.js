const express = require("express");
const crypto = require("crypto");
const xmlCrypto = require("xml-crypto");
const { v4: uuidv4 } = require("uuid");
const { DOMParser } = require("@xmldom/xmldom");
const select = require("xpath").useNamespaces({
  ds: "http://www.w3.org/2000/09/xmldsig#",
});

const app = express();
const tokenStore = new Map();

const sendUserError = (res, message) =>
  res.status(400).json({ error: message });

const tokenError = (res, message) =>
  res.status(400).json({ error: message });

const { privateKey, publicKey } = crypto.generateKeyPairSync("rsa", {
  modulusLength: 2048,
  publicKeyEncoding: { type: "spki", format: "pem" },
  privateKeyEncoding: { type: "pkcs8", format: "pem" },
});

const signingKey = privateKey;
const signingAlgorithm =
  "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256";
const digestAlgorithm = "http://www.w3.org/2001/04/xmlenc#sha256";
const canonicalizationAlgorithm =
  "http://www.w3.org/TR/2001/REC-xml-c14n-20010315";

const signXml = (xml) => {
  const sig = new xmlCrypto.SignedXml();

  sig.privateKey = signingKey;
  sig.signatureAlgorithm = signingAlgorithm;
  sig.canonicalizationAlgorithm = canonicalizationAlgorithm;

  sig.addReference({
    xpath: "//*[local-name()='SignedUserData']",
    transforms: [
      "http://www.w3.org/2000/09/xmldsig#enveloped-signature",
      canonicalizationAlgorithm,
    ],
    digestAlgorithm,
  });

  sig.computeSignature(xml);
  return sig.getSignedXml();
};

const validateXml = (xml) => {
  try {
    const sig = new xmlCrypto.SignedXml();
    const doc = new DOMParser().parseFromString(xml, "application/xml");
    const errors = doc.getElementsByTagName("parsererror");

    if (errors.length > 0) return false;

    const signature = select("//ds:Signature[1]", doc, true);
    if (!signature) return false;

    sig.loadSignature(signature);
    sig.publicCert = publicKey;

    return sig.checkSignature(xml);
  } catch {
    return false;
  }
};

app.get("/issue", (req, res) => {
  const user = req.query.user;
  if (!user) return sendUserError(res, "Username not provided");

  if (user.toLowerCase().includes("admin"))
    return sendUserError(res, "Invalid username: admin is not allowed");

  if (!/^[a-zA-Z0-9]+$/.test(user))
    return sendUserError(
      res,
      "Invalid username: only alphanumeric characters are allowed"
    );

  const xmlToSign =
    `<SignedUserData Id="userDataToSign"><Username>${user}</Username></SignedUserData>`;

  try {
    const signedXml = signXml(xmlToSign);
    const base64UrlXml = Buffer.from(signedXml).toString("base64url");

    if (!validateXml(signedXml))
      return tokenError(
        res,
        "Failed to process token (internal validation failed)"
      );

    const uuid = uuidv4();
    tokenStore.set(uuid, signedXml);

    res.json({ token: uuid, tokenXml: base64UrlXml });
  } catch {
    return tokenError(res, "Failed to issue or process token");
  }
});

app.get("/map", (req, res) => {
  const tokenXmlBase64 = req.query.tokenXml;
  if (!tokenXmlBase64) return tokenError(res, "No tokenXml provided");

  try {
    const xml = Buffer.from(tokenXmlBase64, "base64url").toString("utf8");

    if (!validateXml(xml))
      return tokenError(res, "Invalid signature (map validation)");

    const uuid = uuidv4();
    tokenStore.set(uuid, xml);

    res.json({ token: uuid });
  } catch {
    return tokenError(res, "Invalid token format or processing error");
  }
});

app.get("/user", (req, res) => {
  const tokenUuid = req.query.token;
  if (!tokenUuid || !tokenStore.has(tokenUuid))
    return tokenError(res, "Invalid or missing token UUID");

  const xml = tokenStore.get(tokenUuid);

  try {
    const doc = new DOMParser().parseFromString(xml, "application/xml");
    const errors = doc.getElementsByTagName("parsererror");

    if (errors.length > 0)
      return tokenError(res, "Invalid token: XML parsing failed");

    const usernameNode = doc.getElementsByTagName("Username")[0];
    const username = usernameNode?.textContent.trim();

    if (!username)
      return tokenError(res, "Invalid token: no username found");

    res.json({ valid: true, username });
  } catch {
    return tokenError(res, "Invalid token: processing failed");
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, "0.0.0.0", () => {
  console.log(`Server running on port ${PORT}`);
});
