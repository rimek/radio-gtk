#!/usr/bin/env python2

import os, sys
import fileinput

if os.getuid() != 0:
    print "You need to run this as root"
    sys.exit()

cwd = os.getcwd()
print "Creating symlink radio-gtk",
try:
    os.unlink('/usr/local/bin/radio-gtk')
except:
    pass
os.symlink("%s/main.py" % cwd, '/usr/local/bin/radio-gtk')
print "..done"

print "Changind working dir in main.py",
for line in fileinput.input("main.py", inplace=1):
    if line.find('os.chdir') == 0:
        print  "os.chdir('%s')" % (cwd)
    else:
        print line,
print "..done"
