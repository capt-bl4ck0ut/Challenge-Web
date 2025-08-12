const express = require('express');
const cookieParser = require('cookie-parser');
const serialize = require('node-serialize');
const app = express();
app.use(cookieParser())

app.get('/', (req, res) => {
    if (req.cookies.profile) {
        let str = new Buffer.from(req.cookies.profile, 'base64').toString();

        // Special Filter For You :)

        let obj = serialize.unserialize(str);
        if (obj) {
            res.send("Set Cookie Success!");
        }
    } else {
        res.cookie('profile', "eyJ1c2VybmFtZSI6ICJndWVzdCIsImNvdW50cnkiOiAiS29yZWEifQ==", {
            maxAge: 900000,
            httpOnly: true
        });
        res.redirect('/');
    }

});

app.listen(5000);