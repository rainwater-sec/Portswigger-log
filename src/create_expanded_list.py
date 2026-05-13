from pathlib import Path

# ユーザー名リストの各エントリを 5 回ずつ複製した拡張リストを生成する。
# レスポンス時間計測などで同一ユーザー名を複数回試行したい場合の前処理。
ROOT = Path(__file__).resolve().parent.parent
SRC_FILE = ROOT / "wordlists" / "usernames.txt"
DST_FILE = ROOT / "wordlists" / "expanded_list.txt"

with open(SRC_FILE, 'r') as l:
    username = l.read().splitlines()

with open(DST_FILE, 'w') as l:
    for name in username:
        for _ in range(5):
            l.write(name + '\n')

print(f'{DST_FILE} を生成しました')
