# -*- coding:utf-8 -*-

__author__ = 'hxl'
import  os
import time
from time import sleep
import thread
import threadpool
import sys
print sys.stdin.encoding
import logging
import subprocess
import sqlite3
from multiprocessing.dummy import Pool
from json import  *
reload(sys)
sys.setdefaultencoding("utf-8") 
#device=''
'''
adb -s 127.0.0.1:21503
'''
troopsattrs={"630":"出征兵力上限",
	   "631":"步兵攻击","632":"步兵防御","633":"步兵生命","635":"步兵减伤","636":"步兵伤害加成",
	   "637":"骑兵攻击","638":"骑兵防御","639":"骑兵生命","642":"骑兵冲锋伤害",
	   "643":"弓兵攻击","644":"弓兵防御","645":"弓兵生命","647":"弓兵伤害加成",
	   "648":"车兵攻击","649":"车兵防御","650":"车兵生命","653":"车兵攻城攻击力",
	   "654":"资源掠夺量",
	   "657":"战斗损失转化伤兵",
	   "658":"攻城战中消灭伤兵"}
accounts={"me":"1137025688001343",1:"245400909001793",2:"797241380001797",4:"514165705001810",5:"1827227077001813",6:"872333638001816",7:"721468394001819",9:"410302945001819",10:"995794480001817",12:"75676947001820"}
platforms=['cn360','mi']
def AllianceMemeber(AllianceName,device=''):

	stm=time.strftime("%y_%m_%d_%H_%M_%S")
	dbfile="C:\\cok\\cok_me\\%s_chat_service.db"%stm
	os.system('adb %s pull /sdcard/data/data/com.hcg.cok.mi/1137025688001343/database/chat_service.db %s'%(('-s %s')%device if device <> '' else '',dbfile))
	conn=sqlite3.connect(dbfile)
	cursor=conn.execute("select * from User where AllianceName='%s'"%AllianceName)
	print "UserID\t\tNickName"
	for row in cursor:
		print row[2],'\t\t',row[3]
def battleparse(dbfile):
	conn = sqlite3.connect(dbfile)
	cursor = conn.execute("select createtime,Contents from mail where channelid='fight' order by createtime desc limit 1,2;")
	print "UserName\tNickName"
	for row in cursor:
		content=row[1]
		jdata=loads(content)
		print jdata
		#print jdata['atkUser']["uid"]
		print 'attach:'
		print '攻击者:',jdata['atkUser']["uid"],getuserinfo(jdata['atkUser']["uid"])
		print
		print '防御者:',jdata['defUser']['uid'],getuserinfo(jdata['defUser']['uid'])
		print "攻击者损失战力:",jdata['atkPowerLost']

		for i in jdata["atkWarEffect"]:
			#print i
			for k in i.keys():
				if troopsattrs.has_key(k):
					print troopsattrs[k],':',i[k]
			#print attrs[i[0]]
		print '攻击方龙的等级:',jdata['atkBattleGenerals']#[0]['level']
		print "防御方损失战力:",jdata['defPowerLost']

		for i in jdata["dfWarEffect"]:
			#print i
			for k in i.keys():
				if troopsattrs.has_key(k):
					print troopsattrs[k],':',i[k]
		print "防御方龙的等级:",jdata['defDrag'][0]['level']

def monster_report_parse(str=""):
	jstr='''{"att":{"generalExp":11675,"total":95600,"powerLost":179,"dead":0,"rwdPro":1.100000023841858,"survived":95564,"kill":95415,"exp":11675,"hurt":36},"xy":664714,"def":{"powerLost":708183,"dead":109372,"id":"900762","mmhp":109372,"mchp":0},"rateReward":[{"type":7,"value":{"itemId":"211659","rewardAdd":42,"count":2306,"uuid":"291474ec655948f29bcb043aac6fe0b0","vanishTime":1498460725893}},{"type":7,"value":{"itemId":"200567","rewardAdd":4,"count":865,"para1":"230107","uuid":"0a3ceac55cb64bffaa173bfc4385b0eb","vanishTime":0}},{"type":7,"value":{"itemId":"209861","rewardAdd":12,"count":279,"para1":"1","para2":"209862","para4":"160305","uuid":"af7aac7122d9417abb657f5ff99d0c03","para5":"1","vanishTime":0}},{"type":7,"value":{"itemId":"200201","rewardAdd":8,"count":5535,"para1":"1","para2":"1","para3":"300","uuid":"d278d6e08b224e37ac06b1b9e491d7cf","vanishTime":0}}],"reportUid":"59ade1e918d8423aad700e2fea09f0dc"}'''
	jdata=loads(jstr)
	print "point:",jdata["xy"]
	print "获得经验",jdata['att']["generalExp"]
	print "出征部队:",jdata['att']["total"]
	print "受伤:",jdata['att']['hurt']
	print "死亡:", jdata['att']['dead']
	print  "杀敌数:",jdata['att']['kill']


	pass
def getuserinfo(userid):
	conn = sqlite3.connect("C:\cok\cok_me\\17_06_13_11_31_05_chat_service.db")
	cursor = conn.execute(
		"select NickName,AllianceName from user where userid='%s'"%userid)
	#print "UserName\tNickName"
	for row in cursor:
		print dumps(row,ensure_ascii=False,encoding="gb2312")
