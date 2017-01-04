
import os.path
import websocket,time
import socket
import multiprocessing
from multiprocessing import Manager

#print (__file__)  #__file__ save the name of this file
abspath=os.path.abspath(__file__)
current_dir=os.path.dirname(abspath)
#share data using this method
manager = Manager()
sendinfoPool = manager.list()
validWSaddr=manager.list() #empty dict

def searchVaildAddress(ip="192.168.0.1",port=25303):
	ws = websocket.WebSocket()
	#ws.settimeout(3)
	try:
		wsaddr="ws://"+ip+":"+str(port)+"/"
		#print (wsaddr)
		ws.connect(wsaddr)
		validWSaddr.append(wsaddr)
		#print ("get valid websocket ip:",ip)
		return 1
	except:
		#print ("not this ip:"+ip)
		return 0
	ws.close()

def getLocalIPandHeader():
	"""
	return localIP and IPhead 
	like this :192.168.1.11  , 192.168.1.
	"""
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('baidu.com', 0))
	ip=s.getsockname()[0]
	lastdotpos=ip.rfind(".")
	iphead=ip[:lastdotpos+1]
	return ip,iphead

def getWSaddr(port=25303):
	"""
	return live websocket address like this format:  "ws://192.168.191.1:25303/"
	"""
	ip,iphead=getLocalIPandHeader()
	ipend=range(1,256)
	ipend.reverse()
	for i in ipend:
		searchIP=iphead+str(i)
		checkpro = multiprocessing.Process(target=searchVaildAddress,args=(searchIP,port))
		checkpro.start()
	print ("Searching CoolQ WebSocket Address Now...")
	while True:
		if len(validWSaddr):
			return validWSaddr[0]
		time.sleep(1)


if __name__=="__main__":
	print getWSaddr()
	print "abc"




