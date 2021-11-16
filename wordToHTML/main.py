import zipfile
import json
import xmltodict
import re
import os
import numpy as np
from win32com import client as winC
import time

# jsonFile = open("xmlJSON.json","w+")
# xmlContent = json.dumps(xmlData,indent=2)
# jsonFile.write(xmlContent)
# jsonFile.close()

infoKey = {
    "text":["w:t","#text"],
    "line":["w:u"],
    "number":["w:numPr"],
    "wrap":["w:br"],
    "weight":["w:bCs","w:b"],
}
# 常量
CONFIG = {
    "reg": {
        "wrap":"</br>",
        "title":"$Number",
        "line":"$Line",
        "separator":"-",
        "weight":"$weight"
    }
}

# 通用配置
commonCfg = {
    "title":[0,0,0,0,0,0,0,0,0,0]
}

def parseZip(filepath):
    zipf = zipfile.ZipFile(filepath)
    return zipf.read("word/document.xml")

def docToDocx(fileName):
    # fileName == xxxx.doc 带文件格式的
    currentPath = os.getcwd()
    # currentFileName = f"{currentPath}/{fileName}"
    # # currentFile = open(f"{currentPath}/{fileName}","r",encoding="utf-8")
    # # currentFileContent = currentFile.read()
    # # currentFile.close()

    targetFileName = f'{currentPath}/{".".join(fileName.split(".")[0:-1])}.docx'
    # # targetFile = open(targetFileName,"w+")
    # # targetFile.write(currentFileContent)
    # # targetFile.close()
    # # os.rename(currentFileName,targetFileName)
    # word = winC.Dispatch("Word.Application")
    # doc = word.Documents.Open(currentFileName)
    # doc.SaveAs(targetFileName,12)
    # doc.Close()
    # word.Quit()
    return targetFileName



    


def getRegLabel(key):
    return f"{CONFIG['reg'][key]}{CONFIG['reg']['separator']}"

def initTitleCfg(isClear=False):
    commonCfg["title"] = [0,0,0,0,0,0,0,0,0,0] if isClear else [0,commonCfg["title"][1],0,0,0,0,0,0,0,0]

# 处理字典
def dealWithDict(data):
    text = ""
    for val in data:
        content = getContent(data[val],val)
        text = f"{text}{content}"
        if val in infoKey["number"]:
            text = f'{getRegLabel("title")}{data[val]["w:numId"]["@w:val"]}{text}'
        if val in infoKey["line"]:
            text = f'{CONFIG["reg"]["line"]}{text}'
        if val in infoKey["weight"]:
            text = f'{CONFIG["reg"]["weight"]}{text}'
        if val in infoKey["wrap"]:
            text = f"{text}</br>"
    return text
# 处理列表
def dealWithList(data):
    text = ""
    for val in data:
        text += getContent(val)
    return text

#  获取内容
def getContent(data,key=""):
    text = ""
    if isinstance(data,dict):
        text =  dealWithDict(data)
    elif isinstance(data,list):
        text =  dealWithList(data)
    elif isinstance(data,str):
        text =  data if key in infoKey["text"] else "" 
    return text


def getHtmlLabel(text,label="div",style="agreement_underline"):
    
    curStyle = f"{style} agreement_content_row" if commonCfg["title"][1] > 0 and label=="div" else style
    return  f'<{label} class="{curStyle}">{text}</{label}>'

def getContentLabel(text,style="",label="p"):
    curStyle = f"{style} agreement_content_row  " if commonCfg["title"][1] > 0 else style
    return f'<{label} class="{curStyle}">{text}</{label}>'


# 处理加粗
def dealWithWeight(line):
    text = line.replace(CONFIG["reg"]["weight"],"")
    if re.search(f'^\{CONFIG["reg"]["weight"]}[^\n]+',line):
        text = getHtmlLabel(text,"b","")
    return text