def getdb(account,pf='cn360', device=''):
	stm=time.strftime("%y_%m_%d_%H_%M_%S")
	if isinstance(account,int):
		dbfile = "C:\\cok\\cok_%04d\\%s_chat_service.db"%(account,stm)
	elif isinstance(account,str):
		dbfile = "C:\\cok\\cok_%s\\%s_chat_service.db" % (account, stm)
	os.system('adb %s pull /sdcard/data/data/com.hcg.cok.%s/%s/database/chat_service.db %s' % (('-s %s') % device if device <> '' else '',pf,accounts[account],dbfile))
	# conn = sqlite3.connect(dbfile)
	# cursor = conn.execute("select * from User where AllianceName='SHR'")
	# print "UserName\tNickName"
	# for row in cursor:
	# 	print row[2], row[3]
	#os.system("C:\Users\\xilonghx\Downloads\SQLiteSpy_1.9.11\SQLiteSpy.exe %s"%dbfile)
	return dbfile

def AllianceLastLogin(AllianceName='MPE'):
	dbfile=getdb('me','mi')
	conn = sqlite3.connect(dbfile)
	cursor = conn.execute("select datetime(LastUpdateTIme, 'unixepoch', 'localtime') as time, Nickname from user where AllianceName = '%s';"%AllianceName)
	print "UserName\tNickName"
	for row in cursor:
		print row[0], row[1]

def UserLastLogin(UserId='1839606032001465'):
	dbfile = getdb('me', 'mi')
	conn = sqlite3.connect(dbfile)
	cursor = conn.execute(
		"select datetime(LastUpdateTIme, 'unixepoch', 'localtime') as time, Nickname from user where Userid = '%s';" % UserId)
	#print "UserName\tNickName"
	for row in cursor:
		print row[0], row[1]

#devices='BIIN75BAJNHUNBTO'
accouts=['cokhxl%04d'%i for i in xrange(1,12) if i<>8 or i<>8]

# logging.basicConfig(level=logging.DEBUG,
# 					format='%(thread)d %(asctime)s %(levelname)s %(message)s', 
# 					filename='log.txt',
# 					filemode='a+')
logging.basicConfig(level=logging.DEBUG,
				format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
				datefmt='%Y-%m-%d-%H:%M:%S',
				filename='myapp.log',
				filemode='w')
#################################################################################################
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################
def CMD(cmd):
	res=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
	out,err= res.communicate()
	if err == None:
		if len(out.split('\n'))>=1:
			return out
def startcok(t=0,device=''):
	os.system("adb %s shell am start com.hcg.cok.cn360/com.clash.of.kings.COK"%(('-s %s')%device if device <> '' else ''))
	sleep(t)
def getsoldier(device=''):
	if (isBig(device)):
		click(900,1850,0.2,device)
		click(550,1160,2,device)

	else:
		click(580,1210,1,device)
		click(355,780,2,device)
def click(x,y,t=0,device=''):
	os.system('adb %s shell input tap %d %d'%(('-s %s')%device if device <> '' else '',x,y))
	sleep(t)
def key(key,t=1,device=''):
	if device=='':
		os.system('adb shell input keyevent %s'%(key))
	else:
		os.system('adb -s %s shell input keyevent %s'%(device,key))
	sleep(t)
def slide(a,b,c,d,t=500,device=''):
	if device=='':
		os.system('adb shell input swipe %d %d %d %d %d '%(a,b,c,d,t))
	else:
		os.system('adb -s %s shell input swipe %d %d %d %d %d '%(device,a,b,c,d,t))
def enter(t=0,device=''):
	key(66,t,device)
def tab(device=''):
	key(61,0,device)
def gotocityorworld(device=''):
	if (isBig(device)):
		pass
	else:
		click(70,1233,1,device)
def clkbuild(device=''):
	if(isBig(device)):
		pass
	else:
		click(375,1030,0.5,device)
def confirmbuild(device=''):
	if(isBig(device)):
		pass
	else:
		click(500,1054,1,device)
def batch_update(device=''):
	if (isBig(device)):
		pass
	else:
		# click(210,736,0.5,device)
		# click(265,830,0.5,device)
		# confirmbuild(device)
		# click(220,620,1,device)

		click(527,777,0.5,device)
		click(580,870,0.5,device)
		confirmbuild(device)
		speedup(device)
		pass
def dobuild(device):
	clkbuild(device)
	confirmbuild(device)
def sendtext(text,t=0,device=''):
	os.system("adb %s shell input text %s"%('-s %s'%device if device <> '' else '',text))
	sleep(t)
def changeinputmothod(name,device=''):
	# key(59,0,device) #shift
	# key(62,0,device) #space
	inputs={"hacker" : "org.pocketworkstation.pckeyboard/.LatinIME",
			"baidu":"com.baidu.input/.ImeService"}
	os.system('adb %s shell ime set %s'%('-s %s'%device if device<>'' else "",inputs[name])) #change inputmethod

def backkey(device=''):
	key('4',1,device)

def back(device=''):
	if device=='':
		click(50,50,0.5,device)
	else:
		click(50,50,1,device)
	#os.system('adb shell input keyevent 4'%device)
def getreward(n=1,device=''): #or job tip
	if device =='':
		cmd='adb shell input tap 250 1050'
	else:
		cmd='adb -s %s shell input tap 250 1050'%device
	for i in xrange(0,n):
		os.system(cmd)
		sleep(0.5)

def getupreward(device=''):#升级奖励
	click(360,990,1,device)
	sleep(3)
def speedup(device=''):
	if(isBig(device)):
		click(85,270,1,device)
	else:
		click(60,180,1,device)
def training(device=''):
	click(500,1200,1,device)
def getgoods(device=''):
	if(isBig(device)):
		pass
	else:
		click(360,1050,1,device)
