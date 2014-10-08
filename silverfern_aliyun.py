#!/usr/bin/python -u

# ########################################
# Function:    CMS self-defined monitor SDK
# Usage:       python cms_post.py ali_uid, metric_name, value, fields
# Author:      CMS Dev Team
# Company:     Aliyun Inc.
# Version:     1.0
# Description: Since Python 2.6, please check the version of your python interpreter
# ########################################
import sys
import time
import socket
import random
import urllib
import httplib
import json
import logging
from logging.handlers import RotatingFileHandler

REMOTE_HOST = 'open.cms.aliyun.com'
REMOTE_PORT = 80
REMOTE_MONITOR_URI = "/metrics/put"


def post(ali_uid, metric_name, metric_value, fields):
    # init logger
    logger = logging.getLogger('post')
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(filename="/tmp/post.log", mode='a', maxBytes=1024 * 1024, backupCount=3)
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    socket.setdefaulttimeout(10)

    # convert dimensions
    kv_array = fields.split(',')
    dimensions = {}
    for kv in kv_array:
        kv_array = kv.split('=')
        dimensions[kv_array[0]] = kv_array[1]
    json_str = json.dumps(dimensions)

    #current timestamp
    timestamp = int(time.time() * 1000)

    #concate to metrics
    metrics = '[{"metricName": "%s","value": %s, "unit": "None","timestamp": %s, "dimensions": %s}]' % (
        metric_name, metric_value, timestamp, json_str)
    print metrics

    params = {"userId": ali_uid, "namespace": "acs/custom/%s" % ali_uid, "metrics": metrics}

    #report at random 5 seconds
    interval = random.randint(0, 5000)
    time.sleep(interval / 1000.0)

    data = urllib.urlencode(params)
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Connection": "close"}
    exception = None
    http_client = None
    try:
        http_client = httplib.HTTPConnection(REMOTE_HOST, REMOTE_PORT)
        try:
            http_client.request(method="POST", url=REMOTE_MONITOR_URI, body=data, headers=headers)
            response = http_client.getresponse()
            if response.status == 200:
                return
            else:
                print "response code %d, content %s " % (response.status, response.read())
                logger.warn("response code %d, content %s " % (response.status, response.read()))
        except Exception, e:
            exception = e
    finally:
        if http_client:
            http_client.close()
        if exception:
            logger.error(exception)


###########################################################################################

from splinter import Browser
import schedule
import time

LOGIN_USER = 'chantz'
LOGIN_PASS = '723neoidea'

INTERVAL = 15 # minutes

MONITOR_ID = '1940355560597763'
MONITOR_ITEM = 'silverfern'

LOGIN_URL = 'https://www.immigration.govt.nz/secure/Login+Silver+Fern.htm'
SILVERFERN_URL = 'https://www.immigration.govt.nz/SilverFern/'

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
				post(MONITOR_ID, MONITOR_ITEM, 1, 'name=silverfern')
			else:
				print 'Congratulations, you got it!'
				post(MONITOR_ID, MONITOR_ITEM, 0, 'name=silverfern')
				print browser.html
		except HttpResponseError, e:
			print "Oops, I failed with the status code %s and reason %s" % (e.status_code, e.reason)
		except:
			print 'Oops, something wrong, I choose to ignore!!'

			import traceback
			print traceback.format_exc() 
	
			

if __name__ == '__main__':

	print '+++++++++++++++++++++ Scheduler start at %s +++++++++++++++++++++++++++' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

	schedule.every(INTERVAL).minutes.do(check_it)
	while True:
		schedule.run_pending()
		time.sleep(1)

