import requests
import json

data = {}
data['username'] = 'test'
data['password'] = '12345678'
data = json.dumps(data)
token = requests.post('http://127.0.0.1:8000/api/token-auth/', data,
    headers={'accept': '*/*', 'Content-Type': 'application/json'})
print(token)
token = token.content.decode('utf-8')
token = json.loads(token)
print(token)


data = {}
data['nip'] = '123456'
data['date_from'] = "2020-7-25"
data['data_to'] = "2020-8-25"
data = json.dumps(data)
result = requests.post('https://staging.inguz.site/api/cuenta/',
    data, headers={'accept': '*/*', 'Content-Type': 'application/json',
        'Authorization': token['token']})
print(result)
result = result.content.decode('utf-8')
result = json.loads(result)
print(result)

# data = {}
# data['nip'] = '123456'
# data['month']= "6"
# data['year']= "2020"
# data = json.dumps(data)
# result = requests.post('http://127.0.0.1:8000/api/cuenta/',
#   data, headers={'accept': '*/*', 'Content-Type': 'application/json',
#       'Authorization': 'Token ' + token['token']})
# print(result)
# result = result.content.decode('utf-8')
# result = json.loads(result)
# print(result)
