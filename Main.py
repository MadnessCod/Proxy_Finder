import requests
import peewee
import pandas as pd
import local_settings

from database_manager import DatabaseManager
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()

websites = [
    "https://sslproxies.org/",
    "https://free-proxy-list.net/",
    "https://us-proxy.org/",
    "https://socks-proxy.net/",
]

database_manager = DatabaseManager(
    database_name=local_settings.DATABASE["name"],
    user=local_settings.DATABASE["user"],
    password=local_settings.DATABASE["password"],
    host=local_settings.DATABASE["host"],
    port=local_settings.DATABASE["port"],
)


class Proxy(peewee.Model):
    ip_address = peewee.CharField(max_length=250, verbose_name="ip address")
    port = peewee.CharField(max_length=250, verbose_name="port")
    code = peewee.CharField(max_length=250, verbose_name="code")
    country = peewee.CharField(max_length=250, verbose_name="country")
    anonymity = peewee.CharField(max_length=250, verbose_name="anonymity")
    google = peewee.CharField(max_length=250, verbose_name="google")
    https = peewee.CharField(max_length=250, verbose_name="https")
    last_checked = peewee.CharField(max_length=250, verbose_name="last checked")

    class Meta:
        database = database_manager.db


class Scrapper:
    def __init__(self, url, useragent):
        self.url = url
        self.user_agent = useragent.random
        self.headers = {"User-Agent": self.user_agent}

    def scrapper(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            data_list = list()
        except requests.exceptions.RequestException as e:
            print(e)
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", class_="table")
            th = table.find("thead").find_all("th")
            columns = [i.text for i in th]

            trs = {i: j for i, j in enumerate(table.find("tbody").find_all("tr"))}
            for i in trs.values():
                data_list.append([j.text for j in i.find_all("td")])
            df = pd.DataFrame(data_list, columns=columns)
            return data_list

    def check_proxy(self):
        return requests.get(self.url, headers=self.headers).status_code


if __name__ == "__main__":
    try:
        database_manager.create_table(models=[Proxy])
        for i in websites:
            class_instance = Scrapper(i, ua)
            class_list = class_instance.scrapper()
            for entry in class_list:
                Proxy.create(
                    ip_address=entry[0],
                    port=entry[1],
                    code=entry[2],
                    country=entry[3],
                    anonymity=entry[4],
                    google=entry[5],
                    https=entry[6],
                    last_checked=entry[7],
                )
    except peewee.IntegrityError as e:
        print(f"Error : {e}")
    finally:
        if database_manager.db:
            database_manager.db.close()
            print("database connection is closed")
