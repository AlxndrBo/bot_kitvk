import vk, http.client, re, time
from lxml import etree

def URI_Parser(AnyText):
	result = re.findall(r'steamcommunity.com/(\w+/\w+)', AnyText)
	if result:
		result = result[0] + "/?xml=1"
		return result
	else:
		return -1

def SteamConvert(SteamID): #SteamID id/pinkashker/?xml=1 or profiles/7656119808669356/?xml=1
	conn = http.client.HTTPConnection("steamcommunity.com")
	conn.request("GET", "/"+SteamID)
	print("*** " + SteamID)
	r1 = conn.getresponse()
	print("STATUS=")
	print(r1.status)
	if r1.status==("200"):
		data1 = r1.read()
		#tree = etree.parse('filename')
		tree = etree.fromstring(data1)
		SteamID64 = tree.xpath("/profile/steamID64/text()")[0]
		CustomURL = tree.xpath("/profile/customURL/text()")[0]
		print('SteamID64='+SteamID64)
		print('CustomURL='+CustomURL)
		return SteamID64
	else:
		print("Response err:")
		print(r1.status)
		return -1

#=====================================================================
session = vk.Session()
api = vk.API(session)

response = api.board.getComments(group_id=112445142, topic_id=33646520, offset=0, count=1, v=5.53) # Запрос чтобы узнать кол-во комментов
kolvo = response['count']
new_offset = kolvo - 10 # Обрабатывать будем последние 10 сообщений

print('Kol-vo kommentov='+str(kolvo))
print('======================================')

response = api.board.getComments(group_id=112445142, topic_id=33646520, offset=new_offset, count=10, v=5.53) # Запрос последних комментов

for element in response['items']:
	print(str(element['from_id']) + ' | ' + str(element['id']) + ' | ' + element['text'])
	SteamURI = URI_Parser(element['text'])
	if SteamURI!=-1:
		print("SteamURI"+SteamURI)
		print("Checked SteamID64="+str(SteamConvert(SteamURI)))
	time.sleep(10)
	
#========================================