def radm():
	click(360,640,1,device)
def startborn(device=""):
	if (isBig(device)):
		# #sleep(40)#50剧情
		# print u'升级城堡到二级'
		# os.system('adb -s %s shell input tap 380 790'%device)
		# sleep(2)
		# os.system('adb -s %s shell input tap 500 1050'%device)
		# sleep(2)
		# os.system('adb -s %s shell input tap 370 640'%device) #新建林
		# sleep(1)
		# os.system('adb -s %s shell input tap 360 1030'%device)#确定 单按钮
		# sleep(1)
		# os.system('adb -s %s shell input tap 370 640'%device) #新建林
		# sleep(1)

		# os.system('adb -s %s shell input tap 370 640'%device) #新建马厩
		# sleep(1)
		# os.system('adb -s %s shell input tap 360 1030'%device)#确定 单按钮
		# sleep(1)
		# os.system('adb -s %s shell input tap 370 640'%device)#确定 双按钮按钮
		# sleep(1)
		
		# os.system('adb -s %s shell input tap 360 1030'%device)#训练
		# sleep(1)
		# os.system('adb -s %s shell input tap 500 1220'%device)#确定
		# sleep(1)
		
		# os.system('adb -s %s shell input tap 370 420'%device)#收获骑兵
		# sleep(1)
		# os.system('adb -s %s shell input tap 195 1230'%device)#点击任务
		# sleep(1)
		# os.system('adb -s %s shell input tap 600 600'%device)#点领奖
		# sleep(2)
		
		# os.system('adb -s %s shell input tap 50 40'%device)#back
		# sleep(3)
		
		# os.system('adb -s %s shell input tap 350 1000'%device)#领取
		# sleep(3)
		
		# print u'建造第二个农田'
		# getreward(1,device)
		# os.system('adb -s %s shell input tap 200 1060'%device)#建2农田
		# sleep(3)
		# os.system('adb -s %s shell input tap 310 520'%device)#点击第一个坑
		# sleep(1)
		# os.system('adb -s %s shell input tap 360 1030'%device)#确定 单按钮
		# sleep(1)
		# os.system('adb -s %s shell input tap 500 1045'%device)#立即建造/建造 双按钮按钮
		# sleep(1)
		# os.system('adb -s %s shell input tap 456 567'%device)#点击第2个坑
		# sleep(1)
		# os.system('adb -s %s shell input tap 360 1030'%device)#确定 单按钮
		# sleep(1)
		# os.system('adb -s %s shell input tap 500 1045'%device)#立即建造/建造 双按钮按钮
		# sleep(1)
		
		# os.system('adb -s %s shell input tap 200 610'%device)#点击第3个坑
		# sleep(1)
		# os.system('adb -s %s shell input tap 360 1030'%device)#确定 单按钮
		# sleep(1)
		# os.system('adb -s %s shell input tap 500 1045'%device)#立即建造/建造 双按钮按钮
		# sleep(1)
		
		# os.system('adb -s %s shell input tap 195 1230'%device)#点击任务
		# sleep(1)
		# os.system('adb -s %s shell input tap 600 600'%device)#点领奖
		# sleep(2)
		# os.system('adb -s %s shell input tap 580 870'%device)#点领奖
		# sleep(2)
		
		# back(device)
		
		# print '#点击任务建造校场'
		# os.system('adb -s %s shell input tap 195 1230'%device)
		# sleep(1)
		# os.system('adb -s %s shell input tap 600 600'%device)#前往
		# sleep(1.5)
		# os.system('adb -s %s shell input tap 200 1050'%device)#点击任务建造校场
		# sleep(1)
		# os.system('adb -s %s shell input tap 370 625'%device)#点击校场位置
		
		# os.system('adb -s %s shell input tap 360 1030'%device)#确定 单按钮
		# sleep(1)
		# os.system('adb -s %s shell input tap 500 1045'%device)#立即建造/建造 双按钮按钮
		# sleep(1)
		
		# print '#探索世界'
		# os.system('adb -s %s shell input tap 80 1230'%device)#探索世界--点击世界按钮
		# sleep(10)
		
		# print '攻击小兵'
		# os.system('adb -s %s shell input tap 360 635'%device)#点击小兵
		# sleep(1)
		# os.system('adb -s %s shell input tap 360 1030'%device)#攻击
		# sleep(1)
		# os.system('adb -s %s shell input tap 540 1200'%device)#出征
		
		# os.system('adb -s %s shell input tap 80 1230'%device)#点击世界按钮回城
		# sleep(3)
		# print '升级瞭望塔'
		# os.system('adb -s %s shell input tap 360 830'%device)#升级瞭望塔
		# sleep(3)
		# os.system('adb -s %s shell input tap 500 1045'%device)#升级
		
		# os.system('adb -s %s shell input tap 80 1230'%device)#点击世界出城看怪物攻城
		# sleep(7)
		
		# os.system('adb -s %s shell input tap 80 1230'%device)#点击世界按钮回城
		# sleep(2)
		
		# print'建造战争堡垒'
		# os.system('adb -s %s shell input tap 360 640'%device)#点击位置建造战争堡垒
		
		# os.system('adb -s %s shell input tap 360 1030'%device)#确定 单按钮
		# sleep(1)
		# os.system('adb -s %s shell input tap 500 1045'%device)#立即建造/建造 双按钮按钮
		# sleep(2)
		
		# os.system('adb -s %s shell input tap 550 830'%device)#建造
		# sleep(1)
		# os.system('adb -s %s shell input tap 500 1045'%device)#立即建造/建造 双按钮按钮
		# sleep(1)
		
		# print '收获落石'
		# os.system('adb -s %s shell input tap 370 420'%device)#收获
		# sleep(1)
		
		# os.system('adb -s %s shell input tap 80 1230'%device)#点击世界按钮出城
		# sleep(10)
		
		# os.system('adb -s %s shell input tap 80 1230'%device)#点击世界按钮回城
		# sleep(2)

		# #指引结束


		print '收获成就'
		#getreward(3,device)
		getreward(1,device) #点击任务建造伐木场2个
		click(360,640,0.5,device)# 1
		click(360,1030,0.5,device)
		click(500,1045,0.5,device)

		getreward(3,device)
		sleep(3)

		click(360,780,0.5,device)#升级兵营
		click(500,1050,0.5,device)#升级
		speedup(device)

		getreward(3,device)

		training(device)#训练5个民兵

		getreward(3,device)

		print '升级城墙到二级'
		click(360,780,0.5,device) #升级城墙
		click(500,1050,0.5,device)#升级
		speedup(device)

		click(380,640,0.5,device)
		getgoods(device)
		back(device)
		sleep(5)
		##TODO 领取新手奖励
		print '升级城堡到三级'
		getreward(1,device)
		click(420,800,0.5,device)#升级城堡到三级
		click(480,1050,0.5,device)#升级

		exit(1)
		click(520,100,0.5,device)#跳过剧情
		click(300,300,0.5,device)#随便点击

		speedup(device)

		print '建造靶场'
		getreward(1,device)
		click(380,635,0.5,device)
		click(380,1020,0.5,device)#建造
		click( 500 ,1045,0.5,device)#立即建造/建造 双按钮按钮

		click(300,300,0.5,device) #random

		speedup(device)
		getupreward(device)
		getreward(1,device)
		click(370,630,0.5,device)#行军帐篷
		click(360,1020,0.5,device)
		click( 500 ,1045,0.5,device)
		speedup(device)

		getreward(1,device)

		click(420,740,0.5,device)#升级农田
		click(500,1045,0.5,device)#升级
		speedup(device)

		getreward(2,device)
		click(420,740,0.5,device)#升级伐木场
		click(500,1045,0.5,device)#升级
		speedup(device)

		getreward(2,device)
		click(360,788,0.5,device)#升级仓库
		click(500,1050,0.5,device)#升级
		speedup(device)

		getreward(3,device)
		click(360,788,0.5,device)#升级马厩
		click(500,1050,0.5,device)#升级
		speedup(device)

		getreward(2,device)
		click(360,788,0.5,device)#升级马厩
		click(500,1050,0.5,device)#升级
		speedup(device)

		getreward(2,device)
		click(420,740,0.5,device)
		click(500,1050,0.5,device)#升级
		speedup(device)

		getreward(2,device)
		click(420,740,0.5,device)
		click(500,1050,0.5,device)#升级校场
		speedup(device)
		sleep(3)

		click(230,1230,0.5,device)#回城旁边的领奖
		radm(device)
		click(200,1000,0.5,device)
		click(600,600,0.5,device)
		click(600,600,0.5,device)
		back(device)

		getreward(1,device)
		click(360,635,0.5,device)
		click(360,1030,0.5,device)
		click(500,1045,0.5,device)

		getreward(2,device)
		click(420,740,0.5,device)
		click(500,1050,0.5,device)#升级校场
		speedup(device)

		getreward(1,device)
		click(360,640,0.5,device)
		click(360,1020,0.5,device)#建造
		click( 500 ,1045)#立即建造/建造 双按钮按钮
		speedup(device)

		getreward(1,device)
		click(360,640,0.5,device)
		click(360,1020,0.5,device)#建造
		click( 500 ,1045)#立即建造/建造 双按钮按钮
		speedup(device)
	else :
		# logging.info('攻击小兵')
		# click(360,665,0.2,device)
		# click(360,877,0,device)
		# click()

		logging.info('建造两个伐木场')
		getreward(1,device)
		click(365,655,0.5,device)
		dobuild(device)
		click(460,730,0.5,device)
		dobuild(device)
