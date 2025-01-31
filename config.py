from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
MAX_PAGES = int(os.getenv("MAX_PAGES"))
DELAY = int(os.getenv("DELAY"))
HEADLESS_MODE = bool(os.getenv("HEADLESS_MODE"))
HEADLESS = bool(os.getenv("HEADLESS"))  # True for headless mode (without GUI)
WAIT_TIME = int(os.getenv("WAIT_TIME"))  # Time to wait between pages to make the behavior look more natural
OUTPUT_FILE = os.getenv("OUTPUT_FILE")
VISITED_FILE = os.getenv("VISITED_FILE")
MIN_TIME_SLEEP_NEXT_BUTTON = int(os.getenv("MIN_TIME_SLEEP_NEXT_BUTTON"))
MAX_TIME_SLEEP_NEXT_BUTTON = int(os.getenv("MAX_TIME_SLEEP_NEXT_BUTTON"))
# redis
REDIS_SERVER_IP = os.getenv("REDIS_SERVER_IP")
REDIS_SERVER_PORT = int(os.getenv("REDIS_SERVER_PORT"))
