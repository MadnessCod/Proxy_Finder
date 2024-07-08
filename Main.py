import peewee
import local_settings

from celery import Celery
from database_manager import DatabaseManager
from fake_useragent import UserAgent
from tasks import scrapper


app = Celery('tasks')
app.config_from_object('celeryconfig')
app.autodiscover_tasks(['tasks'])

ua = UserAgent()

websites = {
    "https://sslproxies.org/": 'http',
    "https://free-proxy-list.net/": 'http',
    "https://us-proxy.org/": 'http',
    "https://socks-proxy.net/": 'socks5',
}

database_manager = DatabaseManager(
    database_name=local_settings.DATABASE["name"],
    user=local_settings.DATABASE["user"],
    password=local_settings.DATABASE["password"],
    host=local_settings.DATABASE["host"],
    port=local_settings.DATABASE["port"],
)


class Proxy(peewee.Model):
    ip_address = peewee.CharField(max_length=100, verbose_name="ip address")
    method = peewee.CharField(max_length=100, verbose_name="method")
    port = peewee.CharField(max_length=100, verbose_name="port")
    code = peewee.CharField(max_length=100, verbose_name="code")
    country = peewee.CharField(max_length=100, verbose_name="country")
    anonymity = peewee.CharField(max_length=100, verbose_name="anonymity")
    google = peewee.CharField(max_length=100, verbose_name="google")
    https = peewee.CharField(max_length=100, verbose_name="https")
    last_checked = peewee.CharField(max_length=100, verbose_name="last checked")
    status = peewee.BooleanField(default=False, verbose_name="status")

    class Meta:
        database = database_manager.db


def main():
    try:
        database_manager.create_table(models=[Proxy])
    except peewee.IntegrityError as e:
        print(f"Error : {e}")
    else:
        for website, method in websites.items():
            useragent = ua.random
            headers = {'user-agent': useragent}
            async_results = scrapper.delay(website, headers)
            proxy_list = async_results.get()
            if proxy_list:
                for entry in proxy_list:
                    Proxy.create(
                        ip_address=entry[0],
                        method=method,
                        port=entry[1],
                        code=entry[2],
                        country=entry[3],
                        anonymity=entry[4],
                        google=entry[5],
                        https=entry[6],
                        last_checked=entry[7],
                    )
    finally:
        if database_manager.db:
            database_manager.db.close()
            print("database connection is closed")


if __name__ == '__main__':
    main()
