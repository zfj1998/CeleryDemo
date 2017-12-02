source ../environment/celerydemo/bin/activate
cd CeleryDemo
celery -A demoNo1 worker --loglevel=info
