import peewee

from fake_useragent import UserAgent
from tasks import scrapper
from database_creation import Proxy, database_manager


ua = UserAgent()
websites = {
    "https://sslproxies.org/": 'http',
    "https://free-proxy-list.net/": 'http',
    "https://us-proxy.org/": 'http',
    "https://socks-proxy.net/": 'socks5',
}


def main():
    try:
        if not Proxy.table_exists():
            database_manager.create_table(models=[Proxy])
    except peewee.IntegrityError as e:
        print(f"Error : {e}")
    else:
        for website, method in websites.items():
            useragent = ua.random
            headers = {'User-Agent': useragent}
            scrapper.delay(website, headers, method)
    finally:
        if database_manager.db:
            database_manager.db.close()
            print("database connection is closed")


if __name__ == '__main__':
    main()
