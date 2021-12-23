#!/usr/bin/python
import sys
import sys
import subprocess

import pip

name = sys.argv[1]
sender = sys.argv[2]
log = sys.argv[3]

import yagmail

username = "thebest.polybot@gmail.com"
password = "thePolyBot2000"

log = log.replace("“", "'")
log = log.replace(u"\u2018", "'")
log = log.replace(u"\u2019", "'")

yag = yagmail.SMTP(username, password)

contents = [log]

yag.send(sender, 'PolyBot Result for ' + name + ": ", contents)
