import csv
import sys

def adjust_event_time(csv_file):
    with open(csv_file, 'r', newline='') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
        
        if not rows:
            print("The input CSV file is empty or not readable.")
            return
        
        # Identify the first EventTime as a float for normalization
        first_event_time = float(rows[0]['timestamp'])
        
        # Normalize EventTime across all rows
        for row in rows:
            # Convert timestamp to float, normalize, and then back to string
            row['timestamp'] = str(float(row['timestamp']) - first_event_time)
        
    # Overwrite the original CSV with normalized event times and filtered rows
    with open(csv_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Normalized EventTime in CSV; saved back to {csv_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python adjust_event_time.py <csv_file>")
    else:
        csv_file = sys.argv[1]
        adjust_event_time(csv_file)