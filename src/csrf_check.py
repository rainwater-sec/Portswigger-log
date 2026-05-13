import requests
from bs4 import BeautifulSoup

# パスワードリセット画面に含まれる CSRF トークンの入力欄を確認するための簡易スクリプト
url = 'https://0a6c00780439b6d9825d3d7d008f008b.web-security-academy.net/forgot-password'
session = requests.Session()

res = session.get(url)
print(res.text)  # 取得した HTML を出力して内容を確認する
