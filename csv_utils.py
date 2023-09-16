# csv_utils.py
import csv
import logging
import os
from config import OUTPUT_CSV, CSV_FILENAME

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Initializing csv_utils.py")

def initialize_output_csv():
    logging.info("Initializing output CSV.")
    if not os.path.exists('output'):
        os.makedirs('output')
    with open(OUTPUT_CSV, 'w', newline='') as outfile:
        fieldnames = ['Registration Number', 'Full Name', 'Gender', 'GSM Number', 'Email', 'Score', 'Institution', 'Course', 'LGA', 'State']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
    logging.info("Output CSV initialized.")

def read_input_csv():
    logging.info("Reading input CSV.")
    with open(CSV_FILENAME, 'r') as infile:
        csvreader = csv.reader(infile)
        next(csvreader)
        data = [row[0] for row in csvreader]
    logging.info("Input CSV read.")
    return data

def write_to_output_csv(candidate_info, output_lock):
    logging.info("Writing to output CSV.")
    with output_lock:
        with open(OUTPUT_CSV, 'a', newline='') as outfile:
            fieldnames = ['Registration Number', 'Full Name', 'Gender', 'GSM Number', 'Email', 'Score', 'Institution', 'Course', 'LGA', 'State']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writerow(candidate_info)
    logging.info("Written to output CSV.")

logging.info("csv_utils.py initialized")