# 处理行
def dealWithLine(line):
    text = ""
    if re.sub("\s","",line) == CONFIG["reg"]["line"]:
        pass 
    elif re.search(f'^\{CONFIG["reg"]["line"]}[^\n]+',line):
        text = getHtmlLabel(line.replace(CONFIG["reg"]["line"],""))
    elif re.search(f'\{CONFIG["reg"]["line"]}[^\n]+\{CONFIG["reg"]["line"]}',line):
        matchText = re.findall(f'\{CONFIG["reg"]["line"]}[^\n]+\{CONFIG["reg"]["line"]}',line)[0]
        # matchText = re.match(f'\{CONFIG["reg"]["line"]}[^\n]+\{CONFIG["reg"]["line"]}',line).group()
        content = getHtmlLabel(matchText.replace(CONFIG["reg"]["line"],""),"span")
        text = getContentLabel(line.replace(matchText,content))
    else:
        if line:
            text = getHtmlLabel(line.replace(CONFIG["reg"]["line"],""))
    return text
# 只考虑两位数
def getFisrtLevelTitle(num):
    numsText = ["十","一","二","三","四","五","六","七","八","九"]
    text = ""
    if num <= 10:
        text = numsText[num%10]
    else:
        textList = str(num).split("")
        text = f"{numsText[int(textList[0])]}十{ '' if int(textList[1]) == 0 else numsText[int(textList[1])]}"

    return  f"第{text}条  "

def getTitle(level):
    commonCfg["title"][level] += 1
    footer = "、"
    if level == 1 :
        initTitleCfg()
        return f'{getFisrtLevelTitle(commonCfg["title"][level])}{footer}'
    elif level == 2:
        return f'{str(commonCfg["title"][level])}{footer}'
    else:
        # return f"（{commonCfg['title'][level]}）{footer}"
        return ""

def dealWithTitle(line):
    matchText = re.match(f"\{getRegLabel('title')}\d+",line).group()
    level = int(matchText.split(CONFIG["reg"]["separator"])[1])
    title = line.replace(matchText,getTitle(level))

    return title if level != 1 else f"<h3>{title}</h3>"

# 处理段落文字
def dealWithWord(data):
    rowList = []
    index = 0
    for row in data:
        index += 1
        line = re.sub("\s","",row)
        if  re.search(f"\{getRegLabel('title')}\d+",line):
            line = dealWithTitle(line)
        if  CONFIG["reg"]["weight"] in row:
            line = dealWithWeight(line)

        if  CONFIG["reg"]["line"] in row:
            line = dealWithLine(line)
        else:
            if index == 1:
                line = f'<h1>{line}</h1>'
            else:
                # line = f'<p>{line}</p>'
                line = getContentLabel(line)

        line = line if type(line) is list else [line]
        rowList +=  line
    return rowList

def parseWord(fileName):
    xmlText = parseZip(docToDocx(fileName))
    xmlData = xmltodict.parse(xmlText)  
    pList = xmlData["w:document"]["w:body"]["w:p"]
    allData = []
    index = 0
    for pItems in pList:
        content = getContent(pItems,2)
        index += 1
        # if content != "":
        content = re.sub(f'(\{CONFIG["reg"]["line"]})+',CONFIG["reg"]["line"],content)
        content = content.split(CONFIG["reg"]["wrap"])
        allData = allData + content
    tempWordData = re.sub(f'({CONFIG["reg"]["wrap"]})+',f'{CONFIG["reg"]["wrap"]}{CONFIG["reg"]["wrap"]}',CONFIG["reg"]["wrap"].join(allData)).split(CONFIG["reg"]["wrap"])
    paragraphs = dealWithWord(tempWordData)
    initTitleCfg(True)
    return paragraphs

if __name__ == "__main__":
    print(time.time())
    html = parseWord("../public/word/协议.docx")
    htmlFile = open("index.html","w+",encoding="utf-8")

    defaultHTML = '<!DOCTYPE html><html lang="en"><head>    <meta charset="UTF-8">    <meta http-equiv="X-UA-Compatible" content="IE=edge">    <meta name="viewport" content="width=device-width, initial-scale=1.0">    <title>Document</title></head><style>body{margin:0;padding:8px;box-sizing:border-box;} div{box-sizing:border-box;} span.agreement_underline{text-decoration:underline} .agreement_content_row{margin-left:32px;width:calc(100% - 32px)} .agreement_content_indent{text-indent:20px} div.agreement_underline{border-bottom:1px solid #000;} h1{width:100%;text-align:center} p{    display: block;margin-block-start: 0em;margin-block-end: 0em;margin-inline-start: 0px;margin-inline-end: 0px;}</style><body>  '
    htmlFile.write(f'{defaultHTML}{"".join(html)}  </body></html>')
    htmlFile.close()

    print(time.time())
