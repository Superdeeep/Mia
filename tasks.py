# tasks.py

from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def send_message(message):
    print(f"Sending message: {message}")
    return message
