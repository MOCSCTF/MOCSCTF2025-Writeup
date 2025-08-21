<?php
$Secret_key = "Fidy66rEB65mnE5UbPyEsgMxmmhdNebU";

function checkSignature($signature)
{
    try {
        $decoded = base64_decode($signature, true);
        if ($decoded === false) {
            throw new Exception("Invalid base64 encoding");
        }
        global $Secret_key;
        return $decoded === $Secret_key;
    } catch (Exception $e) {
        echo $e->getMessage() . PHP_EOL;
    }
}

function verifySignature($headers)
{
    if (!isset($headers['X-Signature'])) {
        return false;
    }
    $validSignature = $headers['X-Signature'];
    if (checkSignature($validSignature) === false) {
        return false;
    }
    return true;
}

if (!verifySignature(getallheaders())) {
    http_response_code(403);
?>
    <div style="
        margin: 50px auto;
        padding: 20px;
        max-width: 600px;
        background-color: #ffe6e6;
        color: #a94442;
        border: 1px solid #f5c6cb;
        border-left: 5px solid #d9534f;
        border-radius: 8px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        ">
        <h2>⚠️ 签名验证失败</h2>
        <p>您的请求未通过验证，可能存在伪造行为或签名错误。</p>
    </div>
<?php
    exit;
}

function base64url_encode($data)
{
    return rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
}

function encrypt($data, $key)
{
    $method = 'AES-256-CBC';
    $iv = openssl_random_pseudo_bytes(16);
    $encrypted = openssl_encrypt($data, $method, $key, OPENSSL_RAW_DATA, $iv);
    return base64url_encode($iv . $encrypted);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $function = $_POST['function'] ?? '';

    $protocol = isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? 'https' : 'http';
    $host = $_SERVER['SERVER_ADDR'];
    $baseUrl = $protocol . '://' . $host;

    $data = '';
    if ($function === 'A') {
        $command = 'date';
        $data = bin2hex('A' . pack('n', strlen($command)) . $command);
    } elseif ($function === 'B') {
        $date = $_POST['date'] ?? '';
        $command = $date;
        $data = bin2hex('B' . pack('n', strlen($command)) . $command);
    } elseif ($function === 'C') {
        $weekdate = $_POST['weekdate'] ?? '';
        $timestamp = strtotime($weekdate);
        if ($timestamp === false) {
            $result = '<div class="result"><h3>执行结果：</h3><pre>无效的日期格式</pre></div>';
        } else {
            $monday = strtotime('last monday', $timestamp);
            if (date('N', $timestamp) == 1) $monday = $timestamp;
            $combined = '';
            for ($i = 0; $i < 7; $i++) {
                $day = date('Y-m-d', strtotime("+$i day", $monday));
                $command = $day;
                $combined .= 'B' . pack('n', strlen($command)) . $command;
            }
            $data = bin2hex($combined);
        }
    }

    if (!empty($data)) {
        $encryptedSource = encrypt('index.php', $Secret_key);
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $baseUrl . '/execute.php');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'X-Source: ' . $encryptedSource,
            'Content-Type: application/octet-stream'
        ]);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, hex2bin($data));
        curl_setopt($ch, CURLOPT_TIMEOUT, 5);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 2);

        $response = curl_exec($ch);
        $error = curl_error($ch);
        curl_close($ch);

        $result = $error
            ? '<div class="result"><h3>执行结果：</h3><pre>请求失败: ' . htmlspecialchars($error) . '</pre></div>'
            : '<div class="result"><h3>执行结果：</h3><pre>' . $response . '</pre></div>';
    }
}
?>
<!DOCTYPE html>
<html>

<head>
    <title>功能选择</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }

        .container {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .function {
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 5px;
        }

        input[type="text"] {
            padding: 8px;
            margin: 5px 0;
            width: 200px;
        }

        button {
            padding: 8px 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }

        .result {
            margin-top: 20px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>功能选择</h1>

        <div class="function">
            <h2>当前系统时间</h2>
            <form method="post">
                <input type="hidden" name="function" value="A">
                <button type="submit">执行</button>
            </form>
        </div>

        <div class="function">
            <h2>解析指定日期</h2>
            <form method="post" onsubmit="return validateDate(this.date.value);">
                <input type="hidden" name="function" value="B">
                <input type="text" name="date" placeholder="输入日期 (YYYY-MM-DD)" required pattern="\d{4}-\d{2}-\d{2}">
                <button type="submit">执行</button>
            </form>
        </div>

        <div class="function">
            <h2>解析某日期所在周的每天</h2>
            <form method="post" onsubmit="return validateDate(this.weekdate.value);">
                <input type="hidden" name="function" value="C">
                <input type="text" name="weekdate" placeholder="输入日期 (YYYY-MM-DD)" required pattern="\d{4}-\d{2}-\d{2}">
                <button type="submit">执行</button>
            </form>
        </div>

        <script>
            function validateDate(dateStr) {
                const regex = /^\d{4}-\d{2}-\d{2}$/;
                if (!regex.test(dateStr)) {
                    alert("请输入正确的日期格式：YYYY-MM-DD");
                    return false;
                }
                return true;
            }
        </script>

        <?php if (isset($result)): ?>
            <?php echo $result; ?>
        <?php endif; ?>
    </div>
</body>

</html>