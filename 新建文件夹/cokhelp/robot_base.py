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
import get_pos
reload(sys)
sys.setdefaultencoding("utf-8") 
class AndroidRobot(object):
	def __init__(self,device=''):
		self.device=device
	def CMD(self,cmd):
		res=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
		out,err= res.communicate()
		if err == None:
			if len(out.split('\n'))>=1:
				return out

	def click(self,x,y,t=0):
		os.system('adb %s shell input tap %d %d'%(('-s %s')%self.device if self.device <> '' else '',x,y))
		sleep(t)
	def key(self,key,t=1):
		if self.device=='':
			os.system('adb shell input keyevent %s'%(key))
		else:
			os.system('adb -s %s shell input keyevent %s'%(self.device,key))
		sleep(t)
	def slide(a,b,c,d,t=500):
		if self.device=='':
			os.system('adb shell input swipe %d %d %d %d %d '%(a,b,c,d,t))
		else:
			os.system('adb -s %s shell input swipe %d %d %d %d %d '%(self.device,a,b,c,d,t))

	def tab(self,t=1):
		self.key(61,t)
	def sendtext(self,text):
		os.system("adb %s shell input text %s"%('-s %s'%self.device if self.device <> '' else '',text))
	def startcok(self,t=0):
		os.system("adb %s shell am start com.hcg.cok.cn360/com.clash.of.kings.COK"%(('-s %s')%self.device if self.device <> '' else ''))
		sleep(t)
	def backkey(self,t=1):
		self.key(4,t)
	def enterkey(self,t=0):
		self.key('66',t)
	def back(self,t=1):
		if device=='':
			self.click(50,50,t,self.device)
		else:
			self.click(50,50,t,self.device)
	def donate(self):
		self.enteralliance()
		self.click(536,1720,1)
		self.click(600,1620,1)
  		for i in xrange(17):
			#print i
			self.click(560,1240,2)
		self.backkey()
		self.backkey()
		self.backkey()
	def changeid(self,user=''):
		self.click(1067,1212,2)#float btn
		self.click(500,1200,1)
		self.click(660,845,0)#delete 
		self.sendtext(user)

		self.enterkey()
		self.sendtext('890219')
		self.enterkey()
		#self.click(510,1020,1)
		sleep(20)
		#click(1020,55,1)
		self.backkey(2)
		sleep(3)
	def getdailyreward(self):
		self.click(990,425,3)
		self.click(560,1777,1)
		self.backkey()
		sleep(3)
	def enteralliance(self):
		self.click(970,1860,1)#进入联盟
	def tasklist(self):
		self.click(30,960,1)#点击任务列表
		self.click(680,441,1) #卸货
		self.click(550,1090,1)

		self.click(30,960,3)#点击任务列表
		self.click(670,720,3)#水晶转盘
		self.click(300,1850,2)#

		self.backkey(3)

		self.click(30,960,3)#点击任务列表
		self.click(675,640,3)#精铁转盘
		self.click(810,1135,2)
		self.click(300,1850,2)#
		self.backkey(3)
	def zhaojiling(self):
		t=3
		self.click(1010,590,t)
		self.click(525,1583,t)
		self.click(540,1855,t)
		self.click(1000,97,t)


		self.click(860,700,1)
		self.click(380,1130,2)
		self.click(550,1130,2)
		self.click(720,1130,2)

		self.backkey(2)
	def getalliancetaskreward(self):
		self.click(970,1860,1)#进入联盟
		self.click(520,1600,1)##进入联盟任务
		self.click(550,1835,1)#一键领取
		self.click(780,195,1)#随机任务
		self.click(550,1835,1)#一键领取
		self.backkey()
		self.backkey(2)
	def magic(self):
		self.click(30,950,2) #click work float
		self.click(670,910,2) #魔法学院
		self.click(730,1130,2)
		self.click(260,830,1)
		self.click(810,1460,1) #confirm
		if 1:
			self.click(260,1630,1)
			self.click(810,1460,1) #confirm

		self.backkey()
		sleep(3)
	def dailytaskreward(self):
		for x in [240,430,620,810,1000]:#for mi
			self.click(x,830,1)
			self.click(522,1522,1)
	def dragontower(self,start=1,end=30):
		for i in range(start,end):
			print i
			self.click(800, 600,0)
			
			#click(1000, 530,8)
			self.click(990, 600,9)
			
			if i%3==0:
				self.click(560, 1325,3)
				self.click(560, 1325,4)
			else:
				self.click(560, 1325,4)
if __name__ == '__main__':

	#for d in ['127.0.0.1:6555','127.0.0.1:62025']
	# r1=AndroidRobot('127.0.0.1:6555')#'127.0.0.1:62025'
	# r2=AndroidRobot('127.0.0.1:62025')
	# # r.changeid('cokhxl6004')
	# while(1):
	# 	r1.click(560,1850,1)
	# 	r2.click(560,1850,1)
	device='127.0.0.1:62001'
	r=AndroidRobot(device)
	# #r.getdailyreward()
	# # r.tasklist()
	# r.donate()
	# r.zhaojiling()
	#r.getalliancetaskreward()
	#r.dailytaskreward()
	# r.zhaojiling()
	r.dragontower(1,35)
	exit()
	for user in [#'cokhxl6001',
	#'cokhxl6002',
	#'cokhxl6003',
	'cokhxl6004',
	'cokhxl6005',
	'cokhxl6011','cokhxl6012','cokhxl6013','cokhxl6014',
	'cokhxl6015','cokhxl6016','cokhxl6019','cokhxl6018',
	]:
		r.changeid(user)
		r.getdailyreward()
		r.zhaojiling()
		#r.tasklist()
		r.getalliancetaskreward()
		
		


	#r.donate()
	#print get_pos.compare("C:\Users\Administrator\Nox_share\Image\Screenshot_20190211-222619.png",'xiehuo.png')