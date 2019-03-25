# -*- coding:utf-8 -*-
#run.py  

from subprocess import * 
import threading 
import time
import pdb
micmd="adb shell sqlite3 /data/data/com.hcg.cok.cn360/files/245400909001793/database/Mail.db3"
cmd="adb pull /data/data/com.hcg.cok.mi/files/1137025688001343/database/Mail.db3 wo.db3"
p = Popen("cmd.exe",shell=True,stdin=PIPE,stdout=PIPE)
#p.stdin.write("tasklist\r\n")
p.stdin.write('adb  shell sqlite3 /data/data/com.hcg.cok.mi/files/1137025688001343/database/Mail.db3\r\n')
p.stdin.flush()
print p
#print p.stdout.readline()
out, err = p.communicate()
print out

p.stdin.write("select contents from Mail where channelid='dragonTower' order by createtime desc limit 1;\r\n")
out, err = p.communicate()
print out
time.sleep(5)
exit()
timeout=3
brun=True

def run1(expectstr=''):
    global p,brun
	
    result=''
    while brun:
        line = p.stdout.readline() 
        if not line:  #空则跳出
            break
        print(line)
        result+=line
        if expectstr in line:
            brun=False
before=''
def monitor():
	pass
result=''
brun=True
def run(expectstr=''):
	global p,result,brun
	
	# ret=p.stdout.readlines()
	# print ret
	# # result+=ret
	while brun:
		ret=p.stdout.readline()
		print ret.strip()#,len(ret)
		result+=ret
	#return ret
def test():
	global p,result,brun
	w =threading.Thread(target=run,args=('sqlite1>',))
	
	p.stdin.write('adb  shell sqlite3 /data/data/com.hcg.cok.mi/files/1137025688001343/database/Mail.db3\r\n')
	p.stdin.flush()
	#print p.stdout.readline()
	#time.sleep(1) #延迟是因为等待一下线程就绪
	p.stdin.write("select contents from Mail where channelid='dragonTower' order by createtime desc limit 1;\r\n")
	p.stdin.flush()
	print result
	w.start()
	time.sleep(1)
	brun=False
	#w.start()
#test()
class MyShell(threading.Thread):
	def __init__(self,cmd,expect=""):
		threading.Thread.__init__(self)
		self.p = Popen(cmd,shell=True,stdin=PIPE,stdout=PIPE)
		self.t = threading.Thread(target=run,args=(expect,))
	def sendcmd(self,cmd,expect=""):
	    pass
	@staticmethod
	def run(expectstr=''):
		global p,brun
		
		result=''
		while brun:
			line = p.stdout.readline() 
			if not line:  #空则跳出
				break
			print(">>>>>>",line)
			result+=line
			if expectstr in line:
				brun=False

test()


exit()
import threading

#定义函数

def fun_timer():
	print('hello timer')   #打印输出
	global timer  #定义变量
	timer = threading.Timer(1,fun_timer)   #60秒调用一次函数
	#定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名

	timer.start()    #启用定时器
timer = threading.Timer(1,fun_timer)  #首次启动
timer.start()