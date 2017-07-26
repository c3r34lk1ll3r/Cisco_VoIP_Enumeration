import requests
import os
import time
import sys
import getopt

def enum(host,oui,direc,sle):
	looper=int("f"*(12-len(oui)),16)
	for i in range(0,12-len(oui)):
		oui+='0'
	oui=int(oui,16)
	counter=0
	voc=[]
	while counter <= looper:
		filename="SEP"+format(oui,'012x').upper()+".cnf.xml.sgn"
		oui+=1
		counter+=1
		r=requests.get("http://"+host+"/"+filename)
		print("Trying:"+r.url,end='\r')
		if r.status_code == 200:
			print ("\nFile "+filename+" Found");
			voc.append(filename)
			f=open(direc+"/"+filename,"w")
			f.write(r.text)
			f.close()
		if sle:
			time.sleep(sle)
	print("\n\n-------------")
	if len(voc) == 0:
		print("No file found");
	else:
		print("Files found:");
		for i in voc:
			print("\t"+i)

def Usage(name):
	print ("Cisco VoIP Enumeration  v1.0.0 - A tool for enumerate telephones on the network.")
	print ("Usage: "+name)
	print ("\t-h --help\t\t\tPrint this help.")
	print ("\t-u --url <gateway:port>\t\tDefine the gateway and port.")
	print ("\t-p --prefix <MAC prefix>\tStart enumeration from <MAC prefix> address.")
	print ("\t-s --sleep <sec>\t\tWait <sec> between a request and anothers.")
	print ("\t-d --dir <directory>\t\tTarget directory for storing configuration files.")


def ParseOpt(argv):
	
	settings={}
	settings['u']=None
	settings['d']="."
	settings['s']=0
	settings['p']="c80084"

	try:
		opts, args = getopt.getopt(argv[1:],"hu:d:s:p:",["help","url=","dir=","sleep=","prefix="])
	except getopt.GetoptError:
		Usage(argv[0])
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h' or opt in ("--help"):
			Usage(argv[0])
			sys.exit()
		elif opt in ("-u") or opt in ('--url'):
			inputfile = arg.strip()
			settings['u']=inputfile
		elif opt in ("-d") or opt in ("--dir"):
			inputfile=arg.strip()
			settings['d']=inputfile
		elif opt in ("-s") or opt in ("--sleep"):
			try:
				delay = float(arg)
			except:
				Usage(argv[0])
				sys.exit()
			settings['s']=delay
		elif opt in ("-p") or opt in ("--prefix"):
			prefix = arg.strip().replace(":","")
			settings['p']=prefix
	return settings

def main(argv):
	ret=ParseOpt(argv)
	if ret['u'] == None:
		print("Gateway address is mandatory\n\n");
		Usage(argv[0])
		sys.exit()
	hh=ret['u'].split(":")
	try:
		if len(hh) != 2 and int(hh[1])<0 or int(hh[1])> 65536:
			print("Gateway address is mandatory\n\n");
			Usage(argv[0])
			sys.exit()
	except:
		Usage(argv[0])
		sys.exit()
	if not os.path.exists(ret['d']):
		 os.makedirs(ret['d'])
		 
	enum(ret['u'],ret['p'],ret['d'],ret['s'])



if __name__ == "__main__":
	main(sys.argv)
