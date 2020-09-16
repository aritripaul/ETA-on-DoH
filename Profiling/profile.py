# profile.py
# Author: Gargi Mitra
# Function: Collects traffic samples of given webpage URLs

import io
import os
import sys
import subprocess

########################## take input parameters ################################

def exit_with_help(error=''):
    print("""\
Usage: profile.py [options]

options:
    -whole { /whole/ } : 1 = profile all webpages in the website, 0 = profile a specific set of pages
    -webdir { /webdir/ } : directory containing website map (output of navigation.py)
    -listfile { /listfile/ } : path to file containing list of webpages to profile (for whole = 0)
    -uplevel { /uplevel/ } : till what parent level profiling has to be done (for whole = 0) [default: 0]
    -downlevel { /downlevel/ } : till what child level profiling has to be done (for whole = 0) [default: 0]
 """)
    print(error)
    sys.exit(1)

# Arguments to be read from command line
args = [ ('whole', 'whole', 'whole'),
         ('webdir', 'webdir', 'webdir')]

# Checking if all variables are/will be set
for var, env, arg in args:
    if not '-'+arg in sys.argv:
        vars()[var] = os.getenv(env)
        if vars()[var] == None:
            exit_with_help('Error: Environmental Variables or Argument'+
                        ' insufficiently set! ($'+env+' / "-'+arg+'")')

uplevel = 0
downlevel = 0
listfile = ""

# Read parameters from command line call
if len(sys.argv) != 0:
    i = 0
    options = sys.argv[1:]
    # iterate through parameters
    while i < len(options):
        if options[i] == '-whole':
                i = i + 1
                whole = options[i]
        elif options[i] == '-webdir':
                i = i + 1
                webdir = options[i]
        elif options[i] == '-listfile':
                i = i + 1
                listfile = options[i]
        elif options[i] == '-uplevel':
                i = i + 1
                uplevel = options[i]
        elif options[i] == '-downlevel':
                i = i + 1
                downlevel = options[i]
        else:
            exit_with_help('Error: Unknown Argument! ('+ options[i] + ')')
        i = i + 1

if int(whole) == 0 and not listfile:
    exit_with_help('Error: Mention filename containing list of webpages to be profiled using -listfile option.')

############################ collect samples ##################################

if int(whole) == 0:
    urlipfile = open(listfile, 'r')
    urlcount =  1             # initializing urlcount
    for url in urlipfile:
        opfile = open("statistics",'a')
        opfile.write(url)
        opfile.close()
        for num in range (0,10):
	    command = "./firefox_collect_samples.sh '" + url.rstrip() + "' " + str(urlcount) + "_" + str(num) + " " + str(num)
            print command
            subprocess.call(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        urlcount = urlcount + 1
