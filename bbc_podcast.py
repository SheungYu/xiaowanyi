from splinter import Browser
from datetime import datetime
import urllib

archive_urls = ['http://www.bbc.co.uk/worldservice/learningenglish/general/sixminute/',
				'http://www.bbc.co.uk/worldservice/learningenglish/general/sixminute/2013/12/131212_6min_archive_2012.shtml',
				'http://www.bbc.co.uk/worldservice/learningenglish/general/sixminute/2013/01/130117_6min_archive_2011.shtml',
				'http://www.bbc.co.uk/worldservice/learningenglish/general/sixminute/2011/02/110215_6min_archive_2010.shtml',
				'http://www.bbc.co.uk/worldservice/learningenglish/general/sixminute/2011/01/110114_6min_archive_09.shtml',
				'http://www.bbc.co.uk/worldservice/learningenglish/general/sixminute/2010/01/100126_6min_archive_08.shtml']

with Browser() as browser:
	for archive_url in archive_urls:
		browser.visit(archive_url)
		teasers = browser.find_by_css('div.li-columnised div.ts-headline')
		podcasts = []
		for teaser in teasers:
			a = teaser.find_by_css('h3.ts-title a').first
			b = teaser.find_by_css('div.body').first

			date = datetime.strftime(datetime.strptime(b.text, '%d %B %Y'), '%Y-%m-%d')
			
			podcasts.append({'title': a.text, 'url': a['href'], 'date': date})
			
		for podcast in podcasts:
			print podcast['title']
			print podcast['url']        
			browser.visit(podcast['url'])
			audio_link = browser.find_by_css('a.audio-link').first
			audio_url = audio_link['href']
			script_link = browser.find_by_css('a.pdf-link').first
			script_url = script_link['href']
			
			file_name = '/root/bbc/%s %s' % (podcast['date'], podcast['title'])
			urllib.urlretrieve(audio_url, file_name + '.mp3')
			urllib.urlretrieve(script_url, file_name + '.pdf')
        
        
        
       
    
