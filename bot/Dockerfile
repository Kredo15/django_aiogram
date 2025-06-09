FROM python:3.11
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY .. .
CMD ["python", "main.py"]
CMD ["celery", "-A", "celery_queue.tasks", "worker", "--loglevel=info"]
