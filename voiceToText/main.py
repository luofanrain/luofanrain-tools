import requests
import json
import base64
from urllib.parse import quote, unquote
from tool import getToken,readText,writeText

def getVideo():
    url = './test.wav'
    file = open(url,'rb')
    bitfile = file.read()
    data = base64.b64encode(bitfile)
    video = data.decode()
    file.close()
    return [video,len(bitfile)]
def getData():
    url = 'http://vop.baidu.com/server_api'
    headers = {
        'Content-Type': 'application/json'
    }   
    _token = readText()
    if not _token:
        _token = getToken()
    [speech,bitlen] = getVideo()
    data = {
        'format' : 'wav',
        'rate'   : 16000,
        'channel': 1,
        'dev_pid' : 1536,
        'cuid'   : '962464269426981549426366424269426989423494',
        'token'  : _token,
        'speech' : speech,
        'len'    : bitlen 
    }
    res = requests.post(url,json=data,headers=headers).json()
    item = res.get('words_result');
    for val in item:
        print(val.get('words'))
        print('\n')

if __name__ == "__main__":
	getData()