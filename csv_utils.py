# csv_utils.py
import csv
from config import OUTPUT_CSV, CSV_FILENAME
import os

def initialize_output_csv():
    if not os.path.exists('output'):
        os.makedirs('output')
    with open(OUTPUT_CSV, 'w', newline='') as outfile:
        fieldnames = ['Registration Number', 'Full Name', 'Gender', 'GSM Number', 'Email', 'Score', 'Institution', 'Course', 'LGA', 'State']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

def read_input_csv():
    with open(CSV_FILENAME, 'r') as infile:
        csvreader = csv.reader(infile)
        next(csvreader)
        return [row[0] for row in csvreader]

def write_to_output_csv(candidate_info, output_lock):
    with output_lock:
        with open(OUTPUT_CSV, 'a', newline='') as outfile:
            fieldnames = ['Registration Number', 'Full Name', 'Gender', 'GSM Number', 'Email', 'Score', 'Institution', 'Course', 'LGA', 'State']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writerow(candidate_info)