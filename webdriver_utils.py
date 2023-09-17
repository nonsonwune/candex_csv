# webdriver_utils.py
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
from config import *

logging.getLogger().info("Initializing webdriver_utils.py")

# Initialize and set up webdriver
def initialize_and_setup_webdriver(browser_count, total_count):
    logging.info(f"Initializing and setting up webdriver for browser {browser_count}/{total_count}")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(LOGIN_URL)
    driver.set_window_size(1920, 1080)
    wait = WebDriverWait(driver, 10)
    login(driver, wait, browser_count, total_count)
    return driver, wait

# Login to the web page
def login(driver, wait, browser_count, total_count):
    logging.info(f"Logging in for browser {browser_count}/{total_count}")
    wait.until(EC.presence_of_element_located((By.NAME, USERNAME_FIELD)))
    driver.find_element(By.NAME, USERNAME_FIELD).send_keys(USERNAME)
    driver.find_element(By.NAME, PASSWORD_FIELD).send_keys(PASSWORD)
    driver.find_element(By.LINK_TEXT, LOGIN_BUTTON).click()
    navigate_to_find_candidate(driver, wait, browser_count, total_count)

# Navigate to the "Find Candidate" page
def navigate_to_find_candidate(driver, wait, browser_count, total_count):
    logging.info(f"Navigating to find candidate for browser {browser_count}/{total_count}")
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, FIND_CANDIDATE)))
    driver.find_element(By.LINK_TEXT, FIND_CANDIDATE).click()

# Perform the candidate search operation
def search_candidate(driver, wait, reg_num):
    logging.info(f"Searching for candidate with reg_num {reg_num}")
    wait.until(EC.presence_of_element_located((By.NAME, REG_FIELD_NAME)))
    driver.find_element(By.NAME, REG_FIELD_NAME).clear()
    driver.find_element(By.NAME, REG_FIELD_NAME).send_keys(reg_num)
    driver.find_element(By.LINK_TEXT, SEARCH_DATA).click()

logging.info("webdriver_utils.py initialized")
