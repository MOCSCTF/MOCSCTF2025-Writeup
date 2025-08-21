<?php
highlight_file(__FILE__);
$autoloaderPath = __DIR__ . '/vendor/autoload.php';
require $autoloaderPath;

unserialize((base64_decode($_POST['data'])));