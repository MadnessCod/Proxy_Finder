import requests


from local_settings import BROKER_URL, BACKEND_URL
from bs4 import BeautifulSoup
from celery import Celery
from database_creation import Proxy


app = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)

app.conf.broker_connection_retry = True
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    print(self.AsyncResult(self.request.id).state)


@app.task
def scrapper(url, headers, method):
    try:
        response = requests.get(url, headers=headers)
        proxy_list = list()
    except requests.exceptions.RequestException as error:
        print(f'Error: {error}')
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        # maybe attribute Error
        table = soup.find("table", class_="table")
        trs = {i: j for i, j in enumerate(table.find("tbody").find_all("tr"))}
        for tr in trs.values():
            proxy_list.append([j.text for j in tr.find_all("td")])
        for proxy in proxy_list:
            Proxy.create(
                ip_address=proxy[0],
                method=method,
                port=proxy[1],
                code=proxy[2],
                country=proxy[3],
                anonymity=proxy[4],
                google=proxy[5],
                https=proxy[6],
                last_checked=proxy[7],
                status=check_proxy.delay(method, proxy[0], proxy[1]),
            )


@app.task
def check_proxy(method, ip, port):
    proxy = {'http': f'{method}://{ip}:{port}'}
    return requests.get('https://www.google.com', proxies=proxy).status_code == 200


@app.task
def proxy_evaluator():
    proxies = Proxy.select()
    for proxy in proxies:
        prox = {'http': f'{proxy.method}://{proxy.ip_address}:{proxy.port}'}
        if requests.get('https://www.google.com', proxies=prox).status_code != 200:
            Proxy.delete().where(Proxy.ip_address == proxy.ip_address).execute()
