const express=require('express');
const bodyParser=require('body-parser');
const ejs=require('ejs');
const hash=require('crypto-js/sha256');
const fs = require('fs');
const app=express();


var file={};
var read={};
function isObject(obj) {
  return obj !== null && typeof obj === 'object';
}
function setValue(obj, key, value) {
  const keylist = key.split('.');
  const e = keylist.shift();
  if (keylist.length > 0) {
    if (!isObject(obj[e])) obj[e] = {};
    setValue(obj[e], keylist.join('.'), value);
  } else {
    obj[key] = value;
    return obj;
  }
}

app.use(bodyParser.urlencoded({ extended: false }));
app.set('view engine','ejs');


app.get('/',function(req,resp){
	read['filename']='fake';
	resp.render(__dirname+"/ejs/index.ejs");

})

app.post('/mkfile',function(req,resp){
	let {filename,content}=req.body;
	filename=hash(filename).toString();
	fs.writeFile(__dirname+"/storage/"+filename,content,function(err){
		if(err==null){
			file[filename]=filename;
			resp.send('your file name is '+filename);
		}else{
			resp.write("<script>alert('error')</script>");
			resp.write("<script>window.location='/'</script>");
		}
	})

})

app.get('/readfile',function(req,resp){
	let filename=file[req.query.filename];
	if(filename==null){
		fs.readFile(__dirname+'/storage/'+read['filename'],'UTF-8',function(err,data){
			resp.send(data);
		})
	}else{
		read[filename]=filename.replaceAll('.','');
		fs.readFile(__dirname+'/storage/'+read[filename],'UTF-8',function(err,data){
			if(err==null){
				resp.send(data);
			}else{
				resp.send('file is not existed');
			}
		})
	}

})

app.get('/test',function(req,resp){
	let {func,filename,rename}=req.query;
	if(func==null){
		resp.send("this page hasn't been made yet");
	}else if(func=='rename'){
		setValue(file,filename,rename)
		resp.send('rename');
	}else if(func=='reset'){
		read={};
		resp.send("file reset");
	}
})


app.listen(8000);
