import csv
from PIL import Image
import math
import os

def is_similar_color(r, g, b, target, tolerance):
    # Calculate the Euclidean distance between the current color and target color
    distance = math.sqrt((r - target[0]) ** 2 + (g - target[1]) ** 2 + (b - target[2]) ** 2)
    return distance <= tolerance

def calculate_midpoint(image_path, target_color=(135, 0, 1), tolerance=30):
    x_values = []
    y_values = []

    with Image.open(image_path) as img:
        img = img.convert('RGB')
        width, height = img.size # 1600 800
        pixels = img.load()

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                if is_similar_color(r, g, b, target_color, tolerance):
                    x_values.append(x)
                    y_values.append(y)
    
    if not x_values or not y_values:
        return None, None

    midpoint_x = sum(x_values) / len(x_values) #Find the midpoint of all the point read
    midpoint_y = sum(y_values) / len(y_values)

    return midpoint_x, midpoint_y

def process_images_to_csv(image_paths, output_csv_path): #Write the image position(midpoint) into a csv file
    with open(output_csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Image Number', 'Midpoint_X', 'Midpoint_Y'])

        for idx, image_path in enumerate(image_paths, start=1):
            midpoint_x, midpoint_y = calculate_midpoint(image_path)
            csv_writer.writerow([idx, midpoint_x, midpoint_y])

# Example usage: list of image paths
image_paths = [
    '/Users/kaixinxue/Desktop/M400/Attempt2/Data/Position1.jpg',
    '/Users/kaixinxue/Desktop/M400/Attempt2/Data/Position2.jpg',
    '/Users/kaixinxue/Desktop/M400/Attempt2/Data/Position3.jpg',
    '/Users/kaixinxue/Desktop/M400/Attempt2/Data/Position4.jpg'
]
#Output csv directory
process_images_to_csv(image_paths, 'midpoints.csv')