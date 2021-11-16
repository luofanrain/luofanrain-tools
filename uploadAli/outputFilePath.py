## 批次移动文件
import os, shutil  
import re
import json
  
# 绝对路径  
rootPath = os.getcwd()
dirPath = f"{rootPath}/media3/" 
    
data = []
files = os.listdir(dirPath)
for file in files:
	path = f"{dirPath}{file}"
	item = {
		"filepath":f"{path}/预览视频.mp4",
		"categary": re.sub(r"\d","",file).lower(),
        "title":""
	}

	for name in os.listdir(path):
		items = name.split(".")
		videoName = re.sub("(^\s+)|(\s+$)","",".".join(items[0:-1]))
		item["title"] = videoName		
	data.append(item)
print(json.dumps(data,sort_keys=True,indent=2,ensure_ascii=False))
