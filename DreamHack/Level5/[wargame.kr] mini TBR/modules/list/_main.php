<?php
 die("you have no use for this source.");

 if(!defined('__BHACK__')) exit();
 if (!isset($column) || !isset($word)){
 	$query = "select * from hacked_list order by time desc";
 }else{
 	$column = filtering($column);
 	$word = filtering($word);
	$query = "select * from hacked_list where $column like '%$word%' order by time desc";
 }
 $result = mysql_query($query);

 ?>
<center>
<table id="hacked_list">
	<thead>
		<tr><td>N</td><td>ATTACKER</td><td>URL</td><td>TIME</td></tr>
	</thead>
	<tbody>
	<?php
		while ($row = mysql_fetch_assoc($result)) {
			echo "<tr><td>{$row['idx']}</td><td>{$row['attacker']}</td><td>{$row['url']}</td><td>".date("m-d H:i:s",$row['time'])."</td></tr>";
		}
	?>
	</tbody>
	<tfoot>
		<tr><td colspan="4">
			<form onsubmit="return list_search(this);">
				<select name="sel" value="">
					<option value="idx">NUM</option>
					<option value="url">URL</option>
					<option value="attacker">ATTACKER</option>
				</select>
				<input type="text" name="word" value="" />
				<input type="submit" value="search" />
			</form>
		</td></tr>
	</tfoot>
</table>
</center>
<script>
$(function(){list_init("<?php if(isset($column)) echo $column; ?>","<?php if(isset($word)) echo $word; ?>");});
</script>
