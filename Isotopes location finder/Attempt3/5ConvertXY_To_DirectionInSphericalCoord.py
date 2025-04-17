import csv
from PIL import Image
import numpy as np
from sklearn.cluster import DBSCAN
import os

def is_similar_color(r, g, b, target, tolerance):
    """Check if a pixel color is within a tolerance of the target color."""
    distance = np.sqrt((r - target[0]) ** 2 + (g - target[1]) ** 2 + (b - target[2]) ** 2)
    return distance <= tolerance

def calculate_midpoints(image_path, target_color=(135, 0, 1), tolerance=100, eps=30, min_samples=5):
    coordinates = []

    with Image.open(image_path) as img:
        img = img.convert('RGB')

        # Define the crop region: top-left (5, 5), and 466x324 size
        crop_bounds = (5, 5, 5 + 466, 5 + 324)

        # Print the crop bounds
        print(f"Cropping {image_path} with bounds: (left={crop_bounds[0]}, top={crop_bounds[1]}, right={crop_bounds[2]}, bottom={crop_bounds[3]})")

        # Crop the image
        cropped_img = img.crop(crop_bounds)

        # Save the cropped image
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        cropped_image_path = f"{base_name}_cropped.png"
        cropped_img.save(cropped_image_path)

        # Process only the cropped part of the image
        pixels = cropped_img.load()
        cropped_width, cropped_height = cropped_img.size

        for y in range(cropped_height):
            for x in range(cropped_width):
                r, g, b = pixels[x, y]
                if is_similar_color(r, g, b, target_color, tolerance):
                    coordinates.append((x, y))

    if not coordinates:
        return []

    # Use DBSCAN for clustering
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(coordinates)
    labels = clustering.labels_

    midpoints = []
    for cluster_id in set(labels):
        if cluster_id == -1:
            continue

        cluster_points = np.array([coord for coord, label in zip(coordinates, labels) if label == cluster_id])
        if cluster_points.size > 0:
            midpoint_x = cluster_points[:, 0].mean()
            midpoint_y = cluster_points[:, 1].mean()
            midpoints.append((midpoint_x, midpoint_y))

    return midpoints

def process_images_to_csv(image_paths, output_csv_path):
    with open(output_csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Image Number', 'Cluster Number', 'Midpoint_X', 'Midpoint_Y'])

        for idx, image_path in enumerate(image_paths, start=1):
            midpoints = calculate_midpoints(image_path)
            for cluster_number, (midpoint_x, midpoint_y) in enumerate(midpoints, start=1):
                csv_writer.writerow([idx, cluster_number, midpoint_x, midpoint_y])

# Example usage: list of image paths
image_paths = [
    '/Users/kaixinxue/Desktop/M400/GammaRobotFinalTest/20250321-191133_GammaRobot_Final_Test_multi_01/20250321-191504_SS/mergedImage.jpg',
    '/Users/kaixinxue/Desktop/M400/GammaRobotFinalTest/20250321-191541_GammaRobot_Final_Test_multi_02/20250321-192003_SS/mergedImage.jpg',
    '/Users/kaixinxue/Desktop/M400/GammaRobotFinalTest/20250321-192053_GammaRobot_Final_Test_multi_03/20250321-192547_SS/imageMerged.jpg',
    '/Users/kaixinxue/Desktop/M400/GammaRobotFinalTest/20250321-192701_GammaRobot_Final_Test_multi_04/20250321-193120_SS/imageMerged.jpg',
    '/Users/kaixinxue/Desktop/M400/GammaRobotFinalTest/20250321-193251_GammaRobot_Final_Test_multi_05/20250321-193626_SS/imageMerged.jpg'
]

process_images_to_csv(image_paths, 'midpoints.csv')
