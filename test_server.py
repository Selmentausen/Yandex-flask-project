import requests


print(requests.get('http://127.0.0.1:5000/api/books').json())

# print(requests.post('http://127.0.0.1:5000/api/books', json={'title': 'test',
#                                                              'author': 'me',
#                                                              'description': 'good',
#                                                              'content': 'present'}))