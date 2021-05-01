import os
import requests


print(requests.get('http://127.0.0.1:5000/api/category').json())
print(requests.post('http://127.0.0.1:5000/api/category', data={'name': 'Детектив'}).json())
print(requests.post('http://127.0.0.1:5000/api/category', data={'name': 'История'}).json())
print(requests.post('http://127.0.0.1:5000/api/category', data={'name': 'Фантастика'}).json())
print(requests.post('http://127.0.0.1:5000/api/category', data={'name': 'Триллер'}).json())
print(requests.post('http://127.0.0.1:5000/api/category', data={'name': 'Другое'}).json())
print(requests.get('http://127.0.0.1:5000/api/category').json())



