from Scrapper.celery import app


if __name__ == '__main__':
    app.Beat().run()

