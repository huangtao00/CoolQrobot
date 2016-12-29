# -*- coding: UTF-8 -*- 
import sys
import urllib  ,os
from bs4 import BeautifulSoup

import base64


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import  datetime


"""
post url: http://172.19.53.245/SelectPage.aspx/SerBindTabDate

header:
Content-Type:application/json; charset=UTF-8
Host:172.19.53.245
Origin:http://172.19.53.245
Referer:http://172.19.53.245/SelectPage.aspx

post data:
PartList: ""
SelectPart: 1
#nodeInText: "10501*Meter*博1-636*001401078179"
"""

import httplib2
def get_electricity_fee(url="http://172.19.53.245/SelectPage.aspx/SerBindTabDate",building=1,room_number=636):
    """
    get charge left from your room number 
    """
    header={
    "Content-Type":"application/json; charset=UTF-8",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.132 Safari/537.36"
    }

    SelectPart=str(building)
    #nodeInText="10501*Meter*"+"博"+"1-636*001401078179"
    nodeInText="10501*Meter*"+"博"+str(building)+"-"+str(room_number)+"*001401078179"
    data={
    "PartList":"",
    "SelectPart":SelectPart,
    "nodeInText":nodeInText,
    }
    import json
    data=json.JSONEncoder().encode(data)
    #data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')
    h = httplib2.Http()
    response, content=h.request(url,'POST', headers=header,body=data)
    #print (response)
    myjson=json.loads(content.decode("utf-8"))
    data=myjson['d']
    #print (data)
    soup=BeautifulSoup(data,"lxml")
    #a myriad of information  u can get from the soup object 
    newlist=soup.find("td", { "id" : "tdSYValue" })
    left_power=newlist.string 
    #print (left_power)
    left_power_number=float(left_power[:-1]) #get charge float number 
    print( left_power_number)
    return left_power_number
    information2send=str("charge left:")+left_power
    maildict={"content":information2send}
def gettime():
    import datetime
    now=datetime.datetime.now()
    return now.strftime(' %y-%m-%d %H:%M:%S')
def redcolor(text):
    start="\033[91m"
    end="\033[0m"
    return start+text+end;
def sendone(auser,contentdict):
    """
        给一个用户发邮件
    """
    content=contentdict["content"]

    allmsg = MIMEMultipart('alternative')
    allmsg['Subject'] =contentdict["sub"]#u"寝室可用电量发送程序 by Huangtao"
    allmsg['From'] =contentdict["from"] #u"From Huangtao "
    allmsg['To'] =  auser
    msg = MIMEText(_text=content,_subtype="html", _charset='utf-8')
    allmsg.attach(msg)




    #输入Email地址和口令:
    from_addr = '2990303179@qq.com'
    #password ="397916230qq"
    password ="yzmqryfvwvvmdgcii"
    # 输入SMTP服务器地址:
    smtp_server = 'smtp.qq.com'
    # 输入收件人地址:
    to_addr =auser
    #SMTP协议默认端口是25
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(0)
    server.login(from_addr, password)
    #print "\n"+gettime()+" start sending mail:"+contentdict["mp3filename"]+" to "+auser
    server.sendmail(from_addr, to_addr, allmsg.as_string())
    server.quit()
    #print gettime()+" send to "+ auser +" finished !"






if __name__ == '__main__':
    get_electricity_fee()
    #sendone("397916230@qq.com",maildict)


