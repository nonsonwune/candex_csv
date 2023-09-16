import csv
import os
import logging
from config import OUTPUT_CSV, CSV_FILENAME

logging.getLogger().info("Initializing csv_utils.py")

# Initialize output CSV
def initialize_output_csv():
    logging.info("Initializing output CSV.")
    os.makedirs('output', exist_ok=True)
    with open(OUTPUT_CSV, 'w', newline='') as outfile:
        fieldnames = ['Registration Number', 'Full Name', 'Gender', 'GSM Number', 'Email', 'Score', 'Institution', 'Course', 'LGA', 'State']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

# Read input CSV
def read_input_csv():
    logging.info("Reading input CSV.")
    with open(CSV_FILENAME, 'r') as infile:
        csvreader = csv.reader(infile)
        next(csvreader)
        data = [row[0] for row in csvreader]
    return data

# Write to output CSV
def write_to_output_csv(candidate_info, output_lock):
    logging.info("Writing to output CSV.")
    with output_lock:
        with open(OUTPUT_CSV, 'a', newline='') as outfile:
            fieldnames = ['Registration Number', 'Full Name', 'Gender', 'GSM Number', 'Email', 'Score', 'Institution', 'Course', 'LGA', 'State']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writerow(candidate_info)

logging.info("csv_utils.py initialized")
