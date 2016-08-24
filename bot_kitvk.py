import vk, http.client, re, time
from lxml import etree

def URI_Parser(AnyText): # Принимает текст, возвращает ссылку вида id/customURL/?xml=1 or profiles/SteamID64/?xml=1
	result = re.findall(r'steamcommunity.com/(\w+/\w+)', AnyText)
	if result:
		result = result[0] + "/?xml=1"
		return result
	else:
		return -1

def SteamConvert(SteamID): # Принимает ссылку вида id/customURL/?xml=1 or profiles/SteamID64/?xml=1, возвращает чекнутый через стим SteamID64
	conn = http.client.HTTPConnection("steamcommunity.com")
	conn.request("GET", "/"+SteamID)
	#print("*** " + SteamID)
	r1 = conn.getresponse()
	if r1.status==200:
		data1 = r1.read()
		#tree = etree.parse('filename')
		tree = etree.fromstring(data1)
		SteamID64 = tree.xpath("/profile/steamID64/text()")[0]
		#CustomURL = tree.xpath("/profile/customURL/text()")[0]
		#print('SteamID64='+SteamID64)
		#print('CustomURL='+CustomURL)
		return SteamID64
	else:
		print("Response err:")
		print(r1.status)
		return -1

def VK_CheckSignInGroup(VK_uID, VK_groupID): # Получает VK user ID, проверяет на вхождение в группу. Возвращает 1 при вхождении, 0 при отсутствии, -1 при ошибке
	session = vk.Session()
	api = vk.API(session)
	response = api.groups.isMember(group_id=VK_groupID, user_id=VK_uID, v=5.53)
	if response==0 or response==1:
		return response
	else:
		return -1 # какая-то хрень. Ошибка. ХЗ, как получать коды ошибок от вконтактика
	
def VK_getCommentsQuantity(VK_groupID, VK_topicID):
	session = vk.Session()
	api = vk.API(session)
	response = api.board.getComments(group_id=112445142, topic_id=33646520, offset=0, count=1, v=5.53) # Запрос чтобы узнать кол-во комментов
	kolvo = response['count']
	return kolvo

#=====================================================================

new_offset = VK_getCommentsQuantity(VK_groupID, VK_topicID): - 10 # Обрабатывать будем последние 10 сообщений
print('Kol-vo kommentov='+str(kolvo))
print('======================================')
time.pause(0.5)
response = api.board.getComments(group_id=112445142, topic_id=33646520, offset=new_offset, count=10, v=5.53) # Запрос последних комментов

for element in response['items']:
	print(str(element['from_id']) + ' | ' + str(element['id']) + ' | ' + element['text'])
	VK_UserID = element['from_id']
	UserInGroup = VK_CheckSignInGroup(VK_UserID)
	
	
	SteamURI = URI_Parser(element['text'])
	if SteamURI!=-1:
		#print("SteamURI"+SteamURI)
		CheckedSteamID64 = SteamConvert(SteamURI)
		if CheckedSteamID64==-1:
			time.sleep(180)
			CheckedSteamID64 = SteamConvert(SteamURI)
			if CheckedSteamID64==-1:
				time.sleep(180)
				CheckedSteamID64 = SteamConvert(SteamURI)
		# 
		print("Checked SteamID64 = "+str(CheckedSteamID64))
	time.sleep(10) # Задержка между запросами к Steam
	
#========================================
