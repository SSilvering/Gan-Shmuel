import requests

res = requests.post('http://127.0.0.1:5000/truck', params={'provider_name': 'tomer', 'truck_id': '1571'})

print(res.text)
