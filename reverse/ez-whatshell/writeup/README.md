## flag

MOCSCTF{Th15_15_@n_Ez_p0wer5hell_plu5_b@5h5hell}

## 解題步驟

用hex編輯器查看附件會發現很多亂碼，但開頭是`#!/bin/sh`説明是這是一個bashshell腳本

bash語言有個特性是反引號`可以作為混淆插入到很多linux命令中，例如如下指令仍然會執行打印Hello，但同時也會去找aa命令

```bash
ec`aa`ho "Hello"
```

因此開頭有個`exec 2>/dev/null`直接把stderr錯誤輸出重定向到丟棄，所以不會報錯

可以編寫腳本去除反引號中間的內容，也可以hex編輯器直接手動去除

去除完基本代碼如下

```bash
#!/bin/sh
exec 2>/dev/null
export _1="xxxxx";
echo "xxxx" | perl -pe 's/[^[:print:]]/\\n/g'| openssl base64 -d | pwsh -NoProfile -NonInteractive -Command -
```

其中兩個字符串還是夾雜了大量亂碼字符

分析最後一行代碼可知對echo後面的字符串做了如下操作：

* perl過濾掉不可打印字符，但保留了換行符
* openssl進行base64解密
* pwsh進入linux下的powershell，需要提前安裝否則無法執行命令，可以參考[微軟官網](https://learn.microsoft.com/zh-cn/powershell/scripting/install/installing-powershell-on-linux?view=powershell-7.5)

因此可知最終執行的是powershell代碼，可以通過去除`| pwsh -NoProfile -NonInteractive -Command -`直接看base64解密完的代碼

```powershell
function 0oO0oO0oO0oO0oO0
{
    000ooo0o0ooo000o
    $O0o0OO0ooO000ooo = o0oo0o0o0o0O0oOO
    O00oo0ooOO0oO0oo($O0o0OO0ooO000ooo)
    exit
}

function 0ooo0ooo0oooOOOO() 
{
    if (-NoT (& cat ("/???" + "/" + $gLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[60] + $GlOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[49] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[51] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[56] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[57] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[61] + $GLoBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[53] + "-id") 2>$null)) {exit}
}

