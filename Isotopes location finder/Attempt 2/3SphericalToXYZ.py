import csv
import numpy as np


def read_phi_rho_from_csv(csv_file_path):
    phi_values = []
    rho_values = []

    # Open the CSV file
    with open(csv_file_path, mode='r', newline='') as csv_file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(csv_file)

        # Iterate through each row in the CSV
        for row in csv_reader:
            try:
                # Read the Phi and Rho as floats
                phi = float(row['Phi'])
                rho = float(row['Theta'])
                phi_values.append(phi)
                rho_values.append(rho)
            except ValueError:
                print(f"Skipping row with invalid data: {row}")
            except KeyError as e:
                print(f"Missing column in the row: {row}, Error: {e}")

    return phi_values, rho_values

def write_xyz_to_csv(csv_file_path, x, y, z, output_csv_path):
    # Open the CSV file to read the original data
    with open(csv_file_path, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        fieldnames = csv_reader.fieldnames

    # Replace fieldnames for output
    new_fieldnames = ['Image Number', 'x', 'y', 'z']

    # Open a new CSV file for writing
    with open(output_csv_path, mode='w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(new_fieldnames)

        # Write each row with transformed phi and Theta values
        for i, image_number in enumerate(range(1, len(x) + 1)):
            csv_writer.writerow([image_number, x[i], y[i], z[i]])

def read_robotFacing_from_csv(csv_file_path):
    facing = []

    # Open the CSV file
    with open(csv_file_path, mode='r', newline='') as csv_file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(csv_file)

        # Iterate through each row in the CSV
        for row in csv_reader:
            try:
                face = float(row['face'])
                facing.append(face)
            except ValueError:
                print(f"Skipping row with invalid data: {row}")
            except KeyError as e:
                print(f"Missing column in the row: {row}, Error: {e}")

    return facing

# Example usage: replace 'phi_rho.csv' with your CSV file path
csv_path = '/Users/kaixinxue/Desktop/M400/Attempt2/phi_theta.csv'  # Ensure this is your actual file path
robot_path = '/Users/kaixinxue/Desktop/M400/Attempt2/robotPosition.csv' # Robot path
output_csv_path = '/Users/kaixinxue/Desktop/M400/Attempt2/xyz_coordinates.csv'  # Path to the output CSV
phi_values, theta_values = read_phi_rho_from_csv(csv_path)
robot_Facing = read_robotFacing_from_csv(robot_path)

#modify the phi value so that it is normalized.
phi_values = [(phi + facing) for phi, facing in zip(phi_values, robot_Facing)]

phi_array = np.array(phi_values)
theta_array = np.array(theta_values)
phi_radians = phi_array * np.pi / 180
theta_radians = theta_array * np.pi / 180

phi_values = phi_radians.tolist()
theta_values = theta_radians.tolist()

x = np.sin(phi_values)*np.sin(theta_values) #Transform Spherical coordinates into XYZ unit direction
y = np.cos(phi_values)*np.sin(theta_values)
z = np.cos(theta_values)

write_xyz_to_csv(csv_path, x, y, z, output_csv_path)

print("x, y, z have been written to:", output_csv_path)