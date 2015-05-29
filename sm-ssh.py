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
		return False
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

def ssh_entry(hname):
	host_table=read_conf();
	info=host_table[hname]


def del_entry(hname):
	print "in del_entry"

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


def add_entry(host_info):
	host_table=read_conf()
	write_conf(host_table)

def usage():
	print "in usage"

def main(argv):
	opt,args=getopt.getopt(argv[1:],"a:d:ls:h",["add=","del=","list","ssh=","help"]);
	for name,value in opt:
		if name in ('-a','--add'):
			add_entry(value)
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