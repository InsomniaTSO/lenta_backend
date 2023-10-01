FROM python:3.10

COPY app.py /app
COPY model.py /app
COPY ml_model /app

WORKDIR /app    

RUN pip install -r requirements.txt

CMD ["python", "app.py"]