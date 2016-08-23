import vk
session = vk.Session()
api = vk.API(session)
#response = api.users.get(user_ids=1, version=5.53)
#print(response)

response = api.board.getComments(group_id=112445142, topic_id=33646520, offset=0, count=1, v=5.53)
kolvo = response['count']
new_offset = kolvo - 10

print('Kol-vo kommentov='+str(kolvo))
print('======================================')


response = api.board.getComments(group_id=112445142, topic_id=33646520, offset=new_offset, count=10, v=5.53)

#print(response['items'][0]['text'])
#print(response['items'][1]['text'])
#print(response['items'][2]['text'])
#print('======================================')

for element in response['items']:
#	d_text = element['text'].decode("utf-8")
	print(str(element['from_id']) + ' | ' + str(element['id']) + ' | ' + element['text'])

