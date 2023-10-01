import argparse
import json
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
@app.get('/')
def main():
    return HTMLResponse(content='TEST')

@app.get('/shops')
def stories():
    data = json.load(open(os.path.join(FILE_PATH, 'shops.json')))
    data['status'] = 'ok'
    return data 

@app.get('/categories')
def categories():
    data = json.load(open(os.path.join(FILE_PATH, 'categories.json')))
    data['status'] = 'ok'
    return data

@app.get('/sales')
def sales():
    data = json.load(open(os.path.join(FILE_PATH, 'sales.json')))
    data['status'] = 'ok'
    return data

@app.post('/forecast')
def forecast(data) -> dict:
    return 'ok'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=8000, type=int, dest='port')
    parser.add_argument('--host', default='0.0.0.0', type=str, dest='host')
    args = vars(parser.parse_args())
    uvicorn.run(app, **args)
