#!/usr/bin/python
import sys
import sys
import subprocess

msg = (sys.argv[1]).split('#')
name = sys.argv[2]
sender = sys.argv[3]
log = sys.argv[4]
gramMsg = (sys.argv[5]).split('#')



# Send the resulting email to the sender
from subprocess import call
call(["python", "sendLogViaEmail.py", name, sender, log])