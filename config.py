import os
from dotenv import load_dotenv

load_dotenv()


DB_URL : str = os.environ["DB_URL"]
APP_ENV : str = os.getenv("APP_ENV", "DEV")