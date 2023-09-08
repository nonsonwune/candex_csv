# webdriver_utils.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from config import *
from selenium.webdriver.chrome.options import Options

def initialize_and_setup_webdriver(browser_count, total_count):
    print(f"Opening browser {browser_count}/{total_count}...")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--disable-javascript")
        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(LOGIN_URL)
        driver.set_window_size(1920, 1080)
        wait = WebDriverWait(driver, 10)
        login(driver, wait, browser_count, total_count)
        return driver, wait
    except Exception as e:
        print(f"Exception in initialize_and_setup_webdriver: {e}")
        raise e

def login(driver, wait, browser_count, total_count):
    wait.until(EC.presence_of_element_located((By.NAME, USERNAME_FIELD)))
    username_elem = driver.find_element(By.NAME, USERNAME_FIELD)
    password_elem = driver.find_element(By.NAME, PASSWORD_FIELD)
    username_elem.send_keys(USERNAME)
    password_elem.send_keys(PASSWORD)
    driver.find_element(By.LINK_TEXT, LOGIN_BUTTON).click()
    navigate_to_find_candidate(driver, wait, browser_count, total_count)

def navigate_to_find_candidate(driver, wait, browser_count, total_count):
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, FIND_CANDIDATE)))
    driver.find_element(By.LINK_TEXT, FIND_CANDIDATE).click()
    print(f"Browser {browser_count}/{total_count} ready")

def search_candidate(driver, wait, reg_num):
    """
    Perform the candidate search operation.

    Args:
        driver: WebDriver instance
        wait: WebDriverWait object
        reg_num: Registration number of the candidate
    """
    wait.until(EC.presence_of_element_located((By.NAME, REG_FIELD_NAME)))
    reg_number_elem = driver.find_element(By.NAME, REG_FIELD_NAME)
    reg_number_elem.clear()
    reg_number_elem.send_keys(reg_num)
    driver.find_element(By.LINK_TEXT, SEARCH_DATA).click()