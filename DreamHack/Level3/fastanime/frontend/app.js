const express = require("express")
const path = require('path');
const cookieParser = require('cookie-parser');

const app = express()
const HOST = "0.0.0.0"
const PORT = "3000"

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.static('css'));

app.use(cookieParser());
app.use(express.urlencoded({ extended: true }));

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000"

console.log(BACKEND_URL)

app.get("/", (req, res) => {
    res.render("index")
})

app.get("/login", (req, res) => {
    res.render("login")
})

app.post("/login", async (req, res) => {
    username = req.body['username']
    password = req.body['password']
    if (!username || !password){
        res.send("<script>alert('not enough information')</script>")
    }
    const r = await fetch(BACKEND_URL + "/api/login", {
        method:"POST", 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(req.body),
    })
    if (r.status === 400) {
        return res.send("<script>alert('failed to login')</script>");
    }
    const setCookie = r.headers.get("set-cookie");
    if (setCookie) {
        res.setHeader("Set-Cookie", setCookie);
    }
    return res.send("<script>alert('login successfully'); location='/gen'</script>");
})

app.get("/register", (req, res) => {
    res.render("register")
})

app.post("/register", async (req, res) => {
    username = req.body['username']
    password = req.body['password']
    if (!username || !password){
        res.send("<script>alert('not enough information')</script>")
    }
    const r = await fetch(BACKEND_URL + "/api/register", {
        method:"POST", 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(req.body),
    })
    if (r.status === 400) {
        return res.send("<script>alert('failed to register')</script>");
    }
    const setCookie = r.headers.get("set-cookie");
    if (setCookie) {
        res.setHeader("Set-Cookie", setCookie);
    }
    return res.send("<script>alert('register successfully'); location='/gen'</script>");
})

app.get("/gen", async (req, res) => {
    let count = req.query.count
    if (!count) count = 3
    const r = await fetch(BACKEND_URL + `/api/gen?count=${count}&url=https://any-anime-api.vercel.app/v1/anime/png`, {
        method: "POST"
    })
    const d = await r.json()
    res.render("gen", m=d.m)
})

app.get("/debug", async (req, res) => {
    let mode = req.query.mode;
    let matches
    try{
        matches = mode.match(/\b(?:true|True|1)\b/g);
    }
    catch (err){
        res.send("no mode provided");
    }
    if (matches) {
        res.send("no, i don't remember to use it");
    } else {
        const r = await fetch(BACKEND_URL + `/api/debug?filename=config.json&mode=${mode}&permission=False`, {
            method: "POST",
            headers: {
                'Cookie': req.headers.cookie || '', 
            }
        });

        const d = await r.text();
        res.send(d);
    }
});

app.listen(PORT, HOST, () => {
    console.log(`Listening on port ${PORT}`)
})