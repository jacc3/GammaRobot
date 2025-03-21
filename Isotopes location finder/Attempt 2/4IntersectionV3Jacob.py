import csv
import numpy as np

def read_xyz_from_csv(csv_file_path): #Read xyz unit direction from csv
    x_values = []
    y_values = []
    z_values = []

    # Open the CSV file
    with open(csv_file_path, mode='r', newline='') as csv_file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(csv_file)

        # Iterate through each row in the CSV
        for row in csv_reader:
            try:
                x = float(row['x'])
                y = float(row['y'])
                z = float(row['z'])
                x_values.append(x)
                y_values.append(y)
                z_values.append(z)
            except ValueError:
                print(f"Skipping row with invalid data: {row}")
            except KeyError as e:
                print(f"Missing column in the row: {row}, Error: {e}")

    return x_values, y_values, z_values

def read_robotPosition_from_csv(csv_file_path): #Read the robot position
    x_values = []
    y_values = []
    z_values = []
    facing = []

    # Open the CSV file
    with open(csv_file_path, mode='r', newline='') as csv_file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(csv_file)

        # Iterate through each row in the CSV
        for row in csv_reader:
            try:
                x = float(row['x'])
                y = float(row['y'])
                z = float(row['z'])
                x_values.append(x)
                y_values.append(y)
                z_values.append(z)
            except ValueError:
                print(f"Skipping row with invalid data: {row}")
            except KeyError as e:
                print(f"Missing column in the row: {row}, Error: {e}")

    return x_values, y_values, z_values


direction_path = '/home/jc/Downloads/m400/kaixin/xyz_coordinates.csv' #Unit direction of radioisotopes, csv directory
robot_path = '/home/jc/Downloads/m400/kaixin/robotPosition.csv' #Robot position, csv directory

direction_x, direction_y, direction_z = read_xyz_from_csv(direction_path)
robot_x, robot_y, robot_z = read_robotPosition_from_csv(robot_path)

def closest_point_between_lines(lines):
    """
    Find the closest point to multiple lines in 3D space.
    Each line is defined by a point and a direction vector.

    Parameters:
    - lines: List of tuples [(point1, direction1), (point2, direction2), ...]

    Returns:
    - np.ndarray : The closest point in 3D space.
    """
    points = np.array([line[0] for line in lines])
    directions = np.array([line[1] for line in lines])

    # Matrices for the algorithm
    A = np.zeros((3, 3))
    b = np.zeros(3)

    for point, direction in zip(points, directions):
        # Compute the projection matrix for each line
        d = direction[:, np.newaxis]  # Convert to column vector
        P = np.eye(3) - np.dot(d, d.T) / np.dot(direction, direction)
        A += P
        b += P @ point

    # Solve the system of equations to find the closest point
    closest_point = np.linalg.solve(A, b)

    return closest_point

Vector = list(zip(robot_x, robot_y, robot_z, direction_x, direction_y, direction_z))
lines = [
    (np.array([px, py, pz]), np.array([dx, dy, dz]))
    for px, py, pz, dx, dy, dz in Vector
]


closest_point = closest_point_between_lines(lines)
print("Closest point to all lines:", closest_point)



##
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Read the CSV file
df = pd.read_csv("robotPosition.csv")

# Plot the robot positions in 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['x'], df['y'], df['z'], marker='o', label='Robot Positions')
ax.scatter(closest_point[0], closest_point[1], closest_point[2], color='red', marker='x', s=100, label='Closest Point')
true_source = np.array([0, 10, 0])
ax.scatter(true_source[0], true_source[1], true_source[2], color='blue', marker='*', s=100, label='True Source Location')


# Label axes
ax.set_xlabel("X Position")
ax.set_ylabel("Y Position")
ax.set_zlabel("Z Position")
ax.set_title("Robot Position Path")
ax.legend()

# Show the plot
plt.show()
