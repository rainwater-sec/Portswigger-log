# PortSwigger Web Security Academy 学習リポジトリ

PortSwigger Web Security Academy のラボに取り組む過程で作成した、攻撃手法の検証・自動化用スクリプトを整理したリポジトリです。`requests` を中心とした素朴な実装を通じて、認証回りの脆弱性や SQL インジェクションといった代表的な脆弱性の挙動を自分の手で再現することを目的としています。

## ディレクトリ構成

```
.
├── src/                 各ラボで用いた Python スクリプト
├── wordlists/           ユーザー名・パスワード・フィールド名などの辞書ファイル
└── README.md
```

## スクリプト一覧

### 認証・ブルートフォース系
| ファイル | 概要 |
| --- | --- |
| `src/bruteforce_list.py` | パスワードリストを用いた単一ユーザーに対する総当たり |
| `src/bruteforce_number.py` | 4 桁数値 MFA コードの逐次ブルートフォース |
| `src/bruteforce_number_multi.py` | 上記をスレッドプールで並列化した版 |
| `src/bruteforce_number_multi_rev.py` | 並列版に事前リクエスト・早期終了・例外処理を追加した改良版 |
| `src/detect_error_message.py` | ログインフォームのエラーメッセージ差分による有効ユーザー名列挙 |
| `src/response_time.py` | レスポンス時間差を用いたユーザー名列挙（逐次） |
| `src/response_time_rev.py` | 同じく時間差ベースの列挙をマルチスレッド化し閾値判定を導入 |

### SQL インジェクション
| ファイル | 概要 |
| --- | --- |
| `src/binary_search.py` | Blind SQL Injection において二分探索で管理者パスワードを 1 文字ずつ抽出 |

### Web フォーム・CSRF
| ファイル | 概要 |
| --- | --- |
| `src/csrf_check.py` | パスワードリセットフォーム取得時の CSRF トークン確認用の簡易スクリプト |
| `src/search_field.py` | フォームに受け付けられる隠しフィールド名を辞書ベースで列挙 |

### ユーティリティ
| ファイル | 概要 |
| --- | --- |
| `src/hashing.py` | パスワードリストから `username:md5(password)` を Base64 化したペイロードを生成 |
| `src/create_expanded_list.py` | ユーザー名リストを 5 倍に拡張した補助リストを生成 |

## 動作環境

- Python 3.9 以上
- 必要なライブラリ: `requests`, `beautifulsoup4`

```sh
pip install requests beautifulsoup4
```

## 使い方

各スクリプトはリポジトリのルートディレクトリから実行することを想定しています。

```sh
python src/bruteforce_list.py
```

スクリプト内の `URL`・`session` Cookie などの値は対象ラボに合わせて書き換えてください。

## 注意事項

本リポジトリのスクリプトは PortSwigger Web Security Academy が提供する学習用ラボ環境を対象としたものです。許可されていない実環境への利用は行わないでください。
