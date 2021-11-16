import requests
import base64
from urllib.parse import quote, unquote
from tool import getToken,readText,writeText 


def getImage():
	url = './test.png'
	file = open(url,'rb')
	data = base64.b64encode(file.read())
	image = data.decode()
	file.close()
	return image
def getData():
	url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
	headers = {
		'Content-Type': 'application/x-www-from-urlencoded'
	}	
	data = {
		'image': getImage(),
		# 'url': 'C:/Users/zhyl/Desktop/py/test/jpg',
		'language_type':'CHN_ENG'
	}

	_token = readText()
	if not _token:
		_token = getToken()
	url += '?access_token='+_token
	res = requests.post(url,data=data,headers=headers).json()
	item = res.get('words_result');
	for val in item:
		print(val.get('words'))
		print('\n')

if __name__ == "__main__":
	getData()