# Proxy Scraper and Database Storer

This Python program scrapes proxy data from four different websites and stores it in a PostgreSQL database.

## Features

- **Scraping**: Scrapes proxy data from four specified websites.
- **Database Storage**: Stores the scraped proxy data in a PostgreSQL database.
- **Scheduled Execution**: Can be scheduled to run periodically to update the proxy data.
- **Logging**: Logs scraping and database operations for monitoring and troubleshooting.

## Requirements

- Python 3.x
- Required Python libraries (install via `poetry install`)
- PostgreSQL

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/MadnessCod/Proxy_Finder.git
   cd proxy-scraper
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

   