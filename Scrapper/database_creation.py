import peewee

from database_manager import DatabaseManager
from local_settings import DATABASE


database_manager = DatabaseManager(
    database_name=DATABASE["name"],
    user=DATABASE["user"],
    password=DATABASE["password"],
    host=DATABASE["host"],
    port=DATABASE["port"],
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


if __name__ == "__main__":
    try:
        if not Proxy.table_exists():
            database_manager.create_table(models=[Proxy])
    except peewee.DatabaseError as error:
        print(f'Error : {error}')
    finally:
        if database_manager.db:
            database_manager.db.close()
