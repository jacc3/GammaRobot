import csv
import numpy as np

def read_phi_rho_from_csv(csv_file_path):
    image_numbers = []
    cluster_numbers = []
    phi_values = []
    theta_values = []

    with open(csv_file_path, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            try:
                image_number = int(row['Image Number'])
                cluster_number = int(row['Cluster Number'])
                phi = float(row['Phi'])
                theta = float(row['Theta'])
                
                image_numbers.append(image_number)
                cluster_numbers.append(cluster_number)
                phi_values.append(phi)
                theta_values.append(theta)
            except ValueError:
                print(f"Skipping row with invalid data: {row}")
            except KeyError as e:
                print(f"Missing column in the row: {row}, Error: {e}")

    return image_numbers, cluster_numbers, phi_values, theta_values

def read_robot_facing_from_csv(robot_path):
    facing_data = {}

    with open(robot_path, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            try:
                run_number = int(row['Run Number'])
                face = float(row['facing'])
                facing_data[run_number] = face
            except ValueError:
                print(f"Skipping row with invalid data: {row}")
            except KeyError as e:
                print(f"Missing column in the row: {row}, Error: {e}")

    return facing_data

def write_xyz_to_csv(image_numbers, cluster_numbers, x, y, z, output_csv_path):
    new_fieldnames = ['Image Number', 'Cluster Number', 'x', 'y', 'z']

    with open(output_csv_path, mode='w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(new_fieldnames)

        for i in range(len(x)):
            csv_writer.writerow([image_numbers[i], cluster_numbers[i], x[i], y[i], z[i]])

# Paths to your CSV files
csv_path = '/Users/kaixinxue/Desktop/M400/Attempt3/phi_theta.csv'
robot_path = '/Users/kaixinxue/Desktop/M400/Attempt3/robotPosition.csv'
output_csv_path = '/Users/kaixinxue/Desktop/M400/Attempt3/xyz_coordinates.csv'

image_numbers, cluster_numbers, phi_values, theta_values = read_phi_rho_from_csv(csv_path)
facing_data = read_robot_facing_from_csv(robot_path)

# Modify phi values based on robot facing direction
phi_values = [(phi + facing_data[image_num]) for phi, image_num in zip(phi_values, image_numbers)]

phi_array = np.array(phi_values)
theta_array = np.array(theta_values)
phi_radians = phi_array * np.pi / 180
theta_radians = theta_array * np.pi / 180

x = np.sin(phi_radians) * np.sin(theta_radians)
y = np.cos(phi_radians) * np.sin(theta_radians)
z = np.cos(theta_radians)

write_xyz_to_csv(image_numbers, cluster_numbers, x, y, z, output_csv_path)

print("x, y, z have been written to:", output_csv_path)