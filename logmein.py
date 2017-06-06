#!/usr/bin/env python

import Login
import argparse
import sys
import re

# log.py <user> <pass>
#   Log into All Accounts with <user> <pass>
#
# log.py [-tfyg] <user> <pass>
#   Log into Twitter|Facebook|Gmail|Yahoo with <user> <pass>
#
# log.py [-tfgy] -i <file>
#   Log into All Accounts|Twitter|Facebook|Gmail|Yahoo with credentials from <file>
#   <file> format is 'user:pass'

# ( (-t, -f, -g, -y), -a )* ; ((!username,!password), -i)*

def msg():
    return "usage: %s [-h] [ [-a] | [-t] [-f] [-g] [-y] ] ( [-i FILE ] | username password )" % ( sys.argv[0] )

def getArgs():
    parseit = argparse.ArgumentParser(description="Log into any of FB, Twitter, Gmail, and Yahoo using <username> and <password>",usage=msg())

    parseit.add_argument('-a','--all', action='store_true',help="Log into all accounts")
    parseit.add_argument('-t','--twitter', action='store_true',help="Log into Twitter")
    parseit.add_argument('-f','--facebook', action='store_true',help="Log into Facebook")
    parseit.add_argument('-y','--yahoo', action='store_true',help="Log into Yahoo")
    parseit.add_argument('-g','--gmail', action='store_true',help="Log into Gmail")
    parseit.add_argument('-i','--file', dest="input_file",help="Log in with credentials in file with format as 'username:password'")
    parseit.add_argument("username",type=str,nargs='?',default="",help="Username to log in as")
    parseit.add_argument("password",type=str,nargs='?',default="",help="Password to log in with")
    
    args = parseit.parse_args()
    site_opt = (args.twitter or args.facebook or args.yahoo or args.gmail)

    if args.all and site_opt: # -a used with other site opts
        print msg()
        print "%s: error: argument -a/--all: not allowed with the arguments: -t/--twitter -f/--facebook -y/--yahoo -g/--gmail" % (sys.argv[0])
        return None

    if (args.input_file is not None): # input file added
        if (args.username != "" or args.password != ""): # if -i used with username and password args
            print msg()
            print "%s: error: argument -i/--file: not allowed with the arguments: username password" % (sys.argv[0])
            return None
    else: # no input file
        if (args.username == "" or args.password == ""): # if no "-i FILE" or "username and password"
            print msg()
            print "%s: error: the following arguments are required: username password" % (sys.argv[0])
            return None

    return args

def check_fformat(infile):
    r = re.compile('^.*:.*$')
    f = open(infile,'r')
    
    numlines = sum(1 for line in f)
    f.seek(0)

    for count,line in enumerate(f):
        if (line.count(':') == 1) and (r.match(line) is None):
            print "%s: error: expects format 'user:pass': Line %d " % (sys.argv[0],count+1)
            return -1
    
    f.close()
    return numlines

def log_into(args, client):
    unsuccessful = []
    successful = []

    chosen = [ k for k,v in vars(args).items() if isinstance(v,bool) if v ]
    for site in chosen: # not empty
        if client.login(site, args.username, args.password) == 1:
            successful.append(site)
        else:
            unsuccessful.append(site)
    
    print "Logged into %d sites: %s" %  ( len(successful), ",".join(successful) )

def main():
    max_lines = 0
    creds = []
    f = None

    args = getArgs()
    login_client = Login.Login()
    
    if (args is None):
        return -1
    
    if (args.input_file is not None):
        f = open(args.input_file)
        max_lines = check_fformat(args.input_file)
        if max_lines == -1: 
            return -1
        
    uname = args.username
    pword = args.password

    while (args.input_file is not None) or (uname != "" and pword != "") :
        if (uname != "" and pword != ""): 
            log_into(args, login_client)
            break

        try:
            line = f.readline().split(":")
        except (EOFerror):
            break
        
        args.username = line[0]
        args.password = line[1]
        log_into(args,login_client)

    if f is not None: f.close()


if __name__ == "__main__":
    main()
