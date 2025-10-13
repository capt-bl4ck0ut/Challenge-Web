const express=require('express')
const querystring=require('querystring')
const app=express()


app.use(express.text({ type: '*/*' }))
app.use((req, res, next) => {
    const hostname = req.hostname
    if (hostname === 'localhost') {
      next()
    } else {
      res.status(403).send('Forbidden')
    }
  })


app.get('/check',(req,resp)=>{
    const email=req.query.email
    const pw=req.query.pw
    const emailPattern=/[a-zA-Z0-9]+@[a-zA-Z]+\.(co|.kr|co.kr|m)+$/
    match=emailPattern.exec(email)
    if(match==null){
        resp.send('1')
    }else if(pw!='BlSC2024'){
        resp.send('2')
    }else{
        resp.send(email)
    }
})

app.get('/gatcha',(req,resp)=>{
  num=Math.floor(Math.random() * 100) + 1
  if(num==7){
    resp.send(`${num}!!! good:)`)
  }else{
    resp.send(`${num}... ~_~`)
  }
})

app.post('/checkPath', (req, resp)=>{
  try{
    const data=decodeURI(req.body).toLowerCase()
    const path=querystring.parse(data).path
    if(path.includes('flag')){
      resp.send('gatcha')
    }else{
      resp.send(path)
    }
  }catch{
    resp.send('gatcha')
  }
})

app.get('/flag',(req,resp)=>{
  resp.send('bisc2024{[**REDACTED**]}')
})

app.listen(9001)
