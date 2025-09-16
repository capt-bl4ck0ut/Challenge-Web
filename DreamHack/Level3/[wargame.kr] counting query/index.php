<?php
 if (isset($_GET['view-source'])) {
     show_source(__FILE__);
     exit();
 }
 include("./inc.php"); // database connect, $FLAG.
 ini_set('display_errors',false);

 function err($str){ die("<script>alert(\"$str\");window.location.href='./';</script>"); }
 function uniq($data){ return md5($data.uniqid());}
 function make_id($id){ return mysql_query("insert into all_user_accounts values (null,'$id','".uniq($id)."','guest@nothing.null',2)");}
 function counting($id){ return mysql_query("insert into login_count values (null,'$id','".time()."')");}
 function pw_change($id) { return mysql_query("update all_user_accounts set ps='".uniq($id)."' where user_id='$id'"); }
 function count_init($id) { return mysql_query("delete from login_count where id='$id'"); }
 function t_table($id) { return mysql_query("create temporary table t_user as select * from all_user_accounts where user_id='$id'"); };

 if(empty($_POST['id']) || empty($_POST['pw']) || empty($_POST['type'])){
  err("Parameter Error :: missing");
 }

 $id=mysql_real_escape_string($_POST['id']);
 $ps=mysql_real_escape_string($_POST['pw']);
 $type=mysql_real_escape_string($_POST['type']);
 $ip=$_SERVER['REMOTE_ADDR'];

 sleep(2); // not Bruteforcing!!

 if($id!=$ip){
  err("SECURITY : u can access with allotted id only");
 }

 $row=mysql_fetch_array(mysql_query("select 1 from all_user_accounts where user_id='$id'"));
 if($row[0]!=1){
  if(false === make_id($id)){
   err("DB Error :: create user error");
  }
 }
 
 $row=mysql_fetch_array(mysql_query("select count(*) from login_count where id='$id'"));
 $log_count = (int)$row[0];
 if($log_count >= 4){
  pw_change($id);
  count_init($id);
  err("SECURITY : bruteforcing detected - password is changed");
 }
 
 t_table($id); // don`t access the other account

 if(preg_match("/all_user_accounts/i",$type)){
  err("SECURITY : don`t access the other account");
 }

 counting($id); // limiting number of query

 if(false === $result=mysql_query("select * from t_user where user_id='$id' and ps='$ps' and type=$type")){
  err("DB Error :: ".mysql_error());
 }

 $row=mysql_fetch_array($result);
 
 if(empty($row['user_id'])){
  err("Login Error :: not found your `user_id` or `password`");
 }

 echo "welcome <b>$id</b> !! (Login count = $log_count)";
 
 $row=mysql_fetch_array(mysql_query("select ps from t_user where user_id='$id' and ps='$ps'"));

 //patched 04.22.2015
 if (empty($ps)) err("DB Error :: data not found..");

 if($row['ps']==$ps){ echo "<h2>wow! FLAG is : ".$FLAG."</h2>"; }

?>