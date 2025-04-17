import csv
import sys

def adjust_event_time(csv_file):
    with open(csv_file, 'r', newline='') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
        
        if not rows:
            print("The input CSV file is empty or not readable.")
            return
        
        # Identify the first EventTime across all rows for normalization
        first_event_time = int(rows[0]['EventTime'])
        
        # Normalize EventTime across all rows
        for row in rows:
            row['EventTime'] = str(int(row['EventTime']) - first_event_time)
        
        # Filter out rows where NumPixels is not 2
        filtered_rows = [row for row in rows if row.get('NumPixels') == '2']
        
        if not filtered_rows:
            print("No rows have NumPixels equal to 2.")
            return
        
    # Overwrite the original CSV with normalized event times and filtered rows
    with open(csv_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)
        
    print(f"Normalized and filtered EventTime in CSV; saved back to {csv_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python adjust_event_time.py <csv_file>")
    else:
        csv_file = sys.argv[1]
        adjust_event_time(csv_file)