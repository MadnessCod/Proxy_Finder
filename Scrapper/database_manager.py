from peewee import PostgresqlDatabase


class DatabaseManager:
    def __init__(self, database_name, user, password, host, port):
        self.database_name = database_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.db = self.connect_to_database()

    def connect_to_database(self):
        database_connection = PostgresqlDatabase(
            self.database_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        database_connection.connect()
        return database_connection

    def close_connection(self):
        self.db.close()

    def create_table(self, models):
        self.db.create_tables(models)
