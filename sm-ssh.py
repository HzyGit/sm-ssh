#!/usr/bin/python

import sys
import getopt
import os
import socket

def get_conf_path():
	return os.path.join(os.environ['HOME'],".sm-ssh.conf");

def check_info(info):
	table_num=6
	if len(info)>table_num:
		return False
	if len(info)<1:
		return False
	try:
		socket.inet_pton(socket.AF_INET,info[1])
	except Exception as e:
		return True
	return True

def read_conf():
	path=get_conf_path()
	f=open(path)
	host_table={}
	try:
		for line in f:
			line=line.strip('\n')
			info=line.split(" ")
			if not check_info(info):
				continue
			host=info[0]
			host_table[host]=info[1:]
	finally:
		f.close()
	return host_table

def write_conf(table):
	path=get_conf_path()
	f=open(path,'w')
	try:
		for (d,x) in table.items():
			line=d+" "+" ".join(x)
			f.write(line+"\n")
	finally:
		f.close()

def ssh_exec(cmd,passwd):
	res=os.system("which sshpass > /dev/null 2>&1")
	if res==0:
		cmd="sshpass -p \""+passwd+"\" "+cmd
	else:
		print "not find sshpass, need to input the passwd"
	print cmd
	os.system(cmd)

def ssh_entry(hname):
	host_table=read_conf()
	try:
		info=host_table[hname]
	except Exception as e:
		print 'cannot find %s host' %hname
		return 
	for i in range(len(info)-5):
		info.append('')
	ip_i=0
	user_i=1
	passwd_i=2
	port_i=3
	cmd="ssh "
	if info[port_i] != '':
		cmd+="-p "+info[port_i]
	if info[user_i] !='':
		cmd+=" "+info[user_i]+"@"
	cmd+=info[ip_i]
	passwd=info[passwd_i]
	ssh_exec(cmd,passwd)

def del_entry(hname):
	host_table=read_conf()
	if hname in host_table.keys():
		del host_table[hname]
	else:
		print "\""+hname+"\""+" is not exists"
	write_conf(host_table)

def list_entry():
	host_table=read_conf()
	#print head
	table_num=6
	formart="%-15s %-20s %-20s %-20s %-10s %-30s"
	print formart %("name","host","user","passwd","port","note")
	print '----------------------------------------------------------------------------------------------------'
	for name,value in host_table.items():
		value=[name]+value
		v_len=len(value)
		v_len=table_num-v_len
		for i in range(v_len):
			value.append('')
		print formart %tuple(value[:table_num])


def add_entry(host,info):
	host_table=read_conf()
	if host in host_table.keys():
		print "\""+host+"\""+" has already exists!"
		return
	if len(info)==0:
		return
	host_table[host]=info
	write_conf(host_table)

def usage():
	print "Usage: sm-ssh.py [options] [hostname] [hostinfo]"
	print "\t manager remote host"
	print "\t -s,--ssh hostname             connect to remote host"
	print "\t -a,--add hostname hostinfo    add remote host"
	print "\t -d,--del hostname             del hostname"
	print "\t -h,--help                     display this information"

def main(argv):
	opt,args=getopt.getopt(argv[1:],"a:d:ls:h",["add=","del=","list","ssh=","help"]);
	for name,value in opt:
		if name in ('-a','--add'):
			add_entry(value,args)
		elif name in ('-l','--list'):
			list_entry()
		elif name in ('-d','--del'):
			del_entry(value)
		elif name in ('-s','--ssh'):
			ssh_entry(value)
		elif name in ('-h','--help'):
			usage()

if __name__ == "__main__":
	main(sys.argv)
