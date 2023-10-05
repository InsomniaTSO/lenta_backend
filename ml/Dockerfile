FROM python:3.7
RUN apt-get update && apt-get -y install cron vim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
COPY test.py test.py
COPY api_host.py api_host.py
RUN echo $PYTHONPATH
# run crond as main process of container
CMD ["cron", "-f"]