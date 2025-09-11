<?php
$code = $param[0];
?>
<script>
// I never said that eval is phpeval :p
eval(`<?=$code?>`);
</script>