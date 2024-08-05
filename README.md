### ⚠️ Outdated Documentation Warning
# Authomatic Proxy Scraper

This Python program scrapes proxy data from four different websites and stores it in a PostgreSQL database, 
uses celery and celery beat to make schedule calls to websites and evaluates their availability

## Table of contents
   - [Feature](#features)
   - [Requirements](#requirements)
   - [Installation & usage](#installation-and-usage)

## Features

- **Scraping**: Scrapes proxy data from four specified websites.
- **Database Storage**: Stores the scraped proxy data in a PostgreSQL database.
- **Scheduled Execution**: Can be scheduled to run periodically to update the proxy data.

## Requirements

- Python 3.x
- Required Python libraries (install via `poetry install`)
- PostgreSQL
- Redis

## Installation and Usage

1. **Clone the repository:**

   ```bash
   git clone https://github.com/MadnessCod/Proxy_Finder.git
   ```
2. **install poetry**

    ```bash 
        pip install poetry
    ```

3. **Install dependencies using Poetry**

    ```bash
        poetry install 
    ```

4. **Set up PostgreSQL**

    1. create a new local_settings.py file
   2. copy sample_settings.py to local_settings.py
   3. put your PostgreSQL infor inside local_settings.py 

#### you can run the program in two ways
**Manually**
   1. **Create Database**
      ```bash
      python database_creation.py
      ```
   2. **Setup Redis**
         1. open a new terminal 
         2. 
            ```bash
            cd redis
            ```
         3. 
            ```bash
            redis-server.exe
            ```
   3. **flower(optional)**
      * flower is used to monitor celery tasks
      1. open a new terminal 
      2. 
         ```bash
         cd Scrapper
         ```
      3.
         ```bash
         celery -A tasks flower
         ```
      4. head to your browser 
      5. enter http://localhost:5555/

   4. **Running celery**
      1. open a new terminal 
      2. 
         ```bash
         cd Scrapper
         ```
      3.
         ```bash
         celery -A tasks worker --loglevel=info -P eventlet
         ```
      4. for windows use `-P eventlet`

   5. **Running celery beat**
      1. open a new terminal 
      2. 
         ```bash
         cd Scrapper
         ```
      3.
         ```bash
         celery -A tasks beat --loglevel=info
         ```
**Automatically**
   1. run scrapper.py