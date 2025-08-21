<?php

if (!isset($_SERVER['HTTP_REFERER']) || strpos($_SERVER['HTTP_REFERER'], 'rce.php') === false) {
    http_response_code(403);
    die('Forbidden');
}

highlight_file('rce.php');
