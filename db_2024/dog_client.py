import requests


dog_id = 4
url = f'http://localhost:8081/dogs/{dog_id}'

res = requests.get(url)
print(res.json())