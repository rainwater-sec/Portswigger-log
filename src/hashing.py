import hashlib
import base64
from pathlib import Path

# パスワードリストを 'username:md5(password)' の形式に変換し、Base64 でエンコードしたペイロードを生成する
ROOT = Path(__file__).resolve().parent.parent
input_file = ROOT / "wordlists" / "passwords.txt"
output_file = ROOT / "wordlists" / "payload.txt"
username = 'carlos'

try:
    with open(input_file, 'r', encoding='utf-8') as f:
        passwords = f.read().splitlines()

    with open(output_file, 'w', encoding='utf-8') as out:
        for password in passwords:
            md5_hash = hashlib.md5(password.encode()).hexdigest()

            raw_str = f'{username}:{md5_hash}'
            encoded_str = base64.b64encode(raw_str.encode()).decode()

            out.write(encoded_str + '\n')

except FileNotFoundError:
    print(f'エラー: {input_file} が見つかりません')