def newaccout():
	click(300,787,0.5,device)
	os.system('adb shell input text "890219"'%device)
	click(360,750,0.5,device)

def getdayreward(device=''):
	if isBig(device):
		click(230,300,1,device)
 		click(540,1470,1,device)
		click(420,300,1,device)
		click(540,1470,1,device)
		click(600,300,1,device)
		click(540,1470,1,device)
		click(800,300,1,device)
		click(540,1470,1,device)
		slide(1000 ,380, 300, 380, 1000,device)
		click(230,300,1,device)
		click(540,1470,1,device)
		click(420,300,1,device)
		click(540,1470,1,device)
	else:
		click(160,200,0.5,device)
		click(370,990,0.5,device)
		click(270,200,0.5,device)
		click(370,990,0.5,device)
		click(413,200,0.5,device)
		click(370,990,0.5,device)
		click(530,200,0.5,device)
		click(370,990,0.5,device)
		slide(600 ,200 ,200, 200 ,1000,device)
def snap(device='',bexit=1):
	print device

	timestr=time.strftime('%Y-%m-%d-%H_%M_%S',time.localtime(time.time()))
	os.system('Adb %s shell /system/bin/screencap -p /sdcard/screenshot.png'%(' -s '+ device if device <> '' else ''))
	sleep(1)
	dst="%s.png"%timestr
	os.system('Adb %s pull /sdcard/screenshot.png %s'%((' -s '+ device if device <> '' else ''),dst))
	if bexit :
		exit()
	return dst
