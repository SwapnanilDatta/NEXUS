import csv
import json

# Define file paths
csv_file_path = 'fifaplayers.csv'  # Replace with your CSV file path
json_file_path = 'output.json'  # Replace with your desired JSON file path

# Read the CSV file and convert it to a JSON object
with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    data = [row for row in csv_reader]

# Write the JSON object to a file
with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4)

print(f"CSV file has been converted to JSON and saved as {json_file_path}")
