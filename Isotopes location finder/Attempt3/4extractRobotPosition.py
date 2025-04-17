import pandas as pd
from scipy.spatial.transform import Rotation as R
import numpy as np
import sys
import csv

def find_closest_row(df, timestamp):
    # Ensure the timestamp column is numeric
    df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')

    # Find the index of the row with the closest timestamp
    closest_index = (df['timestamp'] - timestamp).abs().idxmin()

    # Extract the relevant values for position and quaternion
    closest_row = df.loc[closest_index, ['x', 'y', 'z', 'ox', 'oy', 'oz', 'ow']]

    # Extract the quaternion components
    q = [closest_row['ox'], closest_row['oy'], closest_row['oz'], closest_row['ow']]

    # Convert quaternion to Euler angles (roll, pitch, yaw)
    r = R.from_quat(q)
    roll, pitch, yaw = r.as_euler('xyz', degrees=False)

    return closest_row, roll, pitch, yaw

def euler_to_spherical(roll, pitch, yaw):
    # Calculate the spherical coordinates
    phi = yaw  # Azimuthal angle
    theta = np.pi / 2 - pitch  # Polar angle

    # Assume unit radius
    r = 1.0

    # Convert radians to degrees
    phi = np.degrees(phi)
    theta = np.degrees(theta)

    return r, theta, phi

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <timestamp1> <timestamp2> ...")
        sys.exit(1)

    # Specify the fixed path to the CSV file
    csv_file = '/Users/kaixinxue/Desktop/M400/Attempt3/odometryData.csv'
    
    # Convert input arguments to a list of timestamps
    timestamps = [float(ts) for ts in sys.argv[1:]]

    # Load CSV just once
    df = pd.read_csv(csv_file)

    # Prepare results for CSV
    results = []

    # Iterate over the timestamps and process each
    for idx, timestamp in enumerate(timestamps):
        closest_values, roll, pitch, yaw = find_closest_row(df, timestamp)
        r, theta, phi = euler_to_spherical(roll, pitch, yaw)

        # Collect results with the index of the run
        results.append([idx + 1, closest_values['x'], closest_values['y'], closest_values['z'], phi])

    # Output file path
    output_csv = 'robotPosition.csv'

    # Write the robotPosition to a CSV file
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Run Number', 'x', 'y', 'z', 'facing'])
        # Write the data
        writer.writerows(results)

    print(f"Results have been written to {output_csv}")