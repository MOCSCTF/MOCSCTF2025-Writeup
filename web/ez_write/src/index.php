<?php
highlight_file(__FILE__);
$filename = $_POST['refiles'] ?? [];
$filename = preg_replace('/[";()`]/', '', $filename);
$tempfile = 'tmp/'.bin2hex(random_bytes(8)).'.php';
file_put_contents($tempfile, "<?php\n\$files = \"$filename\";\n?>");
echo 'file stored in '.$tempfile;