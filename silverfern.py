from splinter import Browser
from apscheduler.scheduler import Scheduler
import time


def check_opening():
    with Browser('chrome') as browser:
        print 'Check start at %s' % time.time()

        url = 'https://www.immigration.govt.nz/secure/default.htm'
        
        browser.visit(url)
        browser.fill('Footer:newFooter:loginControl:userNameTextBox', '')
        browser.fill('Footer:newFooter:loginControl:passwordTextBox', '')
        browser.find_by_name('Footer:newFooter:loginControl:loginImageButton').first.click()
        browser.visit('https://www.immigration.govt.nz/SilverFern/')
       
        if browser.is_text_present('Unfortunately at this time we are not accepting new applications', wait_time=2):
            print 'Oops, you have no luck!'
        else:
            print 'Congratulations, you got it!'


scheduler = Scheduler(standalone=True)
scheduler.add_cron_job(check_opening, minute='*/5')
scheduler.start()



