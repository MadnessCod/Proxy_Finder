import requests
import peewee

from bs4 import BeautifulSoup

from fake_useragent import UserAgent
from database_creation import Proxy

from celery import Celery
from celery.schedules import crontab
from local_settings import BROKER_URL, BACKEND_URL

app = Celery("Scrapper", broker=BROKER_URL, backend=BACKEND_URL)

app.conf.beat_schedule = {
    "scraping": {
        "task": "tasks.main",
        "schedule": crontab('*/10'),
    },
    "evaluator": {
        "task": "tasks.proxy_evaluator_main",
        "schedule": crontab('*/5'),
    },
}

ua = UserAgent()
websites = {
    "https://sslproxies.org/": "http",
    "https://free-proxy-list.net/": "http",
    "https://us-proxy.org/": "http",
    "https://socks-proxy.net/": "socks5",
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
    print(self.AsyncResult(self.request.id).state)


@app.task()
def main():
    """
    It iterates over the `websites`dictionary, and calls the `scrapper` Celery task
    asynchronously to scrape proxy information from each website.
    """
    for website, method in websites.items():
        scrapper.delay(website, method)


@app.task()
def scrapper(url: str, method: str) -> None:
    """
    Scrapes proxy information from a given URL and stores it in the database.

    Args:
        url (str): The URL to scrape proxy information from.
        method (str): The HTTP method ('http' or 'https') to associate with the proxies.

    Raises:
        requests.RequestException: If there is an issue with the HTTP request to `url`.
        AttributeError: If the HTML structure of the response does not match expectations.
        peewee.OperationalError: If there is an issue with storing data in the database.

    Notes:
        This function assumes the HTML structure of the response from `url` contains a table
        with rows (`tr` elements) where each row represents a proxy. It uses BeautifulSoup
        for parsing the HTML and extracts proxy information into `proxy_list`. Each proxy
        found is then stored in the `Proxy` database model using Peewee ORM. Additionally,
        the status of each proxy (whether it successfully connects to Google) is asynchronously
        checked using the `check_proxy` Celery task.

        Example of `Proxy` database model:
        class Proxy(peewee.Model):
            ip_address = peewee.CharField(unique=True)
            method = peewee.CharField()
            port = peewee.IntegerField()
            code = peewee.CharField()
            country = peewee.CharField()
            anonymity = peewee.CharField()
            google = peewee.CharField()
            https = peewee.CharField()
            last_checked = peewee.CharField()
            status = peewee.CharField()
    """
    try:
        proxy_list = list()
        headers = {"User-Agent": ua.random}
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as error:
        print(f"Error: {error}")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            table = soup.find("table", class_="table")
        except AttributeError as error:
            print(f"Error: {error}")
        else:
            trs = {i: j for i, j in enumerate(table.find("tbody").find_all("tr"))}
            for tr in trs.values():
                proxy_list.append([j.text for j in tr.find_all("td")])
            try:
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
            except peewee.OperationalError as error:
                print(f"Error: {error}")


@app.task()
def check_proxy(method: str, ip: str, port: str) -> bool:
    """
    Checks the connectivity of a given proxy by attempting to access 'https://www.google.com'.

    Args:
        method (str): The HTTP method ('http' or 'https') of the proxy.
        ip (str): The IP address of the proxy.
        port (str): The port number of the proxy.

    Returns:
        bool: True if the proxy successfully connects to 'https://www.google.com' (status code 200),
              False otherwise.

    Raises:
        requests.RequestException: If there is an issue with the HTTP request.
    """
    proxy = {"http": f"{method}://{ip}:{port}"}
    try:
        response = requests.get("https://www.google.com", proxies=proxy).status_code == 200
    except requests.exceptions.RequestException as error:
        print(f"Error: {error}")
    else:
        return response


@app.task()
def proxy_evaluator_main() -> None:
    """
    Evaluates proxies in the database by checking their connectivity to Google.

    This function retrieves all proxies from the `Proxy` table and attempts to
    access 'https://www.google.com' using each proxy. If a proxy fails (status code != 200),
    it is removed from the database.

    This function is intended to run as a periodic Celery task.

    Raises:
        peewee.DatabaseError: If there is an issue accessing the database.
    """
    try:
        proxies = Proxy.select()
    except peewee.DatabaseError as error:
        print(f"Error : {error}")
    else:
        for proxy in proxies:
            proxy_evaluator.delay(proxy)


@app.task()
def proxy_evaluator(proxy) -> None:
    prox = {"http": f"{proxy.method}://{proxy.ip_address}:{proxy.port}"}
    try:
        if requests.get("https://www.google.com", proxies=prox).status_code != 200:
            Proxy.delete().where(Proxy.ip_address == proxy.ip_address).execute()
    except requests.exceptions.RequestException as error:
        print(f"Reqeust Error : {error}")
    except peewee.OperationalError as error:
        print(f'Database Error : {error}')