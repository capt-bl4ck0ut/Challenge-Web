<?php

ini_set("display_errors", false);
define('__BHACK__',true);
session_start();
#sleep(1);
$_BHVAR = Array(
	'path_layout'	=>	'./layouts/',
	'path_lib'	=>	'./lib/',
	'path_module'	=>	'./modules/',
	'path_page'	=>	'./pages/',
	'path_tmp'	=>	'./tmp/'
);

 if(!get_magic_quotes_gpc()){
         $_GET = escape($_GET);
         $_POST = escape($_POST);
         $_COOKIE = escape($_COOKIE);
         foreach($_FILES as $num => $val){
                 $_FILES[$num]['name']=trim(addslashes($val['name']));
         }
 }

 function escape($arr) {
         if (!is_array($arr)) return addslashes($arr);
         foreach($arr as $num => $val){
                 $val = escape($val);
                 $arr[$num]=$val;
         }
         return $arr;
 }

if (!ini_get("register_globals")) extract($_GET);

include_once $_BHVAR['path_lib']."database.php";
include_once $_BHVAR['path_module']."_system/functions.php";

if (!isset($_type) || !isset($_act)){
	$_type = "P";
	$_act = "home";
}

if (isset($_skin)){
	$_SESSION['skin'] = $_skin;
}else if(!isset($_SESSION['skin'])){
	$_SESSION['skin'] = 1;
}

$_skin = $_SESSION['skin'];

db_conn();
$head = $_BHVAR['path_layout'].get_layout($_skin, 'head');
$foot = $_BHVAR['path_layout'].get_layout($_skin, 'foot');

echo file_get_contents($head);

switch ($_type) {
	case "P" : echo file_get_contents($_BHVAR['path_page']."/".$_act."/_main.php"); break;
	case "M" : include_once $_BHVAR['path_module']."/".$_act."/_main.php"; break;
	default : break;
}

echo file_get_contents($foot);

?>
