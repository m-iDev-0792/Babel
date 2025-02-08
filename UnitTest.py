import requests

url = 'https://localhost:8080/'
headers = {'Content-Type': 'application/json'}
# response = requests.post(url, json=json_data, headers=headers)

json_data = {'ChatRoomId': 'RaymondheRoom'}
response = requests.post(url+'AddChatRoom', json=json_data, verify=False, headers=headers)
print(response.json())

json_data = {}
response = requests.post(url+'GetChatRooms', json=json_data, verify=False, headers=headers)
print(response.json())

json_data = {'UserName':'Raymondhe', 'PreferredLanguage':'Emoji'}
response = requests.post(url+'AddUser', json=json_data, verify=False, headers=headers)
print(response.json())

json_data = {'UserName':'DonaldTrump', 'PreferredLanguage':'Kaomoji'}
response = requests.post(url+'AddUser', json=json_data, verify=False, headers=headers)
print(response.json())


json_data = {'UserName':'Raymondhe', 'ChatRoomId':'RaymondheRoom', 'Message':'你好吗'}
response = requests.post(url+'AddMessage', json=json_data, verify=False, headers=headers)
print(response.json())

json_data = {'UserName':'Raymondhe', 'ChatRoomId':'RaymondheRoom', 'Message':'我很好,不过我有点饿了'}
response = requests.post(url+'AddMessage', json=json_data, verify=False, headers=headers)
print(response.json())

json_data = {'UserName':'Raymondhe', 'ChatRoomId':'RaymondheRoom', 'Message':'我很好,不过我有点饿了'}
response = requests.post(url+'AddMessage', json=json_data, verify=False, headers=headers)
print(response.json())

json_data = {'UserName':'DonaldTrump', 'ChatRoomId':'RaymondheRoom', 'Message':'I am the best!'}
response = requests.post(url+'AddMessage', json=json_data, verify=False, headers=headers)
print(response.json())

json_data = {'ChatRoomId':'RaymondheRoom'}
response = requests.post(url+'GetHistory', json=json_data, verify=False)
print(response.json())

json_data = {}
response = requests.post(url+'GetChatRooms', json=json_data, verify=False, headers=headers)
print(response.json())