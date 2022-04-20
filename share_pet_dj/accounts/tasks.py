from config.celery import app


@app.task
def send():
    pass
