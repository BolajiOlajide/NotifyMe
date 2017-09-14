import random
import time

import requests
from flask import Flask, jsonify, url_for
from bs4 import BeautifulSoup #Doc: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

from task import make_celery
from sms import send_sms

app = Flask(__name__)
app.config.update(
	CELERY_BROKER_URL='redis://localhost:6379',
	CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

@celery.task()
def add_together(a, b):
	time.sleep(120)
	return a + b

@app.route('/add', methods=['POST'])
def add():
	result = add_together.apply_async(args=[1,2], countdown=1200)
	return jsonify({'status': 202, 'task_id': result.state}, 202)


@app.route('/')
def index():
	return 'Hello!'


@celery.task(bind=True)
def scraper(self): 
	html = requests.get('http://tooxclusive.com/').text
	soup = BeautifulSoup(html, "html.parser")

	# All songs are in a div called `post` that is surrounded by an outer div caled
	# `loop`
	songs = soup.find("div", id="loop").findAll("div", class_="post")
	print('KKKKK =============>>> .........')

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

		time.sleep(120)
		  
	return result

@celery.task(bind=True)
def long_task(self):
	"""Background task that runs a long function with progress reports."""
	verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
	adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
	noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
	message = ''
	total = random.randint(10, 50)
	for i in range(total):
		if not message or random.random() < 0.25:
			message = '{0} {1} {2}...'.format(random.choice(verb),
											  random.choice(adjective),
											  random.choice(noun))
		self.update_state(state='PROGRESS',
						  meta={'current': i, 'total': total,
								'status': message})
	return {'current': 100, 'total': 100, 'status': 'Task completed!',
			'result': 42}

@app.route('/task', methods=['POST'])
def longtask():
	task = long_task.apply_async()
	return jsonify({}), 202, {'Location': url_for('taskstatus',
												  task_id=task.id)}

@app.route('/scraper', methods=['POST'])
def scrape_data():
	posts = scraper.apply_async(countdown=1200)
	return jsonify({}), 202, {'Location': url_for('taskstatus',
												  task_id=posts.id)}

@app.route('/status/<task_id>')
def taskstatus(task_id):
	task = long_task.AsyncResult(task_id)
	if task.state == 'PENDING':
		response = {
			'state': task.state,
			'current': 0,
			'total': 1,
			'status': 'Pending...'
		}
	elif task.state != 'FAILURE':
		response = {
			'state': task.state,
			'current': task.info.get('current', 0),
			'total': task.info.get('total', 1),
			'status': task.info.get('status', '')
		}
		if 'result' in task.info:
			response['result'] = task.info['result']
	else:
		# something went wrong in the background job
		send_sms('08101644645', 'Your scraping is complete.')
		response = {
			'state': task.state,
			'current': 1,
			'total': 1,
			'status': str(task.info),  # this is the exception raised
			'message': 'An SMS has been sent to your mobile.'
		}
	return jsonify(response)


if __name__ == '__main__':
	app.run(debug=True)