def isBig(device='',l=[]):
	# if os.popen('adb %s shell wm size'%(('-s %s')%device if device <> '' else '')).readlines()[0].find('1080x1920') <> -1:
	# 	return True
	# else:i
	if len(l)==0:
		cmd='adb %s shell wm size'%('-s '+device if device <> '' else '')
		print cmd
		str=os.popen(cmd).readlines()
		print str
		if len(str) == 0:
			print 'no device'
			return
		if str[0].find('1080x1920') <> -1:
			l.append(True)
		else:
		#if str[0].find('1080x1920') <> -1:
		#	return True
			l.append(False)
	return l[0]

def login():
	os.system('adb -s shell 127.0.0.1:21503 input text "gp10498660"'%device) #Tab
	os.system('adb -s shell 127.0.0.1:21503 input keyevent 61'%device) #Tab
	os.system('adb -s shell 127.0.0.1:21503 input text "890219"'%device) #Tab
	os.system('adb -s shell 127.0.0.1:21503 input keyevent 66'%device) #Enter
def say(device):
	click(252,1240,1,device)
	for i in xrange(0,100):

		click(460,750,1,device)
		click(460,1150,1,device)
		click(675,675,1,device)
		#backkey(device)
		sleep(5)
def gettimedgift(device):	
	click(50,950,0.5,device)
	click(550,480,0.5,device)

def ss(device):
	click(375,345,1,device)
	click(375,985,1,device)

devices=['127.0.0.1:62001','127.0.0.1:62025','127.0.0.1:62026','127.0.0.1:62027','139124717d22']
def help(device=""):
	if isBig(device):
		pass
	else:
		click(375,1220,1,device)
def helpall1():
	while 1:
		for i in devices:
			click(375,1220,0,i)
		sleep(1)
def helpall():
	pool=threadpool.ThreadPool(5)
	reqs=threadpool.makeRequests(lambda x:click(375,1220,1,x),devices)
	[pool.putRequest(req) for req in reqs]
	pool.wait()
def keephelpall():
	while 1:
		pool=threadpool.ThreadPool(5)
		reqs=threadpool.makeRequests(lambda x:click(375,1220,1,x),devices)
		[pool.putRequest(req) for req in reqs]
		pool.wait()
		sleep(1)
def getdayrewards():
	pool=threadpool.ThreadPool(5)
	reqs=threadpool.makeRequests(lambda x:getdayreward(x),devices)
	[pool.putRequest(req) for req in reqs]
	pool.wait()
	# for i in devices:
	#	 click(375,1220,0,i)
	# sleep(1)
def getgifts():
	pool=threadpool.ThreadPool(5)
	reqs=threadpool.makeRequests(lambda x:getgift(x),devices)
	[pool.putRequest(req) for req in reqs]
	pool.wait()
def doTimedtask(device):
	click(710,660,1,device)

def changeaccount1(account,device=''):
	logging.info('account :%s'%account)
	#changeinputmothod(device)
	y=570
	click(710,y,1,device) #pop 4 tabs
	click(415,y,3,device) #click fuli

	#sim
	#click(270,225,0.5,device) #click changeaccount
	#click(475,530,0.2,device) #delete account
	#red3
	click(360,300,0.5,device)
	click(510,490,0.5,device)

	key()
	sendtext(account,device)
	enter(device)
	enter(device)
	sendtext('890219',device)
	enter(device)
	#sleep(0.2)
	#backkey(device)b
	#click(370,720,1,device) #click login btn
	enter(device)
	sleep(5) #login timeout
	backkey(device) #remove login ui
	sleep(15)		#start ui
	backkey(device) #remove ads

	# logging.info('get timed gift')
	# click(350,490,0.5,device)	
	# click(365,720,0.5,device)

	#signin(device)
	#getlimitedreward(device)
def batch_changeid(device):
	changeinputmothod(device)
	for name1 in accouts:
		print name1
		changeaccount(name1,device)
		sleep(5)
def farmerupdate(device):
	# click(190,640,1,device)
	# click(260,730,1,device)
	# click(500,1060,1,device)

	# click(310,520,1,device)
	# click(360,640,0.5,device)
	# click(500,1060,1,device)
	# click(310,430,1,device)

	click(450,570,0.5,device)
	click(500,680,0.5,device)
	click(500,1060,1,device)
	click(450,480,3,device)
def scure(device):
	if (isBig(device)):
		pass
	else:
		pts=[290,450,600,760]
		txtptsy=[226,380,540,700,]
		click(400,665,1,device)
		click(500,765,0.5,device)
		for y in pts:
			slide(600,y,200,y,100,device)
		click(500,txtptsy[2],0.5,device)
		sendtext('400',device)
		enter(device)
		click(580,1220,2,device)
		click(375,595,2,device)
		helpall()
def  showlogs(device):
	pass
def buildsilver(device=''):
	xs=[(180,810),(270,710),(370,770),
	(500,820),(670,820)]
	if(isBig(device)):
		pass
	else:
		#build silver
		for pt in xs : 
			click(pt[0],pt[1],0.5,device)
			#
			slide(360,150,360,1000,1000,device)
			slide(360,150,360,1000,1000,device)

			click(360,1030,0.5,device)
			click(500,1050,0.5,device)

			click(pt[0],pt[1]-80,0.5,device)
			sleep(2)


