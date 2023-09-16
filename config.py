# config.py
import os
from dotenv import load_dotenv
from datetime import datetime

# Initialize environment variables for login
load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

now = datetime.now()
output_time = now.strftime("%Y%m%d%H%M%S") + str(now.microsecond)[:6]

# Constants
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
CSV_FILENAME = 'input/foreign 2.csv'
OUTPUT_CSV = f'output/{CSV_FILENAME.split("/")[-1].split(".")[0]}_output{output_time}.csv'
BROWSER_WINDOW = 7