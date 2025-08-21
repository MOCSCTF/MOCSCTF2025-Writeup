<?php
highlight_file(__FILE__);

if (isset($_GET['MOCSCTF2025'])) {
    $code = $_GET['MOCSCTF2025'];

    if(!preg_match("/[a-zA-Z0-9@#%^&*:{}\-<\?>\"|`~\\\\]/",$code)){

        eval($code);
    }
    else{
        die('hacker！！你想幹嘛！！！');
    }
}




