import os
import re
import csv

def extract_shark_tank_data(transcript):
    sales_pattern = r"(?:sales of \$(\d+[\d,]*|\d+\s(?:million|billion|grand)))|(?:netted|over|on|about|close to)?\s*\$\s?(\d+[\d,]*|\d+\s(?:million|billion|grand))\s*(?:in sales|sales revenue|annual sales|total sales|revenue|net sales)|\b(netted|earned|made)\s+\$(\d+[\d,]*|\d+\s(?:million|billion|grand))"
    profitability_pattern = r"\b(profitable|profits|yes we made money|net income|earnings|profit margin|after expenses)\b"

    total_sales = re.findall(sales_pattern, transcript, re.IGNORECASE)
    total_sales = [item for sublist in total_sales for item in sublist if item]
    profitability_mentions = re.findall(profitability_pattern, transcript, re.IGNORECASE)
    is_profitable = "Yes" if profitability_mentions else "No"

    results = {
        "Total Sales/Revenue": total_sales,
        "Profitable": is_profitable
    }

    return results

directory_path = "Data/Pitch_Transcripts/"
output_directory = "Data/new_metrics"
os.makedirs(output_directory, exist_ok=True)
output_file_path = os.path.join(output_directory, "pitch_data.csv")

all_pitches_data = []
for root, dirs, files in os.walk(directory_path):
    for filename in files:
        if filename.endswith(".txt"):
            file_path = os.path.join(root, filename)

            pitch_number_match = re.search(r"Pitch_(\d+)", filename)
            pitch_number = int(pitch_number_match.group(1)) if pitch_number_match else -1

            with open(file_path, 'r', encoding='latin-1') as file:
                content = file.read()

                pitch_data = extract_shark_tank_data(content)
                pitch_data_with_number = {"Pitch Number": pitch_number, **pitch_data}
                all_pitches_data.append(pitch_data_with_number)

all_pitches_data.sort(key=lambda x: x['Pitch Number'])

with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)

    csv_writer.writerow(['Pitch Number', 'Total Sales/Revenue', 'Profitable'])

    for pitch in all_pitches_data:
        csv_writer.writerow([pitch['Pitch Number'], pitch['Total Sales/Revenue'], pitch['Profitable']])

print(f"Data written to {output_file_path}")