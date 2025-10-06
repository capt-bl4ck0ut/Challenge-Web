function list_search(f){
	sel = f.sel.value;
	word = f.word.value;
	window.location.href="./M.list."+sel+"."+word;
	return false;
}

function list_init(s, w){
	if (s != '') $('select[name=sel]').val(s);
	if (w != '') $('input[name=word]').val(w);
}
