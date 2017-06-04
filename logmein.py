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
    return ""

def getArgs():
    parseit = argparse.ArgumentParser(description="Log into any of FB, Twitter, Gmail, and Yahoo using <username> and <password>",usage=msg())

    parseit.add_argument('-a','--all', action='store_true',help="Log into all accounts")
    parseit.add_argument('-t','--twitter', action='store_true',help="Log into Twitter")
    parseit.add_argument('-f','--facebook', action='store_true',help="Log into Facebook")
    parseit.add_argument('-y','--yahoo', action='store_true',help="Log into Yahoo")
    parseit.add_argument('-g','--gmail', action='store_true',help="Log into Gmail")
    parseit.add_argument('-i','--file', type=file, dest="input_file",help="Log in with credentials in file with format as 'username:password'")
    parseit.add_argument("username",type=str,nargs='?',default="",help="Username to log in as")
    parseit.add_argument("password",type=str,nargs='?',default="",help="Password to log in with")
    
    args = parseit.parse_args()
    site_opt = (args.twitter or args.facebook or args.yahoo or args.gmail)

    if args.all and site_opt:
        print msg()
        print "%s: error: argument -a/--all: not allowed with the arguments: -t/--twitter -f/--facebook -y/--yahoo -g/--gmail" % (sys.argv[0])
        return -1

    if (args.input_file is not None): # input file added
        if (args.username != "" or args.password != ""):
            print msg()
            print "%s: error: argument -i/--file: not allowed with the arguments: username password" % (sys.argv[0])
            return -1
    else: # no input file
        if (args.username == "" or args.password == ""): # if no user and pass
            print msg()
            print "%s: error: the following arguments are required: username password" % (sys.argv[0])
            return -1

    return args

def main():
     
    #login_client = Login.Login(username='',password='')
    #site.login(logsite)

if __name__ == "__main__":
	main()
