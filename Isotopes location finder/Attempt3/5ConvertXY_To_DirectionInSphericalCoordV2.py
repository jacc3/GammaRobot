import csv
import numpy as np

def read_midpoints_from_csv(csv_file_path):
    image_numbers = []
    cluster_numbers = []
    x_values = []
    y_values = []

    # Open the CSV file
    with open(csv_file_path, mode='r', newline='') as csv_file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(csv_file)

        # Iterate through each row in the CSV
        for row in csv_reader:
            try:
                image_number = int(row['Image Number'])
                cluster_number = int(row['Cluster Number'])
                x = float(row['Midpoint_X'])
                y = float(row['Midpoint_Y'])
                
                image_numbers.append(image_number)
                cluster_numbers.append(cluster_number)
                x_values.append(x)
                y_values.append(y)
            except ValueError:
                print(f"Skipping row with invalid data: {row}")
            except KeyError as e:
                print(f"Missing column in the row: {row}, Error: {e}")

    return image_numbers, cluster_numbers, x_values, y_values

def write_phi_theta_to_csv(image_numbers, cluster_numbers, phi, theta, output_csv_path):
    new_fieldnames = ['Image Number', 'Cluster Number', 'Phi', 'Theta']

    # Open a new CSV file for writing
    with open(output_csv_path, mode='w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(new_fieldnames)

        # Write each row with transformed phi and theta values
        for i in range(len(phi)):
            csv_writer.writerow([image_numbers[i], cluster_numbers[i], phi[i], theta[i]])

# Example usage
csv_path = '/Users/kaixinxue/Desktop/M400/Attempt3/midpoints.csv'  # Path to your input CSV
output_csv_path = '/Users/kaixinxue/Desktop/M400/Attempt3/phi_theta.csv'  # Path to the output CSV

image_numbers, cluster_numbers, x_values, y_values = read_midpoints_from_csv(csv_path)


# Calculate phi and theta
phi = np.array(x_values) * 2 * np.pi / 466 * 180 / np.pi - 90 # the 90 is to normalize such the front of detector is 0
theta = np.array(y_values) * np.pi / 324 * 180 / np.pi


# Write the new CSV with phi and theta
write_phi_theta_to_csv(image_numbers, cluster_numbers, phi, theta, output_csv_path)

print("Phi and Theta have been written to:", output_csv_path)