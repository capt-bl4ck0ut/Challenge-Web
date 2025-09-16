<?php
declare(strict_types=1);
ini_set('display_errors', '0');

$TMP_DIR = __DIR__ . '/tmp';
$DST_DIR = __DIR__ . '/uploads';
$YARA    = '/usr/bin/yara';
$RULES   = '/var/app/rules/i_dont_like_webshell.yar';

function four_digits(): string {
  return str_pad((string)random_int(0, 9999), 4, '0', STR_PAD_LEFT);
}
function ext_of(string $name): string {
  $e = strtolower(pathinfo($name, PATHINFO_EXTENSION) ?? '');
  return $e ? ".$e" : '';
}
function bad($m,$c=400){ http_response_code($c); echo htmlspecialchars($m,ENT_QUOTES,'UTF-8'); exit; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') bad('POST only',405);
if (!isset($_FILES['file']) || !is_uploaded_file($_FILES['file']['tmp_name'])) bad('no file');

$orig = $_FILES['file']['name'] ?? 'noname';
$ext  = ext_of($orig);
$rand = four_digits();
$tmp_path = $TMP_DIR . '/' . $rand . $ext;

if (!move_uploaded_file($_FILES['file']['tmp_name'], $tmp_path)) bad('save failed',500);
chmod($tmp_path, 0644);

usleep(800 * 1000);

$out = []; $ret = 0;
$cmd = sprintf('%s -m %s %s 2>&1',
  escapeshellarg($YARA),
  escapeshellarg($RULES),
  escapeshellarg($tmp_path)
);
exec($cmd, $out, $ret);

$stdout   = implode("\n", $out);
$ruleName = 'Suspicious_there_is_no_such_text_string_in_the_image';
$hitByName = (strpos($stdout, $ruleName) !== false);

if ($ret === 1 || $hitByName) {
  @unlink($tmp_path);
  echo "Upload scanned: MALWARE detected. File removed.<br><a href=/>back</a>";
  exit;
} elseif ($ret === 0) {
  $dst = $DST_DIR . '/' . basename($tmp_path);
  if (!@rename($tmp_path, $dst)) { @copy($tmp_path, $dst); @unlink($tmp_path); }
  echo "Upload scanned: OK. Moved to <a href=./uploads/" . htmlspecialchars(basename($dst)) . ">View Guide</a>";
  exit;
} else {
  @unlink($tmp_path);
  bad('scan error',500);
}