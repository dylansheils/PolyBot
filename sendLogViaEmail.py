#!/usr/bin/python
import sys
import os
import time
import subprocess

import pip

name = sys.argv[1]
sender = sys.argv[2]

fileObj = open("tempLogParsed.txt", "r", encoding="utf-8")
log = fileObj.read()
fileObj.close()
os.remove("tempLogParsed.txt")
time.sleep(.5)

import yagmail

username = "thebest.polybot@gmail.com"
password = "thePolyBot2000"

log = log.replace("“", "'")
log = log.replace(u"\u2018", "'")
log = log.replace(u"\u2019", "'")

yag = yagmail.SMTP(username, password)

contents = [log]

yag.send(sender, 'PolyBot Result for ' + name + ": ", contents)
