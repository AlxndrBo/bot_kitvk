import re

stroka1 = "Musor http://steamcommunity.com/profiles/7656119808669356 musor"
stroka2 = "musor http://steamcommunity.com/id/pinkashker/ musor" 
stroka3 = "musor vsyakaya hrenka master.com/id/mrak musor snova"

result = re.findall(r'steamcommunity.com/(\w+/\w+)', stroka2)
if result:
	result = result[0] + "/?xml=1"
	print(result)

