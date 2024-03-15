import requests   #pip install

url = 'http://localhost:8087/add'
data = {'a': 5, 'b': 12}

response = requests.post(url, json=data)

if response.status_code == 200:
    result = response.json()['result']
    print(f'The sum of 5 and 12 is: {result}')
else:
    print('Error: Unable to get the result.')