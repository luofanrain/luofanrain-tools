import requests
import json
global appkey
global secretkey
appkey = 'GHrzWKkartnFnFsXKSlnGwgP'
secretkey = 'VkpGkGjCtrzRe6vGFl498mfChHW4Vfb2'
def getToken():
    tokenUrl = 'https://openapi.baidu.com/oauth/2.0/token'
    data = {
        'grant_type':'client_credentials',
        'client_id':appkey,
        'client_secret':secretkey
    }
    res = requests.post(tokenUrl,data).json()
    if res.get('access_token'):
        writeText(res)
    return res.get('access_token')
def writeText(data):
	file = open('token.txt','w+')
	file.write(json.dumps(data))
	file.close()
def readText():
	file = open('token.txt','a+')
	text = file.read()
	file.close()
	if text:
		_data = json.loads(text)
		return _data.get('access_token')
	return text