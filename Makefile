install:
	cp sm-ssh.py /usr/local/bin/
	touch ~/.sm-ssh.conf
uninstall:
	-rm /usr/local/bin/sm-ssh.py
	-rm ~/.sm-ssh.conf

