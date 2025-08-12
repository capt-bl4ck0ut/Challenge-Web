const express = require('express');
const router = express.Router();


router.get('/', (req, res) => {
  const user = req.session.user; 

  if (user) {
    res.render('user', { user: user }); 
  } else {
    res.redirect('/login'); 
  }
});

module.exports = router;
