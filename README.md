# NotifyMe

### Starting The Celery Worker
- To do this simply use the command `celery -A manage.celery worker` to start the Celery worker.
Ensure you have your redis server running locally, if not start it with `redis-server`.

### Why Celery?

Running background tasks through **Celery** is not as trivial as doing so in threads. But the benefits are many, as Celery has a distributed architecture that will enable your application to scale. A Celery installation has three core components:

The Celery client. This is used to issue background jobs. When working with Flask, the client runs with the Flask application.
The Celery workers. These are the processes that run the background jobs. Celery supports local and remote workers, so you can start with a single worker running on the same machine as the Flask server, and later add more workers as the needs of your application grow.
The message broker. The client communicates with the the workers through a message queue, and Celery supports several ways to implement these queues. The most commonly used brokers are RabbitMQ and Redis.


### Author
**Bolaji Olajide**