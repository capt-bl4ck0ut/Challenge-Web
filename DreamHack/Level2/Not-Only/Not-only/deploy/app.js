const express = require('express');
const app = express();
const path = require('path');
const port = 3000;
const loginRouter = require('./routes/login'); 
const userRouter = require('./routes/user'); 
const session = require('express-session');

app.use(session({
  secret: 'REDACTED',
  resave: false,
  saveUninitialized: true
}));


app.use(express.urlencoded({ extended: false }));
app.use(express.json());

app.set('view engine','ejs')
app.set('views', path.join(__dirname, 'views')); 


app.get('/', (req, res) => {
  res.render("index.ejs");
});


app.use('/login', loginRouter);


app.use('/user', userRouter);

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
})
