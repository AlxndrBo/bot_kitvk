import vk, http.client, re, time, socket
from lxml import etree



RCON_pwd = input("RCON password: ")
SteamID_list = []
VK_groupID = 112445142
VK_topicID = 33646520
RCON_IP = "192.168.0.4"
RCON_Port = 2022
metod = 1 # Способ добавления SteamID в группу VK в файле permissions
		# 1 - Через Rocket RCON 
		# 2 - Напрямую в файл + RCON p reload | Не реализовано
		# 3x - В файл на веб-сервере при исп. WebPermission плагина. | Не реализовано
			# 31 - Через API сайта | Не реализовано
			# 32 - Напрямую в файл на сервере | Не реализовано

RCON_login_line = "login " + str(RCON_pwd)

			
conn = socket.socket()
conn.connect((RCON_IP, RCON_Port))
conn.send(RCON_login_line + "\n")
time.sleep(1)
conn.send(b"p reload\n")
time.sleep(1)
conn.send(b"p reload\n")
time.sleep(1)
conn.shutdown(2)
time.sleep(1)
conn.close()

sys.exit()
			
			
def URI_Parser(AnyText): # Принимает текст, возвращает ссылку вида /id/customURL/?xml=1 or /profiles/SteamID64/?xml=1
	#result = re.findall(r'steamcommunity.com/(w+/\w+)', AnyText)
	#result = re.findall(r'steamcommunity.com/(id|profiles+/\w+)', AnyText)
	#result = re.findall(r'(steamcommunity.com\/id\/\w+|steamcommunity.com\/profiles\/\w+)', AnyText)
	#result = re.findall(r'steamcommunity.com(\/id\/\w+)|steamcommunity.com(\/profiles\/\w+)', AnyText)
	result = re.findall(r'steamcommunity.com(\/id\/\w+|\/profiles\/\w+)', AnyText)
	if result:
		result = result[0] + "/?xml=1"
		return result
	else:
		return -1

def SteamConvert(SteamID): # Принимает ссылку вида /id/customURL/?xml=1 or /profiles/SteamID64/?xml=1, возвращает чекнутый через стим SteamID64
	conn = http.client.HTTPConnection("steamcommunity.com")
	conn.request("GET", SteamID)
	r1 = conn.getresponse()
	if r1.status==200:
		data1 = r1.read()
		#tree = etree.parse('filename')
		tree = etree.fromstring(data1)
		#print(data1)
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
	
def VK_getCommentsQuantity(VK_gID, VK_tID):
	session = vk.Session()
	api = vk.API(session)
	response = api.board.getComments(group_id=VK_gID, topic_id=VK_tID, offset=0, count=1, v=5.53) # Запрос чтобы узнать кол-во комментов
	kolvo = response['count']
	return kolvo
	
def VK_getComments(VK_gID, VK_tID, nOffset):
	session = vk.Session()
	api = vk.API(session)
	response = api.board.getComments(group_id=VK_gID, topic_id=VK_tID, offset=nOffset, count=10, v=5.53) # Запрос последних комментов
	return response['items']
	
def AddSteamIDtoPermission(ID_list, metod):
	for element in ID_list:
		print(element)
	return 0
	
def AddSteamIDnVKIDtoDB(CheckedSteamID64, VK_UserID):
	return 0

#=====================================================================

new_offset = VK_getCommentsQuantity(VK_groupID, VK_topicID) - 10 # Обрабатывать будем последние 10 сообщений
print('Kol-vo kommentov=', new_offset+10)
print('======================================')
time.sleep(0.5)
response_items = VK_getComments(VK_groupID, VK_topicID, new_offset)
for element in response_items:
	print(str(element['from_id']) + ' | ' + str(element['id']) + ' | ' + element['text'])
	VK_UserID = element['from_id']
	SteamURI = URI_Parser(element['text'])
	if SteamURI!=-1:
		UserInGroup = VK_CheckSignInGroup(VK_UserID, VK_groupID)
		if UserInGroup==1:
			#print("SteamURI"+SteamURI)
			CheckedSteamID64 = SteamConvert(SteamURI)
			if CheckedSteamID64==-1:
				time.sleep(180)
				CheckedSteamID64 = SteamConvert(SteamURI)
				if CheckedSteamID64==-1:
					time.sleep(180)
					CheckedSteamID64 = SteamConvert(SteamURI)
			if CheckedSteamID64!=-1:
				print("Checked SteamID64 = "+str(CheckedSteamID64))
				#Также можно чекнуть, что с этого VKID не добавлялись ранее.
				SteamID_list.append(CheckedSteamID64)
				#AddSteamIDtoPermission(CheckedSteamID64, metod) # Добавить SteamID на игровой сервер 
				#AddSteamIDnVKIDtoDB(CheckedSteamID64, VK_UserID) # Добавить пару SteamID, VKID в файл 
			else:
				print("Neverniy SteamID ili Steam mertv") 
		else:
			print("Ne v gruppe")
		time.sleep(10) # Задержка между запросами к Steam

AddSteamIDtoPermission(SteamID_list, metod)
	
#========================================