function 000ooo0o0ooo000o
{
    $o0O0O0O0OO0O0O0O0OO0O0O0O0O = (-JoIn ((&(Get-Command /???/cat) /?tc/*get*).tOChArARray() | SOrT-ObjECt | sELecT-oBjecT -unIquE))
    $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O = $o0O0O0O0OO0O0O0O0OO0O0O0O0O
    0ooo0ooo0oooOOOO
}

function o0oo0o0o0o0O0oOO
{
    $000OoOOO00OO0ooO = $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[12] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[53] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[67] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[51] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[12] + $GLOBaL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[60] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[49] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[51] + $GLoBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[56] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[57] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[61] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[53] + "-id"
    if (-nOT (&($GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[50] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[49] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[66] + $GlOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[53] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[18] + [char]([int]$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[16]+1)) $000OoOOO00OO0ooO 2>$null).Trim() -eq ($GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[41] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[44] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[29] + [cHar]0x6A + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[46] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[44] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[19] + $GLOBAl:O0O0O0O0OO0O0O0O0OO0O0O0O0O[22])) { return $null }
    return cat $000OoOOO00OO0ooO 
}

function O00oo0ooOO0oO0oo 
{ 
    param([string]$kEY) # oh?!
    $_1 = $env:_1
    $o0o0oo0oo0oooo0o = & {eChO $_1 | &($GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[63] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[53] + $GLoBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[65] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[59]) ($GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[10] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[63] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[53]) ($GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[66] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[12] + [char]([int]$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[46]+2) + [char]([int]$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[46]+5) + [char]([int]$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[46]+2) + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[20] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[63] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[65] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[57] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[61] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[67] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[20] + [Char]([int]$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[46]+4) + [char]([int]$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[46]+4) + $GlOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[12] + [char]([int]$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[46]+3) + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[61] + $GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[12] + $GLObAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[55]) | &($GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[62]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[63]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[53]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[61]+$gLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[66]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[66]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[59]) ($GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[53]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[61]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[51]) ($GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[10]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[52]) ($GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[10]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[49]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[53]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[66]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[10]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[15]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[17]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[18]+$gLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[10]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[51]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[50]+$GLObAl:O0O0O0O0OO0O0O0O0OO0O0O0O0O[51]) ($GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[10]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[58]) $kEY ($GLoBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[10]+$GLOBAL:O0O0O0O0OO0O0O0O0OO0O0O0O0O[49]) 2>$null}
    if ($LASTEXITCODE -ne 0) {
        WrITe-HOsT "解密失敗，繼續努力" -ForegroundColor Red
    }
    else {
        wRitE-hoSt "太強了，flag是" $o0o0oo0oo0oooo0o
    }
}

0oO0oO0oO0oO0oO0

```

有混淆大概分析下還原為如下代碼

```powershell
function main 
{
    gen_charset_and_check
    key = verify_key
    openssl_dec(key)
    exit
}

function check_environment() 
{
    if (-NoT (& cat ("/???" + "/" + $GLOBAL:charset[60] + $GLOBAL:charset[49] + $GLOBAL:charset[51] + $GLOBAL:charset[56] + $GLOBAL:charset[57] + $GLOBAL:charset[61] + $GLOBAL:charset[53] + "-id") 2>$null)) {exit}
}

function gen_charset_and_check
{
    $tmp_charset = (-join ((&(Get-Command /???/cat) /?tc/*get*).tochararray() | sort-object | select-object -unique))
    $Global:charset = $tmp_charset
    check_environment
}

function verify_key
{
    $path = $GLOBAL:charset[12] + $GLOBAL:charset[53] + $GLOBAL:charset[67] + $GLOBAL:charset[51] + $GLOBAL:charset[12] + $GLOBaL:charset[60] + $GLOBAL:charset[49] + $GLOBAL:charset[51] + $GLoBAL:charset[56] + $GLOBAL:charset[57] + $GLOBAL:charset[61] + $GLOBAL:charset[53] + "-id"
    if (-nOT (&($GLOBAL:charset[50] + $GLOBAL:charset[49] + $GLOBAL:charset[66] + $GlOBAL:charset[53] + $GLOBAL:charset[18] + [char]([int]$GLOBAL:charset[16]+1)) $path 2>$null).Trim() -eq ($GLOBAL:charset[41] + $GLOBAL:charset[44] + $GLOBAL:charset[29] + [cHar]0x6A + $GLOBAL:charset[46] + $GLOBAL:charset[44] + $GLOBAL:charset[19] + $GLOBAl:charset[22])) { return $null }
    return cat $path 
}

function openssl_dec 
{ 
    param([string]$key) 
    $_1 = $env:_1
    $plaintext = & {eChO $_1 | &($GLOBAL:charset[63] + $GLOBAL:charset[53] + $GLoBAL:charset[65] + $GLOBAL:charset[59]) ($GLOBAL:charset[10] + $GLOBAL:charset[63] + $GLOBAL:charset[53]) ($GLOBAL:charset[66] + $GLOBAL:charset[12] + [char]([int]$GLOBAL:charset[46]+2) + [char]([int]$GLOBAL:charset[46]+5) + [char]([int]$GLOBAL:charset[46]+2) + $GLOBAL:charset[20] + $GLOBAL:charset[63] + $GLOBAL:charset[65] + $GLOBAL:charset[57] + $GLOBAL:charset[61] + $GLOBAL:charset[67] + $GLOBAL:charset[20] + [Char]([int]$GLOBAL:charset[46]+4) + [char]([int]$GLOBAL:charset[46]+4) + $GlOBAL:charset[12] + [char]([int]$GLOBAL:charset[46]+3) + $GLOBAL:charset[61] + $GLOBAL:charset[12] + $GLObAL:charset[55]) | &($GLOBAL:charset[62]+$GLOBAL:charset[63]+$GLOBAL:charset[53]+$GLOBAL:charset[61]+$gLOBAL:charset[66]+$GLOBAL:charset[66]+$GLOBAL:charset[59]) ($GLOBAL:charset[53]+$GLOBAL:charset[61]+$GLOBAL:charset[51]) ($GLOBAL:charset[10]+$GLOBAL:charset[52]) ($GLOBAL:charset[10]+$GLOBAL:charset[49]+$GLOBAL:charset[53]+$GLOBAL:charset[66]+$GLOBAL:charset[10]+$GLOBAL:charset[15]+$GLOBAL:charset[17]+$GLOBAL:charset[18]+$gLOBAL:charset[10]+$GLOBAL:charset[51]+$GLOBAL:charset[50]+$GLObAl:charset[51]) ($GLOBAL:charset[10]+$GLOBAL:charset[58]) $kEY ($GLoBAL:charset[10]+$GLOBAL:charset[49]) 2>$null}
    if ($LASTEXITCODE -ne 0) {
        WrITe-HOsT "解密失敗，繼續努力" -ForegroundColor Red
    }
    else {
        wRitE-hoSt "太強了，flag是" $plaintext
    }
    // echo $_1 | perl -pe 's/[^[:print:]]//g' | openssl enc -d -aes-256-cbc -k $key -a
}

main

```

首先main通過gen_charset_and_check生成符號表，分析可知讀取了/etc/wgetrc裏的內容，然後排序並選出單獨的

```powershell
$tmp_charset = (-join ((&(Get-Command /???/cat) /?tc/*get*).tochararray() | sort-object | select-object -unique))
```

可以直接在pwsh環境中運行查看可知charset值為

```
 !"#$'()*,-./0123568:<=>@ABCEFGHIKLMNOPRSTUVWXY_`abcdefghiklmnopqrstuvwxyz~
```

然後根據值去還原每個命令

* check_environment檢查了`/etc/machine-id`是否為空，為空直接退出
* verify_key讀取`/etc/machine-id`並base64加密，和`TWFjYW8=`比較，解密可知`/etc/machine-id`需要為`Macao`
* openssl_dec傳入key，執行了`echo $_1 | perl -pe 's/[^[:print:]]//g' | openssl enc -d -aes-256-cbc -k $key -a`，其中`$_1`已在bash腳本傳入到環境變量中，然後同樣對亂碼字符串perl篩選掉非ascii可打印字符，獲取base64字符串然後openssl aes解密，密鑰就是`Macao`

所以正確做法可以直接將/etc/machine-id改為`Macao`，跑腳本即可打印flag `MOCSCTF{Th15_15_@n_Ez_p0wer5hell_plu5_b@5h5hell}`

```bash
sudo cp /etc/machine-id /etc/machine-id.bak
echo -n "Macao" | sudo tee /etc/machine-id 
./wh@t_1s_th1s 
太強了，flag是 MOCSCTF{Th15_15_@n_Ez_p0wer5hell_plu5_b@5h5hell}
sudo cp /etc/machine-id.bak /etc/machine-id 
```

