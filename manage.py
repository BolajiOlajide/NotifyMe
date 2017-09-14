from flask import Flask

from task import make_celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

@celery.task()
def add_together(a, b):
    return a + b

@celery.task()
def loop(array_one, array_two):
  result = []

  for item_one in array_one:
    for item_two in array_two:
      if item_one == item_two:
        result.append(item_two)

  return result


if __name__ == '__main__':
	app.run(debug=True)
