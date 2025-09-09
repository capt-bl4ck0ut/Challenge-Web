const express = require("express")
const path = require("path")
const cookieParser = require("cookie-parser")
const { engine } = require("express-handlebars")
const Database = require("./db")
const indexRoute = require("./routes/index")
const purchaseRoute = require("./routes/purchase")
const couponRoute = require("./routes/coupon")

const app = express();
const PORT = 3000

const db = new Database("web-app.db");

app.engine(".hbs", engine({ extname: ".hbs", partialsDir: path.join(__dirname, 'views/partials') }));
app.set("view engine", ".hbs")

app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use("/static", express.static(path.resolve("static")));

app.use("/",indexRoute(db));
app.use("/purchase",purchaseRoute(db));
app.use("/coupon", couponRoute(db));


(async () => {
  await db.connect()
  await db.init()
  app.listen(PORT, () => {
    console.log(`[+] Start on port ${PORT}`)
  })
})();
