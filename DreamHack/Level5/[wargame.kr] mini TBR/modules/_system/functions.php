<?php
 if(!defined('__BHACK__')) exit();

 function db_conn(){
 	global $_BHVAR;
	mysql_connect($_BHVAR['db']['host'], $_BHVAR['db']['user'], $_BHVAR['db']['pass']);
	mysql_select_db($_BHVAR['db']['name']);
 }

 function get_layout($layout, $pos){
	$result = mysql_query("select path from _BH_layout where layout_name='$layout' and position='$pos'");
	$row = mysql_fetch_array($result);
	$allow_list = ["./book_store_skin/head.html", "./book_store_skin/foot.html", "./reverted/h.htm", "./reverted/f.htm"];

	if (isset($row['path'])){
		if ($row['path'] == "hacked") {
			die("FLAG is DH{**CENSORED**}");
		}
		if (in_array($row['path'], $allow_list)) {
			return $row['path'];
		}
	}

	if ($pos == 'head'){
		return "./reverted/h.htm";
	}
	return "./reverted/f.htm";
 }

 function filtering($str){
 	$str = preg_replace("/select/","", $str);
 	$str = preg_replace("/union/","", $str);
 	$str = preg_replace("/from/","", $str);
 	$str = preg_replace("/load_file/","", $str);
 	$str = preg_replace("/ /","", $str);
 	return $str;
 }


?>
