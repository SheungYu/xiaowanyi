from splinter import Browser
from datetime import datetime
import re

archive_url = 'http://www.listen-to-english.com/index.php?atp=archive_atp'

with Browser() as browser:
	browser.visit(achive_url)
	lis = 

	podcasts = []
	for li in browser.find_by_css('div.post li'):
		a = li.find_by_css('a').first
		b = li.find_by_css('small').first

		date = re.match(r" posted on \w+ (.+)", b.text).group(1)
		date = datetime.strftime(datetime.strptime(date, '%d %B %Y'), '%Y-%m-%d')
		
		podcasts.append({'title': a.text, 'url': 'http://www.listen-to-english.com/' + a['href'], 'date': date})

	for podcast in podcasts:
		print podcast['title']
		print podcast['url']        
		browser.visit(podcast['url'])
		audio_link = browser.find_link_by_partitial_text('Download MP3').first
		audio_url = audio_link['href']
		#TODO
		script_div = browser.find_by_css('div.clearfloats').first
		script_url = script_link['href']
		
		file_name = '/root/listentoenglish/%s %s' % (podcast['date'], podcast['title'])
		urllib.urlretrieve(audio_url, file_name + '.mp3')
		urllib.urlretrieve(script_url, file_name + '.txt')


