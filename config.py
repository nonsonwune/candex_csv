# config.py
import os
import logging
from dotenv import load_dotenv
from datetime import datetime

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)
logging.info("Initializing config.py")

# Load environment variables
load_dotenv()

# Constants
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
CHROMEDRIVER_PATH = "chromedriver-mac-x64/chromedriver"
LOGIN_URL = 'https://efacility.jamb.gov.ng/Signin'
USERNAME_FIELD = 'UserName'
PASSWORD_FIELD = 'password'
LOGIN_BUTTON = 'Login'
FIND_CANDIDATE = 'Find Candidate'
SEARCH_DATA = 'Search Data'
REG_FIELD_NAME = 'ctl00$MainContent$txtRegNumber'
DATA_CLASS = 'col-md-8'
DATA_TABLE = 'table'
CSV_FILENAME = 'input/sample9.csv'
OUTPUT_CSV = f'output/{os.path.basename(CSV_FILENAME).split(".")[0]}_outputfile.csv'
BROWSER_WINDOW = 3

logging.info("config.py initialized")