import argparse
import os


def load_settings():
    if os.path.exists('local_settings.py'):
        try:
            from local_settings import DATABASE
            if all(DATABASE.get(key) for key in ['name', 'user_name', 'password', 'host', 'port']):
                return DATABASE
        except ImportError:
            pass
    return None


def cli_main():
    settings = load_settings()
    if settings:
        print(settings)
    else:

        parser = argparse.ArgumentParser(description='save Database connection information')
        parser.add_argument(
            '--database_name',
            type=str,
            required=True,
            help='the name of the database'
        )
        parser.add_argument(
            '--user_name',
            type=str,
            required=True,
            help='the name of the user'
        )
        parser.add_argument(
            '--password',
            type=str,
            required=True,
            help='the password of the user'
        )
        parser.add_argument(
            '--host',
            default='localhost',
            help='the database port',
        )
        parser.add_argument(
            '--port',
            type=int,
            default=5432,
            help='the database port'
        )
        args = parser.parse_args()
        save_settings(args.database_name, args.user_name, args.password, args.host, args.port)


def save_settings(database_name, user_name, password, host, port):

    settings_content = f"""
    DATABASE = {{
        'name': '{database_name}',
        'user_name': '{user_name}',
        'password': '{password}',
        'host': '{host}',
        'port': {port}
    }}
    """

    with open('local_settings.py', 'w') as file:
        file.write(settings_content)


if __name__ == '__main__':
    cli_main()
