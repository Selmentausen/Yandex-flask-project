import requests


print(requests.get('http://127.0.0.1:5000/api/categories').json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Art & music'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Biographies'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Business'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Comics'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Computers & tech'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Cooking'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Entertainment'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'History'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Horror'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Kids'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Literature'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Mysteries'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Parenting'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Romance'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Sci-Fi'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Fantasy'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Science'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Sports'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'True Crime'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Westerns'}).json())
print(requests.post('http://127.0.0.1:5000/api/categories', data={'name': 'Travel'}).json())
print(requests.get('http://127.0.0.1:5000/api/categories').json())



