const util = require('total.js/utils')

var obj = {
    'background_color':'#ffffff',
    'text_color':'#000000'
}

exports.install = function () {
    ROUTE('/', home);
    ROUTE('POST /change', change);
};

function home(){
    this.view('index', [o=obj])
}

function home() {
    this.view('index', [o=obj]);
}

function change() {
    let new_background_color = this.body.background_color
    let new_text_color = this.body.text_color
    if (!new_background_color || !new_text_color){
        this.plain("No, I can't huhu")
    }
    for (i in this.body){
        util.set(obj, i, this.body[i])
    }
    this.plain('OK, changed');
}