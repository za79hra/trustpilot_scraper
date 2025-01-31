# trustpilot_scraper

This project is designed to scrape reviews from a website. It uses Playwright for browsing the web pages and Redis for storing the scraped data.

## Prerequisites

Make sure you have the following installed before running the project:

1. **Python 3.9 or higher**
2. **Redis** for data storage
3. **Playwright** for browser automation

## Install Dependencies

First, install the dependencies by running the following command in the root of your project:

```bash
pip install -r requirements.txt
```
## Setting Up Redis

```bash
sudo apt-get install redis-server
```
Then, start the Redis service:
```bash
sudo service redis-server start
```
## Or use Docker:
If you're using Docker for Redis, you can run Redis with this command:
```bash
docker run --name redis -p 6379:6379 -d redis
```
## Configuring Environment Variables

The project uses a **.env** file to configure environment variables. Create a .env file in the root of your project with the following variables:
```bash
BASE_URL=https://example.com/reviews
MAX_PAGES=10
DELAY=3
HEADLESS_MODE=True
HEADLESS=True
WAIT_TIME=5
OUTPUT_FILE=reviews.json
VISITED_FILE=visited_reviews.json
MIN_TIME_SLEEP_NEXT_BUTTON=1
MAX_TIME_SLEEP_NEXT_BUTTON=2

REDIS_SERVER_IP=localhost
REDIS_SERVER_PORT=6379
```
## Running the Project
To run the project, use the following command:
```bash
python main.py
```
This script will start scraping data from the website and store the results in the **reviews.json** file.

## Notes
If you need to run this script in headless mode (on a server), set the ***HEADLESS*** variable to ***True***.
The ***WAIT_TIME*** variable controls the delay between requests to simulate natural user behavior.

