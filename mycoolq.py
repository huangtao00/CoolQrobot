#-*- coding:utf-8 -*-

import sys,time
#sys.setdefaultencoding('gbk')
#ws://localhost:25303/

import websocket
import multiprocessing
from multiprocessing import Manager


#share data using this method
manager = Manager()
sendinfoPool = manager.list()
vip_dict=manager.dict()
vip_dict["a"]=100

class toQQGroup:
    def __init__(self,groupid=None):
        self.groupid=groupid
        self.msg=""
        self.ws=None
    def setWS(self,ws):
        self.ws=ws
    def setGroupID(self,groupid):
        self.groupid=groupid
    def setMsg(self,msg):
        self.msg=msg
    def sendMsg(self,groupid,msg):
        msg='{"act": "101","groupid": "%s","msg": "%s"}' %(str(groupid),msg)
        self.ws.send(msg)
    def sendMsg(self):
        msg='{"act": "101","groupid": "%s","msg": "%s"}' %(str(self.groupid),self.msg)
        self.ws.send(msg)
    def sendMsg(self,msg):
        msg='{"act": "101","groupid": "%s","msg": "%s"}' %(str(self.groupid),msg)
        self.ws.send(msg)

class toQQPrivate:
    def __init__(self,QQID=None):
        self.QQID=QQID
        self.msg=""
        self.act=106
    def setWS(self,ws):
        self.ws=ws
    def setQQID(self,QQID):
        self.QQID=QQID
    def setMsg(self,msg):
        self.msg=msg
    def sendMsg(self,QQID,msg):
        msg='{"act": "106","QQID": "%s","msg": "%s"}' %(str(QQID),msg)
        self.ws.send(msg)
    def sendMsg(self):
        msg='{"act": "106","QQID": "%s","msg": "%s"}' %(str(self.QQID),self.msg)
        self.ws.send(msg)
    def sendMsg(self,msg):
        msg='{"act": "106","QQID": "%s","msg": "%s"}' %(str(self.QQID),msg)
        #print msg
        self.ws.send(msg)
class MyQQ():
    def  __init__(self):
        self.personNum=0
        self.groupNum=0
        self.QQIDlist=[]
        self.GroupIDlist=[]
    def setWS(self,ws):
        self.ws=ws
    def addPerson(self,QQID):
        self.QQIDlist.append(QQID)
        self.personNum+=1
    def addGroup(self,GroupID):
        self.GroupIDlist.append(GroupID)
        self.groupNum+=1
    def sendperMsg(self,QQID,msg):
        if QQID in self.QQIDlist:
            person=toQQPrivate(QQID)
            person.setWS(self.ws)
            person.sendMsg(msg)
        else:
            print("you dont have this QQ friend:%d" %(QQID))
    def sendgroMsg(self,GroupID,msg):
        if GroupID in self.GroupIDlist:
            group=toQQGroup(QQID)
            group.setWS(self.ws)
            group.sendMsg(msg)
        else:
            print("you dont have this QQ friend:%d\nmsg sending failed!" %(QQID))
    def addAllPerson(self):
        pass
    def addAllGroup(self):
        pass

    def __del__(self):
        print("close websocket now")
        self.ws.close()
import json
def on_message(ws, message):
    global gmsg
    global aaa
    message=json.loads(message)
    if "msg" in message:
        amsg=message["msg"]
        key=""
        if ":" in  amsg:
            key,value=amsg.split(":")
            print key,value
            value=int(value)
        elif "：" in message:
            key,value=amsg.split(":")
            print key,value
            value=int(value)
        if key in vip_dict:
            vip_dict[key]=value
            tmpmsg="set dict:"+key+"="+str(value)+" ok!"
            sendinfoPool.append(tmpmsg)
    else:
        print "wrong"

    print "\n"


def checkmsgpool(qq,msgpool):
    while True:
        time.sleep(2)
        if len(msgpool):
            tmpmsg=msgpool.pop()
            qq.sendperMsg(397916230,tmpmsg)



if __name__ == '__main__':

    ws = websocket.WebSocket()
    ws.connect("ws://192.168.1.142:25303/") #run coolQ in the local network on the windows 7 system
    qq=MyQQ()
    qq.setWS(ws)
    qq.addPerson(397916230)
    qq.sendperMsg(397916230,"hello 你")

    wslisten = websocket.WebSocketApp("ws://192.168.1.142:25303/",on_message=on_message)
    #ws.connect("ws://192.168.1.142:25303/") #run coolQ in the local network on the windows 7 system
    process = multiprocessing.Process(target=wslisten.run_forever,args=())
    process.start()
    checkpro = multiprocessing.Process(target=checkmsgpool,args=(qq,sendinfoPool))
    checkpro.start()
    #wslisten.run_forever()

    while True:
        time.sleep(3)
        if vip_dict["a"]==2:
            qq.sendperMsg(397916230,"hello 你")
        # print gmsg,id(gmsg)
        # print "vip list",vip_list
        print "vip dict",vip_dict