<?php
function generate_uuid_v4() {
    $data = random_bytes(16);

    $data[6] = chr(ord($data[6]) & 0x0f | 0x40);
    $data[8] = chr(ord($data[8]) & 0x3f | 0x80);

    return vsprintf('%s%s-%s-%s-%s-%s%s%s', str_split(bin2hex($data), 4));
}

error_reporting(0);
ini_set('display_errors', 0);

$flag = file_get_contents('/flag.txt');
session_start();

$usernameAdmin = 'admin';
$passwordAdmin = generate_uuid_v4();

$entropy = "My-password-is-super-secure-that-You'd-never-guess-it-Hia-hiahia";

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    $hash = password_hash($usernameAdmin . $entropy . $passwordAdmin, PASSWORD_BCRYPT);

    if ($usernameAdmin === $username && password_verify($username . $entropy . $password, $hash)) {
        $_SESSION['logged_in'] = true;
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background: linear-gradient(135deg, #6e7cfc, #3a4fdb);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            color: #fff;
            overflow: hidden;
        }

        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 40px 50px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            width: 100%;
            max-width: 400px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        h2 {
            text-align: center;
            color: #fff;
            margin-bottom: 20px;
            font-weight: bold;
            font-size: 24px;
        }

        label {
            font-size: 16px;
            color: #fff;
            margin-bottom: 5px;
            display: block;
        }

        input {
            width: 100%;
            padding: 15px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            background-color: #f7f9fc;
            color: #333;
            transition: all 0.3s ease;
        }

        input:focus {
            border-color: #4e73df;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(78, 115, 223, 0.3);
        }

        button {
            width: 100%;
            padding: 15px;
            background-color: #4e73df;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        button:hover {
            background-color: #375a8f;
            transform: translateY(-2px);
        }

        .flag-message {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: #4CAF50;
            background-color: rgba(76, 175, 80, 0.2);
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        .login-form {
            display: flex;
            flex-direction: column;
        }

        .login-form input {
            margin-bottom: 15px;
        }
    </style>
</head>
<body>

<div class="container">
    <?php if (isset($_SESSION['logged_in']) && $_SESSION['logged_in'] === true): ?>
        <div class="flag-message"><?php echo $flag; ?></div>
    <?php else: ?>
        <h2>Login</h2>
        <form method="POST" class="login-form">
            <label for="username">Username:</label>
            <input type="text" name="username" id="username" required>

            <label for="password">Password:</label>
            <input type="password" name="password" id="password" required>

            <button type="submit">Login</button>
        </form>
    <?php endif; ?>
</div>

</body>
</html>