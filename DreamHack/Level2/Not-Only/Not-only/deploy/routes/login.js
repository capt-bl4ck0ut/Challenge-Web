const express = require('express');
const router = express.Router();
const path = require('path');

const mongoose = require('mongoose');
mongoose.connect('mongodb://localhost/main', { useNewUrlParser: true, useUnifiedTopology: true });
const db = mongoose.connection;

router.post('/', (req, res) => {
    const uid = req.body.uid;
    const upw = req.body.upw;
  
    
    db.collection('user').findOne({
        'uid': uid,
        'upw': upw,
    }, function(err, result){
        if (err){
            res.send('err');
        }else if(result){
            req.session.user = { uid: result['uid'], admin: result['admin']}; 
            res.redirect('/user');
        }else{
            res.redirect('/login');
        }
    });
  });

router.get('/', function(req, res) {
    res.render("login.ejs");
});

module.exports = router;