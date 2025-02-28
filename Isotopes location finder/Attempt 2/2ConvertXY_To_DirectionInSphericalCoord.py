import csv
import numpy as np

def read_midpoints_from_csv(csv_file_path):
    x_values = []
    y_values = []

    # Open the CSV file
    with open(csv_file_path, mode='r', newline='') as csv_file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(csv_file)

        # Iterate through each row in the CSV
        for row in csv_reader:
            try:
                x = float(row['Midpoint_X'])
                y = float(row['Midpoint_Y'])
                x_values.append(x)
                y_values.append(y)
            except ValueError:
                print(f"Skipping row with invalid data: {row}")
            except KeyError as e:
                print(f"Missing column in the row: {row}, Error: {e}")

    return x_values, y_values

def write_phi_theta_to_csv(csv_file_path, phi, theta, output_csv_path):
    # Open the CSV file to read the original data
    with open(csv_file_path, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        fieldnames = csv_reader.fieldnames

    # Replace fieldnames for output
    new_fieldnames = ['Image Number', 'Phi', 'Theta']

    # Open a new CSV file for writing
    with open(output_csv_path, mode='w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(new_fieldnames)

        # Write each row with transformed phi and Theta values
        for i, image_number in enumerate(range(1, len(phi) + 1)):
            csv_writer.writerow([image_number, phi[i], theta[i]])

# Example usage
csv_path = '/Users/kaixinxue/Desktop/M400/Attempt2/midpoints.csv'  # Path to your input CSV
output_csv_path = '/Users/kaixinxue/Desktop/M400/Attempt2/phi_theta.csv'  # Path to the output CSV

x_values, y_values = read_midpoints_from_csv(csv_path) #Reads the midpoint and transform that code into sphereical coordinates

# Calculate phi and rho
phi = np.array(x_values) * 2 * np.pi / 1600 * 180 / np.pi - 90 # the 90 is to normalize such the front of detector is 0
theta = np.array(y_values) * np.pi / 800 * 180 / np.pi

# Write the new CSV with phi and rho
write_phi_theta_to_csv(csv_path, phi, theta, output_csv_path)

print("Phi and Theta have been written to:", output_csv_path)