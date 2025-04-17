import csv
import numpy as np
from collections import defaultdict
from itertools import combinations

def read_xyz_with_metadata(csv_file_path):
    unique_rows = set()  # Track unique rows
    x_values, y_values, z_values = [], [], []
    image_numbers, cluster_numbers = [], []

    with open(csv_file_path, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Create a tuple of row data excluding keys/case-sensitive issues
            row_tuple = tuple(row.items())
            if row_tuple not in unique_rows:
                unique_rows.add(row_tuple)
                try:
                    x_values.append(float(row['x']))
                    y_values.append(float(row['y']))
                    z_values.append(float(row['z']))
                    image_numbers.append(int(row['Image Number']))
                    cluster_numbers.append(int(row['Cluster Number']))
                except (ValueError, KeyError) as e:
                    print(f"Skipping row due to error: {row}, {e}")

    return x_values, y_values, z_values, image_numbers, cluster_numbers

def read_robot_positions(csv_file_path):
    positions = {}
    unique_rows = set()  # Track unique rows

    with open(csv_file_path, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Create a tuple of row data for uniqueness checking
            row_tuple = tuple(row.items())
            if row_tuple not in unique_rows:
                unique_rows.add(row_tuple)
                try:
                    positions[int(row['Run Number'])] = (
                        float(row['x']), float(row['y']), float(row['z'])
                    )
                except (ValueError, KeyError) as e:
                    print(f"Skipping row due to error: {row}, {e}")
    return positions

def closest_point_between_lines(lines):
    points = np.array([line[0] for line in lines])
    directions = np.array([line[1] for line in lines])

    A = np.zeros((3, 3))
    b = np.zeros(3)
    for point, direction in zip(points, directions):
        d = direction[:, np.newaxis]
        P = np.eye(3) - np.dot(d, d.T) / np.dot(direction, direction)
        A += P
        b += P @ point

    try:
        closest_point = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        closest_point = np.full(3, np.nan)

    return closest_point

def calculate_distance_from_lines(closest_point, lines):
    total_distance = 0
    count = 0
    for point, direction in lines:
        line_point = point + direction * np.dot((closest_point - point), direction) / np.dot(direction, direction)
        total_distance += np.linalg.norm(line_point - closest_point)
        count += 1
    return total_distance / count if count > 0 else float('inf')

def optimize_cluster_selection(robot_positions, direction_data):
    organized_data = defaultdict(lambda: defaultdict(list))
    for dx, dy, dz, img_num, cluster_num in zip(*direction_data):
        if img_num in robot_positions:
            rx, ry, rz = robot_positions[img_num]
            organized_data[img_num][cluster_num].append((np.array([rx, ry, rz]), np.array([dx, dy, dz])))

    result_points = []
    all_combinations = []

    # Collect all possible image-cluster pairs
    for img in organized_data:
        for cluster in organized_data[img]:
            all_combinations.append((img, cluster))

    max_clusters = 2  # Given two clusters per image
    num_images = len(organized_data)  # The number of images

    # Iterate over combinations for calculation
    for first_combo in combinations(all_combinations, num_images):
        if len(set(img for img, _ in first_combo)) == num_images:
            remaining_combinations = [c for c in all_combinations if c not in first_combo]

            for second_combo in combinations(remaining_combinations, num_images):
                if len(set(img for img, _ in second_combo)) == num_images:
                    # Calculate closest point for each valid combo
                    used_clusters = set(first_combo)
                    first_lines = sum((organized_data[img][cluster] for img, cluster in first_combo), [])
                    first_cp = closest_point_between_lines(first_lines)
                    first_avg_dist = calculate_distance_from_lines(first_cp, first_lines)

                    if not np.isnan(first_cp).any():
                        used_clusters.update(second_combo)
                        second_lines = sum((organized_data[img][cluster] for img, cluster in second_combo), [])
                        second_cp = closest_point_between_lines(second_lines)
                        second_avg_dist = calculate_distance_from_lines(second_cp, second_lines)

                        if not np.isnan(second_cp).any():
                            combined_avg_dist = (first_avg_dist + second_avg_dist) / 2
                            result_points.append((first_combo, first_cp, second_combo, second_cp, combined_avg_dist))

    # Sort and choose combinations with the smallest distance
    result_points.sort(key=lambda x: x[4])
    selected_points = result_points[:max_clusters]  # Select top combinations

    # Format for CSV output
    output = []
    for first_combo, first_cp, second_combo, second_cp, _ in selected_points:
        output.append((first_combo, first_cp))
        output.append((second_combo, second_cp))
    
    return output

def write_to_csv(results, csv_filepath):
    with open(csv_filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Combination", "Closest Point X", "Closest Point Y", "Closest Point Z"])
        for combos, closest_point in results:
            combo_info = "; ".join(f"{img}-{cluster}" for img, cluster in combos)
            writer.writerow([combo_info] + closest_point.tolist())

# File paths
direction_path = '/Users/kaixinxue/Desktop/M400/Attempt3/xyz_coordinates.csv'
robot_path = '/Users/kaixinxue/Desktop/M400/Attempt3/robotPosition.csv'
output_path = '/Users/kaixinxue/Desktop/M400/Attempt3/closest_points.csv'

# Read CSV data
direction_data = read_xyz_with_metadata(direction_path)
robot_positions = read_robot_positions(robot_path)

# Compute closest points optimizing cluster selection
closest_point_results = optimize_cluster_selection(robot_positions, direction_data)

# Write results to a CSV
write_to_csv(closest_point_results, output_path)
