const puppeteer = require("puppeteer")
const Handlebars = require("handlebars")
const { v4: uuidv4 } = require("uuid")
const fs = require("fs")
const path = require("path")

const genReceipt = async (name, email, address, product) => {
  let templateFormat = fs.readFileSync(
    path.join(__dirname, "../views/receipt.hbs"),
    { encoding: "utf8" }
  )
  const template = Handlebars.compile(templateFormat)
  const html = template({
    name: name,
    email: email,
    address: address,
    product: product,
  })
  const htmlPath = path.join(__dirname, `../../tmp/${uuidv4()}.html`)
  fs.writeFileSync(htmlPath, html)
  const url = `file://${htmlPath}`

  try {
    const browser = await puppeteer.launch({
      executablePath: "/usr/bin/google-chrome-stable",
      headless: "new",
      args: ["--no-sandbox", "--disable-gpu"],
    })
    const page = await browser.newPage()
    await page.goto(url, { timeout: 3000 })
    await page.emulateMediaType("screen")
    let options = {
      format: "A4",
    }
    const pdf = await page.pdf(options)
    await browser.close()
    fs.unlinkSync(htmlPath) // tmp file deleted
    return pdf
  } catch (error) {
    console.log("An error occurred while generating receipt: ", error)
  }
}

module.exports = { genReceipt }
