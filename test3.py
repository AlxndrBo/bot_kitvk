import http.client
from lxml import etree

conn = http.client.HTTPConnection("steamcommunity.com")
conn.request("GET", "/id/pinkashker/?xml=1")
r1 = conn.getresponse()
data1 = r1.read()

#tree = etree.parse('filename')
tree = etree.fromstring(data1)

SteamID64 = tree.xpath("/profile/steamID64/text()")[0]
CustomURL = tree.xpath("/profile/customURL/text()")[0]
print('SteamID64='+SteamID64)
print('CustomURL='+CustomURL)
