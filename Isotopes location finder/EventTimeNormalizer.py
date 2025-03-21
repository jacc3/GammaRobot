import csv
import sys

def adjust_event_time(csv_file):
    with open(csv_file, 'r', newline='') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
        
        if not rows:
            print("The input CSV file is empty or not readable.")
            return
        
        # Identify the first EventTime
        first_event_time = int(rows[0]['EventTime'])
        
        # Adjust each EventTime
        for row in rows:
            row['EventTime'] = str(int(row['EventTime']) - first_event_time)
        
    # Overwrite the original CSV with new event times
    with open(csv_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Adjusted EventTime in CSV; saved back to {csv_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python adjust_event_time.py <csv_file>")
    else:
        csv_file = sys.argv[1]
        adjust_event_time(csv_file)
