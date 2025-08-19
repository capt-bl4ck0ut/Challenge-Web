const crypto = require('crypto');
const express = require('express');
const fetch = require('node-fetch');
const path = require('path');
const session = require('express-session');

const app = express();

const adminPassword = crypto.randomBytes(32).toString('hex');

app.use(session({
    secret: crypto.randomBytes(32).toString(),
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }
}))

app.use(express.urlencoded({ extended: true }));

function update(dest, src) {
    for (var key in src) {
        if (typeof src[key] !== 'object') {
            dest[key] = src[key];
        } else {
            if (typeof dest[key] !== 'object') {
                dest[key] = {};
            }
            update(dest[key], src[key]);
        }
    }
}

function setAPI(apiInfo, userApiInfo) {
    update(apiInfo, JSON.parse(userApiInfo));
}

async function callAPI(apiInfo, isAdmin) {
    const baseUrl = `http://${apiInfo['host']}`;
    const path = `${apiInfo['path']}`;
    const method = `${apiInfo['method']}`;

    try {
        const headers = isAdmin ? {'is-admin': 'true'} : {};
        switch (method) {
            case 'GET':
                var response = await fetch(`${baseUrl}${path}`, {
                    method: 'GET',
                    headers: headers,
                });
                break;
            case 'POST':
                headers['Content-Type'] = 'application/json';
                var response = await fetch(`${baseUrl}${path}`, {
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify(apiInfo['body'])
                });
                break;
        }
    } catch (error) {
        console.log(error);
    }

    const data = await response.json();

    if (!data) {
        return null;
    }
    return data;
}

app.post('/auth', (req, res, next) => {
    if (req.body.password === adminPassword) {
        req.session['isAdmin'] = true;
        res.send('true')
        return;
    }
    res.send('false')
});

app.post('/api', async (req, res, next) => {
    var apiInfo = {'host': 'backend:8000'}

    try {
        const userApiInfo = req.body.api_info;
        setAPI(apiInfo, userApiInfo);
    } catch (error) {
        next(error);
        return;
    }

    const data = await callAPI(apiInfo, req.session['isAdmin']);
    res.json(data);
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '/templates/index.html'));
});

app.listen(7000, '0.0.0.0');
