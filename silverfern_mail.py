#!/usr/bin/python -u

from splinter import Browser
from splinter.request_handler.status_code import HttpResponseError
import schedule
import time

LOGIN_USER = ''
LOGIN_PASS = ''

INTERVAL = 10 # minutes

MONITOR_ID = '1940355560597763'
MONITOR_ITEM = 'silverfern'

LOGIN_URL = 'https://www.immigration.govt.nz/secure/Login+Silver+Fern.htm'
SILVERFERN_URL = 'https://www.immigration.govt.nz/SilverFern/'

import smtplib,sys 
from email.mime.text import MIMEText

def send_mail(sub,content): 
	mailto_list=["***@foxmail.com"] 

	mail_host="smtp.qq.com"
	mail_user=""
	mail_pass=""
	mail_postfix="qq.com"


	me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
	msg = MIMEText(content,_charset='utf-8') 
	msg['Subject'] = sub 
	msg['From'] = me 
	msg['To'] = ";".join(mailto_list) 
	try: 
		s = smtplib.SMTP() 
		s.connect(mail_host) 
		s.login(mail_user,mail_pass) 
		s.sendmail(me, mailto_list, msg.as_string()) 
		s.close() 
		return True
	except Exception, e: 
		print str(e) 
		return False

def notify_unopened():
	if send_mail('Oops, Silver Fern Visa NO Opened```','Please login ' + LOGIN_URL + ', then visit ' + SILVERFERN_URL): 
		print 'email notify_unopened success'
	else: 
		print 'email notify_unopened failed'

def notify_opened(content):
	if send_mail('Silver Fern Visa Opened!!','Please login ' + LOGIN_URL + ', then visit ' + SILVERFERN_URL + '\n\n' + content): 
		print 'email notify_opened success'
	else: 
		print 'email notify_opened failed'

def check_it():
	
	with Browser('phantomjs') as browser:
		
		print '===================== Check start at %s ======================' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		
		try:		
			browser.visit(LOGIN_URL)
			browser.fill('OnlineServicesLoginStealth:VisaLoginControl:userNameTextBox', LOGIN_USER)
			browser.fill('OnlineServicesLoginStealth:VisaLoginControl:passwordTextBox', LOGIN_PASS)
			browser.find_by_name('OnlineServicesLoginStealth:VisaLoginControl:loginImageButton').first.click()
			browser.visit(SILVERFERN_URL)
			
			#print browser.html
		   
			if browser.title == 'Runtime Error':
				print 'Runtime Error, I choose to ignore!!'
			elif browser.is_text_present('Unfortunately at this time we are not accepting new applications', wait_time=2):
				print 'Oops, you have no luck!'
				#post(MONITOR_ID, MONITOR_ITEM, 1, 'name=silverfern')
				#notify_unopened()
			else:
				print 'Congratulations, you got it!'
				#post(MONITOR_ID, MONITOR_ITEM, 0, 'name=silverfern')
				notify_opened(browser.find_by_tag('body').first.text)
				
				print browser.html
		except HttpResponseError, e:
			print "Oops, I failed with the status code %s and reason %s" % (e.status_code, e.reason)
		except:
			print 'Oops, something wrong, I choose to ignore!!'

			import traceback
			print traceback.format_exc() 

		print '===================== Check end at %s ======================' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	
			

if __name__ == '__main__':

	print '+++++++++++++++++++++ Scheduler start at %s +++++++++++++++++++++++++++' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

	schedule.every(INTERVAL).minutes.do(check_it)
	while True:
		schedule.run_pending()
		time.sleep(1)
