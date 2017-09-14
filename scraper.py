import requests
from bs4 import BeautifulSoup #Doc: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

def scraper(): 
	html = requests.get('http://tooxclusive.com/').text
	soup = BeautifulSoup(html, "html.parser")

	# All songs are in a div called `post` that is surrounded by an outer div caled
	# `loop`
	songs = soup.find("div", id="loop").findAll("div", class_="post")

	headline = "There are {} new songs on TooXClusive".format(len(songs))
	result = []


	for song in songs:
		# I normally won't do this as Njira has warned me and made me scared of nested for loops
		# but I need this to take as long as possible for me to test this.
		info = BeautifulSoup(song.text, "html.parser")
		## Remove blank lines
		info = "".join([s for s in info.text.strip().splitlines(True) if s.strip()])
		post_title = info.splitlines()[2]
		body = info.splitlines()[3]

		data = {
			"title": post_title,
			"body": body
		}
		result.append(data)

		# This is here sjust to waste time, it is absolutely useless
		count = 0
		for number_one in range(7000):
			for number_two in range(5000):
				if number_one == number_two:
					count = count + 1
					
	return result