def updatesilver(device=''):
	xs=[(180,810),(270,710),(370,770),
	(500,820),(670,820)]
	if(isBig(device)):
		pass
	else:
		#build silver
		buildsilver(device)
		#updatesilver
		for pt in xs : 
			click(pt[0],pt[1],0.5,device)
			click(pt[0]+66,pt[1]+135,0.5,device)
			upgrade()
			break;

		#speedup()
		#speedup()

def signin(device):
	slide(200,700,700,700,500,red3)
def upgradefarm(device=''):
	pts=[#(420,975),
	#(610,1030),
	(740,1130),(490,1140)]
	if (isBig(device)):
		for pt in pts : 
			click(pt[0],pt[1],0.5,device)
			click(pt[0]+66,pt[1]+135,0.5,device)
			click(750,1575,1,device)

			speedup()
def upgradewood(device=''):
	pts=[(400,1070),
	(520,1160),
	(645,1263),(655,1025)]
	if (isBig(device)):
		for pt in pts : 
			click(pt[0],pt[1],0.5,device)
			click(pt[0]+66,pt[1]+135,0.5,device)
			click(750,1575,1,device)

			speedup()
def login(device=''):
	slide()
def getgift(device):	
	click(50,950,1,device)
	click(550,480,4,device)
	#os.system('adb %s shell input tap 550 480'%('-s %s')%device if device <> '' else '')
	click(390,310,2,device)
def dakavm(device=''):
	slide(200,700,500,700,600,device)
	click(425,770,0,device)
	click(444,925,0,device)
	click(370,878,0.5,device)
	backkey(device)
def daka(device=''):
	slide(200,700,600,700,600,device)
	sleep(2)
	click(400,370,0,device)
	click(400,530,0,device)
	click(379,880,1,device)
	backkey(device)
	pass

def batch_daka():
	pass
def callnames(device=''):
	while 1:
		click(460,750,0)
		click(454,1160,0)
		click(670,665,0.5)


def changeaccount(account, device=''):
	y = 540
	click(710, y, 1, device)  # pop 4 tabs
	click(420,y, 3, device)  # click fuli
	# red3
	print ("click changeaccount")
	click(360, 300, 0.5, device)  # click changeaccount
	print ("delete account")
	click(510, 490, 0.5, device)  # delete account
	print "change input"
	changeinputmothod("hacker",device)
	print "input account"
	sendtext(account,device)
	enter(0,device)
	print ("input pwd")
	sendtext('890219',device)
	enter(3,device)
	backkey(device)
	sleep(15)#waiting for login
	backkey(device)#exit ad
	#dakavm(device)
	daka(device)
	alliancework(device)
	help(device)

	changeinputmothod("baidu",device)
def wechat(device=''):
	for i in xrange(19):
		print i
		if(isBig(device)):
			click(190,1750,0,device)
			click(100,1835,1,device)
			backkey(device)
			slide(300,300,300,300,1000,device)
			click(133,483,0,device)
			click(630,1840,10,device)
			pass
		else:
			click(120,1185,0,device)
			click(120,1185,1,device)
			backkey(device)
			slide(200,300,200,300,1000,device)
			click(110,350,0,device)
			click(350,1240,10,device)
	exit()
def help1(device):
	slide(375,935,375,600,500,device)
	click(350,900,0,device)
	click(355,1220,1,device) #click help
	backkey(device)
	#click
def alliancework(device):
	click(645,1240,0,device)
	click(360,990,0,device)
	click(375,1220,0,device)
	click(525,135,0,device)
	click(375,1220,0,device)

def multido1(func,devices):
	pool=threadpool.ThreadPool(len(devices))
	reqs=threadpool.makeRequests(lambda x:func(x),devices)
	[pool.putRequest(req) for req in reqs]
	pool.wait()
def attack(device=''):
	click(560, 680, 0.1)
	click(675, 695, 0.1)
	click(190, 780, 0.1)
	click(660, 330, 0.1)
	click(540, 1200, 1)
def attack1(device=''):
	click(400, 650)
	click(500, 640)
	click(200, 780)
	click(650, 333)
	click(520, 1220)

	click(400, 650)
	click(500, 640)
	click(200, 780)
	click(650, 333)
	click(520, 1220)
	sleep(3)

def usegoods(n,device=''):

	if (isBig(device='')):
		for i in xrange(n):
			click(900, 1820,0.5,device)
			click(590, 1200,0.5,device)
			click(539, 1290,0.5,device)
		
		
	else:
		for i in xrange(n):
			click(630, 1210,0,device)
			click(380, 780,1)
			click(280, 980,0.5)


	exit(0)
def mobai():
	for i in xrange(10):
		click (440, 425,1)
		click(560, 230+75*i,2)

def getVIP(device='',levelcnt={0:0}):
	if isBig(device):
		for key,value in levelcnt.items():
			for i in xrange(value):
				click(875,340+250*(key-1),0,device)
				click(550,1185,0,device)
				print key,i
		pass
	else:
		for key,value in levelcnt.items():
			for i in xrange(value):
				click(580,230+170*(key-1),0,device)
				click(360,790,0,device)
				print key,i
	pass
	exit(1)

##16 1000, 530
##17
def dragontower(device=''):

	for i in range(1,20):
		print i
		click(800, 600,0,device)
		
		#click(1000, 530,8)
		click(990, 600,8,device)
		
		if i%3==0:
			click(560, 1325,3,device)
			click(560, 1325,1,device)
		else:
			click(560, 1325,1,device)
	exit()
def repeat(func,cnt):
	for i in xrange(cnt):
		func()
