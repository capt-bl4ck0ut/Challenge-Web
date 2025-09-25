rule Suspicious_there_is_no_such_text_string_in_the_image
{
  meta:
    description = "Broader PHP webshell heuristics for CTF (fast, no backtick regex)"
    severity = "high"
  
  strings:
    $php_any     = /<\?(php|=)?/ nocase
    $php_script  = "<script language=\"php\">" nocase

    $eval1     = "eval" nocase
    $assert1   = "assert" nocase
    $system1   = "system" nocase
    $exec1     = "exec" nocase
    $shexec1   = "shell_exec" nocase
    $passthru1 = "passthru" nocase
    $popen1    = "popen" nocase
    $procopen1 = "proc_open" nocase

    $cmd1      = "cmd" nocase
    $cmd2      = "command" nocase

    $cuf       = "call_user_func(" nocase
    $cufa      = "call_user_func_array(" nocase
    $reflf     = "ReflectionFunction" nocase
    $crefunc   = "create_function(" nocase
    $preg_e    = /preg_replace\s*\(\s*[^,]*['"][^'"]*e['"]/ nocase

    // wrappers & inputs
    $php_input   = "php://input" nocase
    $php_filter  = "php://filter" nocase
    $phar        = "phar://" nocase
    $zipwrap     = "zip://" nocase
    $superglobal = /\$_(GET|POST|REQUEST|COOKIE|FILES|SERVER)\s*\[/ nocase

    // short code
    $short_bt_post   = "<?=`$_POST[" nocase
    $short_bt_get    = "<?=`$_GET[" nocase
    $short_bt_req    = "<?=`$_REQUEST[" nocase
    $short_bt_cookie = "<?=`$_COOKIE[" nocase

    // obfuscators
    $base64    = "base64_decode(" nocase
    $rot13     = "str_rot13(" nocase
    $inflate   = "gzinflate(" nocase
    $gzuncomp  = "gzuncompress(" nocase
    $hex2bin   = "hex2bin(" nocase
    $urldec    = "urldecode(" nocase
    $rawurl    = "rawurldecode(" nocase
    $strrev    = "strrev(" nocase

    // re
    $assign_func = /\$[A-Za-z_]\w*\s*=\s*["'](system|exec|shell_exec|passthru|popen|proc_open)["']/ nocase
    $assign_concat_system = /\$[A-Za-z_]\w*\s*=\s*["']sys["']\s*\.\s*["']tem["']/ nocase
    $var_call_super = /\$[A-Za-z_]\w*\s*\(\s*\$_(GET|POST|REQUEST|COOKIE)\s*\[/ nocase
    $assign_concat_multi = /\$[A-Za-z_]\w*\s*=\s*\$[A-Za-z_]\w*\s*\.\s*["'](tem|xec|shell_exec)["']/ nocase
    $assign_concat_more = /\$[A-Za-z_]\w*\s*=\s*(\$[A-Za-z_]\w*|\s*["']s["']\s*\.\s*["']ys["'])\s*\.\s*["']tem["']/ nocase


  condition:
    ( $php_any or $php_script )
    or
    ( 1 of ( $eval1, $assert1, $system1, $exec1, $shexec1, $passthru1, $popen1, $procopen1,
             $cuf, $cufa, $reflf, $crefunc, $preg_e, $cmd1, $cmd2,
             $short_bt_post, $short_bt_get, $short_bt_req, $short_bt_cookie)
      or ( $assign_func and $var_call_super )
      or ( $assign_concat_system and $var_call_super )
      or ( $assign_concat_multi )
      or ( $assign_concat_more )
    )
    and
    ( 1 of ( $base64, $rot13, $inflate, $gzuncomp, $hex2bin, $urldec, $rawurl, $strrev,
             $php_input, $php_filter, $phar, $zipwrap, $superglobal ) )
}
