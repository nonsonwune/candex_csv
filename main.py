# main.py
from multiprocessing import Process, Manager, Lock
from collections import OrderedDict
from webdriver_utils import initialize_and_setup_webdriver, search_candidate
from csv_utils import initialize_output_csv, read_input_csv, write_to_output_csv
import logging
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException
import re
from selenium.webdriver.common.by import By 
from config import BROWSER_WINDOW, DATA_CLASS, OUTPUT_CSV
import csv

logging.getLogger().info("Initializing main.py")

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Initializing main.py")

processed_count = 0
output_lock = Lock()
sorted_output = OrderedDict()

def no_record_dict(reg_num):
    logging.info(f"Creating no_record_dict for {reg_num}")
    return OrderedDict([
        ('Registration Number', reg_num),
        ('Full Name', 'No Record Found'),
        ('GSM Number', 'No Record Found'),
        ('Email', 'No Record Found'),
        ('Score', 'No Record Found'),
        ('Gender', 'No Record Found'),
        ('Institution', 'No Record Found'),
        ('Course', 'No Record Found'),
        ('LGA', 'No Record Found'),
        ('State', 'No Record Found')
    ])

def get_candidate_info(driver, reg_num):
    logging.info(f"Getting candidate info for {reg_num}")
    try:
        element = driver.find_element(By.CLASS_NAME, DATA_CLASS)
        element_innerHTML = element.get_attribute('innerHTML')
    except NoSuchElementException:
        return no_record_dict(reg_num)

    def extract(regex, text, default=None):
        match = re.search(regex, text)
        return match.group(1) if match else default

    full_name = extract(r'Full Name: <b>(.*?)<\/b>', element_innerHTML)
    gsm_number = extract(r'GSM No.: <b>(.*?)<\/b>', element_innerHTML)
    email = extract(r'e-Facility email: (.*?)<br>', element_innerHTML)
    score = extract(r'UTME Scores Aggregate: (\d+)', element_innerHTML)
    gender = extract(r'Gender: <b>(.*?)<\/b>', element_innerHTML)

    origin = extract(r'Origin: <b>(.*?)<\/b>', element_innerHTML)
    lga, state = ("", "") if origin is None else map(str.strip, origin.split(","))
    if lga:
        lga = lga.replace(' Local Govt', '').strip()
    if state:
        state = state.replace(' State.', '').strip()

    try:
        course_Inst_div = driver.find_element(By.CSS_SELECTOR, "div#MainContent_dvCourse div.panel-body")
        table_element = course_Inst_div.find_element(By.TAG_NAME, 'table')
        rows = table_element.find_elements(By.TAG_NAME, 'tr')
        cells = rows[1].find_elements(By.TAG_NAME, 'td')
        course = cells[0].text
        institution = cells[1].text
    except NoSuchElementException:
        course, institution = "No Record Found", "No Record Found"

    logging.info(f"Got candidate info for {reg_num}")
    return OrderedDict([
        ('Registration Number', reg_num),
        ('Full Name', full_name),
        ('GSM Number', gsm_number),
        ('Email', email),
        ('Score', score),
        ('Gender', gender),
        ('Institution', institution),
        ('Course', course),
        ('LGA', lga),
        ('State', state)
    ])

def write_immediately(candidate_info, output_lock):
    with output_lock:
        with open(OUTPUT_CSV, 'a', newline='') as outfile:
            fieldnames = ['Registration Number', 'Full Name', 'Gender', 'GSM Number', 'Email', 'Score', 'Institution', 'Course', 'LGA', 'State']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writerow(candidate_info)

def search_and_extract_in_tab(work_chunk, total_count, browser_count, mgr_processed_count, output_lock):
    logging.info(f"Starting search_and_extract_in_tab for browser {browser_count}")
    try:
        driver, wait = initialize_and_setup_webdriver(browser_count, BROWSER_WINDOW)
    except Exception as e:
        print(f"Failed to initialize and login browser instance: {e}")
        return

    for reg_num in work_chunk:
        try:
            search_candidate(driver, wait, reg_num)
            candidate_info = get_candidate_info(driver, reg_num)
            if candidate_info:
                write_immediately(candidate_info, output_lock)
                mgr_processed_count.value += 1  # Change here
                print(f"{mgr_processed_count.value}/{total_count} processed")
        except (NoSuchElementException, TimeoutException, NoSuchWindowException) as e:
            no_record = no_record_dict(reg_num)
            write_immediately(no_record, output_lock)
            print(f"Error processing {reg_num}: {e}")
    logging.info(f"Completed search_and_extract_in_tab for browser {browser_count}")

def main():
    logging.info("Main function started.")
    initialize_output_csv()
    registration_numbers = read_input_csv()
    work_chunks = [registration_numbers[i::BROWSER_WINDOW] for i in range(BROWSER_WINDOW)]
    total_count = len(registration_numbers)

    manager = Manager()
    mgr_processed_count = manager.Value('i', 0)
    sorted_output = manager.dict()
    output_lock = Lock()

    processes = []
    for i, work_chunk in enumerate(work_chunks):
        process = Process(target=search_and_extract_in_tab, args=(work_chunk, total_count, i + 1, mgr_processed_count, output_lock))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    logging.info("Main function completed.")

if __name__ == '__main__':
    main()