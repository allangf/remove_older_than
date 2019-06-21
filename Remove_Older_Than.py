# -*- coding: latin-1 -*-
'''
Company:				Altair Brasil

Copyright:				TODOS OS DIREITOS RERVADOS.
						ALL RIGHTS RESERVED.
						
Project:				REMOVING OLDER FILE
File:					Remove_Older_Than.py
Author:					Allan Fernandes
Date created			07/11/2018
Purpose:				Will keep just newer files and folders in root specified and recreate folders structures define in config file
OS:						Win/Linux
HW Version:			
PBS Version:
TCL/TK Version:
Python Version:			2.7.x

Date 			Author 				Revision
07/11/2018		Allan Fernandes		1.2		

Improvement:
Instructions: To use configuration file, in same directory that script was created insert directories that will need to be recreate (./config/Remove.conf)
              To use ignore path, in the same directory that script was created insert the full path that whant be ignored(./config/Ignore.conf)
'''
import os
import sys
import time
import datetime

if len(sys.argv) != 3:
    print "usage", sys.argv[0], " <dir> <days>\n\t Will keep files less than <days>."
    sys.exit(1)

if not os.path.exists((sys.argv[0])[:-20] + "config"):
    os.mkdir((sys.argv[0])[:-20] + "config")

if not os.path.exists((sys.argv[0])[:-20] + "log"):
    os.mkdir((sys.argv[0])[:-20] + "log")

ignored_path = []
if os.path.isfile((sys.argv[0])[:-20] + "config\\Ignore.conf"):
    ignored_path = open((sys.argv[0])[:-20] + "config\\Ignore.conf", 'r').read().splitlines()
    if ignored_path:
        log = open((sys.argv[0])[:-20] + "log\\" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + "_Ignored_Folders.log", 'w')
        for ignored in ignored_path:
            log.write(ignored + "\n")
        log.close()

log = open((sys.argv[0])[:-20] + "log\\" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + "_Remove_Files.log", 'w')
log.write("Date created\t\tDate modified\t\tName\n")
for root, dirs, files in os.walk(sys.argv[1]):  
    for filename in files:
        file = (os.path.join(root, filename))
        control_ignored = True	
        for ignored in ignored_path:
            if ignored in file:
                control_ignored = False
        if control_ignored:
            try:
                stat = os.stat(file)
            except (IOError, WindowsError, Exception), err:
                    error = open((sys.argv[0])[:-20] + "log\\Remove_Files_Error.log", 'a+')
                    error.write(datetime.datetime.fromtimestamp(stat.st_ctime).strftime("%m/%d/%Y %I:%M %p") + "\t" + datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%m/%d/%Y %I:%M %p") + "\t" + file +" "+ str(err) + "\n")
                    error.close()
            filedate= stat.st_ctime
            if stat.st_ctime < stat.st_mtime:
                filedate = stat.st_mtime
            if filedate < (time.time() - (int(sys.argv[2]) * 24 * 60 * 60)):
                log.write(datetime.datetime.fromtimestamp(stat.st_ctime).strftime("%m/%d/%Y %I:%M %p") + "\t" + datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%m/%d/%Y %I:%M %p") + "\t" + file +" \n")
                try:
                    os.remove(file)
                except (IOError, WindowsError, Exception), err:
                    error = open((sys.argv[0])[:-20] + "log\\Remove_Files_Error.log", 'a+')
                    error.write(datetime.datetime.fromtimestamp(stat.st_ctime).strftime("%m/%d/%Y %I:%M %p") + "\t" + datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%m/%d/%Y %I:%M %p") + "\t" + file +" "+ str(err) + "\n")
                    error.close()
log.close()
log = open((sys.argv[0])[:-20] + "log\\" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + "_Remove_Folders.log", 'w')
log.write('Date created\t\tDate modified\t\tName\n')
empty=[]
for root ,dirs ,files in os.walk(sys.argv[1]):
	for dir in dirs:
		dir = os.path.join(root,dir)
		if not os.listdir(dir):
		    empty.append(dir)

empty.sort(key=len, reverse=True)

for path in empty:
    empty.remove(path)
    stat = os.stat(path)
    log.write(datetime.datetime.fromtimestamp(stat.st_ctime).strftime("%m/%d/%Y %I:%M %p") + "\t" + datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%m/%d/%Y %I:%M %p") + "\t" + path + "\n")
    os.rmdir(path)
log.close()

log = open((sys.argv[0])[:-20] + "log\\" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + "_Remove_Path.log", 'w')

if os.path.isfile((sys.argv[0])[:-20] + "config\\Remove.conf"):
    folders = open((sys.argv[0])[:-20] + "config\\Remove.conf", 'r').read().splitlines()
    for folder in folders:
        log.write(sys.argv[1] + "\\" + folder)
        if os.path.exists(sys.argv[1] + "\\" + folder):
            log.write(" EXISTS\n")
        else:
            if "\\" in folder:
                path = folder.split("\\")
                pfolder = ""
                for f in path:
                    pfolder += f + "\\" 
                    os.mkdir(sys.argv[1] + "\\" + pfolder)
            else:
                    os.mkdir(sys.argv[1] + "\\" + folder)
            log.write(" CREATED\n")				
else:
    config = open((sys.argv[0])[:-20] + "config\\Remove.conf", 'w')
    config.write('\n')
    config.close()
log.close()
sys.exit(0)
