import requests


url = 'https://gt-servicios.com/propld/listsapi/searchlist'
headers = {
        'Accept': 'application/json',
        # 'X-API-KEY':'KYC-DSR92Sj2NgK8aPyPHXYSxjDs'
        'X-API-KEY': 'KYC-eWTR92Sj2NgK8aPyPHXYSxjVr'
}

data = {
    'id_entidad': 5500,
    'mothers_last_name': 'Cueto',
    'last_name': 'Moreno',
    'name': 'Marcela',
}

r = requests.post(url, data=data, headers=headers)
print(r.content)
print(r.text)
print(r.request)
print(r.json)
