import requests
from bs4 import BeautifulSoup
from celery import Celery

BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6379/0'
app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)

app.conf.broker_connection_retry = True
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    print(self.AsyncResult(self.request.id).state)


@app.task
def scrapper(url, headers):
    try:
        response = requests.get(url, headers=headers)
        data_list = list()
    except requests.exceptions.RequestException as error:
        print(f'Error: {error}')
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="table")
        trs = {i: j for i, j in enumerate(table.find("tbody").find_all("tr"))}
        for tr in trs.values():
            data_list.append([j.text for j in tr.find_all("td")])
        return data_list


@app.task
def check_proxy(method, ip, port):
    proxy = {'http': f'{method}://{ip}:{port}'}
    return requests.get('https://www.google.com', proxies=proxy).status_code == 200
