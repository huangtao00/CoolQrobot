#-*- coding:utf-8 -*-

import sys,time
#sys.setdefaultencoding('gbk')
#ws://localhost:25303/

import websocket
import multiprocessing
from multiprocessing import Manager
from dormCharge import get_electricity_fee

#share data using this method
manager = Manager()
sendinfoPool = manager.list()
vip_dict=manager.dict()
vip_dict[u"a"]=u"2"




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
def readVariableVal(key):
    if key in vip_dict:
        msg=str(key)+"="+str(vip_dict[key])
    else:
        msg=str(key)+" does not exist"
    return msg

def writeVariableVal(key,value):
    if key in vip_dict:
        vip_dict[key]=value
        tmpmsg="set dict:"+key+"="+str(value)
    else:
        vip_dict[key]=value
        tmpmsg="add a new dict:"+key+"="+str(value)
    return tmpmsg

def getKeyValue(amsg):
    #print "amsg",amsg
    if ":" in  amsg:
        key,value=amsg.split(":")
        print (key,value)
        return key,value
    elif u"：" in amsg:
        key,value=amsg.split(":")
        print (key,value)
        return key,value
    else:
        return None,None

import json
def on_message(ws, message): 
    """
    receive message and deal with it

    """

    message=json.loads(message)
    if "msg" in message:
        amsg=message["msg"]
        key,value=getKeyValue(amsg)
        if key==None:                               #map string to function 
            if amsg==u"电费":
                tmpmsg=get_electricity_fee()
                print(tmpmsg)
                sendinfoPool.append(tmpmsg)

        else:
            if "check" ==key:                       # read variable from vip_dict
                tmpmsg=readVariableVal(value)
                sendinfoPool.append(tmpmsg)
            else:
                tmpmsg=writeVariableVal(key,value)  # write value to a variable
                sendinfoPool.append(tmpmsg)  
    else:
         sendinfoPool.append("Sorry!I Got Wrong Msg!!")



def checkmsgpool(qq,msgpool):
    """
    check out the msgpool situation, 
    if not empty,means we have message to send
    """
    while True:
        time.sleep(2)
        if len(msgpool):
            tmpmsg=msgpool.pop()
            qq.sendperMsg(397916230,tmpmsg)



from getWSaddr import getWSaddr
if __name__ == '__main__':

    wsaddr=getWSaddr(port=25303)
    # print wsaddr
    ws = websocket.WebSocket()
    ws.connect(wsaddr) #run coolQ in the local network on the windows 7 system
    print ("connected ok")

    #binding websocket to QQ  in order to send message
    qq=MyQQ()
    qq.setWS(ws)
    qq.addPerson(397916230)
    qq.sendperMsg(397916230,"hello 你")

    #Daemon1:wslistener is another porcess in order to listen to all the message from private and group
    wslistener = websocket.WebSocketApp(wsaddr,on_message=on_message)
    process = multiprocessing.Process(target=wslistener.run_forever,args=())
    process.start()

    #Daemon2:checkmsgpool is another process in order to check out the message pool,if  not empyt ,than send it to the destination
    #use this daemon process to response to the received message
    checkpro = multiprocessing.Process(target=checkmsgpool,args=(qq,sendinfoPool))
    checkpro.start()



    while True:
        time.sleep(3)
        if  "a" in vip_dict:
            if vip_dict["a"]=="2":
                qq.sendperMsg(397916230,"hello 你")
            # print gmsg,id(gmsg)
            # print "vip list",vip_list
        #print ("vip dict",str(vip_dict))