def iron():
	#pts=[(345,845)]
	x=85
	y=110
	#pts=[(315-15,675),(0455-15,705),(285-15,780),(415-15,830),(540,800)]
	pts=[(430,705),(285-15,780),(415-15,830),(540,800)]
	for pt in pts:
		click(pt[0], pt[1])
		click(pt[0]+x, pt[1] +y)
		click(500, 1055)
		click(pt[0], pt[1]-60,1)
def upgrade():
	#pts=[(760,795),(620,885),(600,1070),(435,1200),(670,1205)]
	pts=[(620,885),(600,1070),(435,1200),(670,1205)]
	for pt in pts:
		click(pt[0], pt[1],0.5)
		click(pt[0], pt[1]+150,0.5)
		click(760, 1580,0.5)
		click(pt[0], pt[1]-60,1)
def upgradefarm():
	h=120
	w=140
	#pts=[(605,1030),(420,960),(300,1070)]
	pts=[(300,1070)]
	for pt in pts:
		click(pt[0], pt[1],0.5)
		click(pt[0]+w, pt[1]+h,0.5)
		click(760, 1580,0.5)
		click(pt[0], pt[1]-60,1)
def longyunshi(device=''):
	if(isBig(device)):
		pts=[(170+i*180,1495) for i in range(5)]
		pts.extend([(170+i*180,1495+200) for i in range(5)])
		pts.extend([(170+i*180,1495+370) for i in range(5)])
		for pt in pts:       
			print pt[0], pt[1]
			click(pt[0], pt[1])
			click(535, 1286)
			click(575, 1205,1.5)
			
		pass
	else:
		pts=[(110+i*120,990) for i in range(5)]
		pts.extend([(110+i*120,990+130) for i in range(5)])
		for pt in pts:
			print pt[0], pt[1]
			click(pt[0], pt[1])
			click(360, 855)
			click(370, 785,1.5)
	exit(0)
def attackmonster(device=''):
	if(isBig(device)):
		pts=[(73,1271),(120,1415),(500,1820),(534,984)]
		for pt in pts:
			print pt[0], pt[1]
			click(pt[0], pt[1])
		sleep(2)
		click(530,1342,1)
		click(325, 705,1)
		click(630, 800,0.5)
		click(800, 1800)
		pass
def sd(cnt):
	for i in xrange(cnt):
		click(550,870,0)
		click(540,690,0.5)
def callnames(device=''):
	if isBig(device):
		for i in xrange(0,1000):
			slide(470,1870,470,1870,2000,device)
			click(110,1745,1,device)
			sendtext(str(i),1,device)
			click(1010,1856,1,device)
	else:
		for i in xrange(0,1000):
			slide(340,1240,340,1240,2000,device)
			click(100,1120,1,device)
			sendtext(str(i),1,device)
			click(675,1230,1,device)
def multido(func,paras={}):
	
	pool=Pool(5)
	for d in getdevices():
		print d
		pool.apply_async(func,[d]+paras)
	pool.close()
	pool.join()

	exit(0)

def getdevices():
	ret= CMD("adb devices").split("\r\n")[1:]
	devices= map(lambda x: x.split("\t")[0],ret)[:-2]
	return devices
def test(a,b):
	pool=Pool(5)
	for i in getdevices:
		pool.apply_async(getVIP,[{4:100},i])
	pool.close()
	pool.join()

	exit(0)
def getgoldfrom_taobao(device=''):
	#start taobao
	CMD("adb shell am start com.taobao.taobao/com.taobao.tao.homepage.MainActivity3")
	sleep(5)
	#goto page
	click(540,840,3,device)
	#get gold
	click(540,340,0,device)
	exit()
def getfuncname(func):
    def run(*argv):
       print func.__name__
       if argv:
            ret = func(*argv)
       else:
            ret = func()
       return ret
    return run
def getfuncname1(func):
	print func.__name__
@getfuncname1
def t(a):
    print a 
@getfuncname1
def sds():
	pass


from PIL import Image
def VerifyPic(image_path="2018-06-07-15_55_05.png"):
    i=0

    image = Image.open(image_path)
    print image.getpixel((288,1412))
    print image.getpixel((803,1407))
    if set(image.getpixel((288,1412))) & {152, 139, 89,0}:
        i=i+2
        print i
    if set(image.getpixel((803,1407))) & {164, 146, 98,0}:
        i=i+1
        print i
    return i

def douniformjob(device=''):
	ret=VerifyPic(snap(device))
	if ret == 3 or ret == 1:
		click(803,1407,1,device)
	elif ret == 2:
		click(288,1412,1,device)
	else:
		click(560,1210,1,device)	


