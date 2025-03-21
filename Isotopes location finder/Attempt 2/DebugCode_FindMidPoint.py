import csv

def calculate_midpoint(csv_path):
    x_values = []
    y_values = []

    # Read the CSV file containing the pixel data
    with open(csv_path, mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Skip the header row
        next(csv_reader)

        for row in csv_reader:
            x, y = int(row[0]), int(row[1])
            x_values.append(x)
            y_values.append(y)

    if not x_values or not y_values:
        print("No pixel data found to calculate midpoint.")
        return None

    # Calculate midpoint
    midpoint_x = sum(x_values) / len(x_values)
    midpoint_y = sum(y_values) / len(y_values)

    return midpoint_x, midpoint_y

# Example usage: replace 'output.csv' with your CSV file path
midpoint1 = calculate_midpoint('/Users/kaixinxue/Desktop/M400/Attempt2/Position1.csv')
midpoint2 = calculate_midpoint('/Users/kaixinxue/Desktop/M400/Attempt2/Position2.csv')
midpoint3 = calculate_midpoint('/Users/kaixinxue/Desktop/M400/Attempt2/Position3.csv')
midpoint4 = calculate_midpoint('/Users/kaixinxue/Desktop/M400/Attempt2/Position4.csv')
if midpoint1:
    print(f"The midpoint of the pixels is at: ({midpoint1[0]}, {midpoint1[1]})")
if midpoint2:
    print(f"The midpoint of the pixels is at: ({midpoint2[0]}, {midpoint2[1]})")
if midpoint3:
    print(f"The midpoint of the pixels is at: ({midpoint3[0]}, {midpoint3[1]})")
if midpoint4:
    print(f"The midpoint of the pixels is at: ({midpoint4[0]}, {midpoint4[1]})")