if __name__ == '__main__': 
	rednote='BIIN75BAJNHUNBTO'  
	red3='4f72e03a7cf3'
	red2='139124717d22'
	device4='127.0.0.1:21503'
	d="127.0.0.1:62001"
	mi6='1f33ee18'

	#s=[1,2,3,4,5]
	#print s[-1]

	#getgoldfrom_taobao()
	#
	# slide(280,680,440,830,100,'127.0.0.1:62026')
	# slide(440,830,440,830,500,'127.0.0.1:62026')
	# slide(440,830,440,985,100,'127.0.0.1:62026')
	# exit()
	#snap('127.0.0.1:62026')
	#getVIP(mi6,{4:400})
	#multido(getVIP,[{4:400}])
	snap(mi6)
	exit(0)

	#multido(callnames)
	#print ge  tdevices()
	#multido(wechat,[])

	# pool=Pool(5)
	# for i in getdevices():
	# 	print i
	# 	pool.apply_async(callnames,(i,))
	# pool.close()
	# pool.join()

	#multido(test,['a','b'],[(1,2)])
	#exit()
	#map(lambda x:isBig(x),[red3,red2])
	#sd(41)
	#iron()
	#longyunshi()
	#wechat()
	#attackmonster()
	snap()
	
	#repeat(upgradefarm,5)
	
	#dragontower("1f33ee18")
	#repeat(iron, 5)

	#usegoods(72)
	# for i in xrange(200):
	# 	#attack1()
	# 	click(360, 830)
	#
	#AllianceMemeber('MIR')
	#getdb('me','mi')
	#getdb(9)
	#str=
	#getdb(4)
	#getuserinfo("1050734065001343")

	# startborn()
	
	#getVIP({1: 300},True)


	#getVIP({4:200})

	#monster_report_parse()
	#battleparse(getdb('me','mi'))
	#print getdb('me','mi')
	#AllianceMemeber("KRA")
	#AllianceLastLogin("MPE")
	#UserLastLogin()

	#os.system("adb shell input tap 360 620")
	#attack(red3)
	#snap()

	#AllianceMemeber("LSC")
	# for i in xrange(20):
	# 	wechat()


	
	# while 1:
	# 	multido(help,devices)
	# snap()
	# startcok()
	# sleep(20)
	#backkey("127.0.0.1:62001")

	#getgift("127.0.0.1:62001")
	#slide(10,400,360,400,500,"127.0.0.1:62001")
	#changeinputmothod(red2)
	# for i in xrange(20):
	# 	wechat()
	# conn = sqlite3.connect(str)
	# cursor = conn.execute("select datetime(createTime,'unixepoch','localtime'),channelid from Mail order by id  limit 1,100 ")
	# for row in cursor:
	# 	print row
	# exit(0)

	# print "start"

	# startcok(5)
	# backkey(red3)
	# sleep(20)
	#changeinputmothod("hacker")
	#changeaccount('cokhxl0001',red3)
	# click(300,1230,0,red3)
	# backkey(red3)
	# for i in xrange(10):

	# 	sendtext("%dh0llo%d"%(i,i),red3)
	# 	click(680,1230,0,red3)
	# 	sleep(1)
	#enter(0,red3)
	# daka(red3)
	# snap(red3)
	# daka(red3)
	# startcok()
	#slide(200,700,600,700,600)
	#
	# enter()
	#click(350,180,0)	#enter input
	#click(346,755,0) #change en
	
	# upgradefarm()
	# upgradewood()
	# exit(0)
	#for i in xrange(20):

	#updatesilver()
	#exit(0)
	#farmerupdate(device2)
	#helpall()
	#getdayrewards()
	#exit(0)
	# results=os.popen('adb devices')
	# for d in results.readlines()[1:]:
	# 	print d.strip()  
	# 	for i in d.split(' '):
	# 		print i
	# #etdayreward('127.0.0.1:62001')
	
	#getdayreward(device1)
	#
	#thread.start_new_thread(helpall,())
	
		#sleep(1)
	
	job = 9
	if job==0:
		snap("")
	elif job == 2:
		startborn(rednote)
	elif job == 1:
		getdayrewards()
	elif job == 3:
		getgifts()
	elif job == 4:
	#	helpall()
		for i in xrange(0,50):
			scure(red3)
	elif job == 5:
		getdayreward(red3)
	elif job == 6:
		keephelpall()
	elif job == 7:
		batch_changeid()
		#changeaccount('cokhxl0006',red3)
	elif job == 8:
		logging.info('你好')
		for i in xrange(0,3):
			batch_update(red3)
	elif job == 9:
		for i in xrange(0,70):
			getsoldier()
			sleep(1)
			back()
			print i
	elif job == 10:
		updatesilver()
	elif job == 11:
		getdb(1)
	elif job == 12:
		for i in xrange(20):
			wechat()
			print i
	elif job == 23:
		cnt=0
		while 1:
			
			print cnt
			for i in devices:
				helpall(i) 
			cnt+=1
			sleep(5)
	elif job== 24: #get vip
		for i in range(17):
			click(800, 1065, 0)
			click(555, 1185, 1)
			print i
	elif job == 99:
		y=[
		430,
		670,
		900,
		1145
		#1380
		]
		p1s=[(780,340),(780,580),(780,820),(780,1050),(780,1290)]
		for j in xrange(0,7):
			click(600,1015,0.5,device1)
			click(765,1095,0.5,device1)
			for i in y:
				slide(900,i,300,i,500,device1)

			click(790,580,1,device1)
			os.system('adb -s BIIN75BAJNHUNBTO shell input text 400')
			os.system('adb -s BIIN75BAJNHUNBTO shell input keyevent 66')
			click(900,1830,1,device1)
			click(605,888,1,device1)

			for d in devices:
				click(375,1220,0,d)

			sleep(5)





'''
;select count(*) from Mail where ChannelID='fight' and Titletext='攻城大败';
;update Mail set Status='1' where ChannelId='fight' and Status='0';
select * from Mail where ChannelID='fight';
;delete from Mail where ChannelId='fight' and titletext='攻城大败';


SELECT datetime(1377168853, 'unixepoch', 'localtime');时间戳转时间

看资源报告
select UnreadCount from Channel where ChannelId='resource' ;

国频发言
select datetime(b.CreateTime, 'unixepoch', 'localtime') as Time,a.NickName,a.Alliancename,b.Msg from User a,Chat_facec66ba0122eff356b153cfb92d511 b where a.userid=b.userid;
Mail:
title=1 被侦查

'''