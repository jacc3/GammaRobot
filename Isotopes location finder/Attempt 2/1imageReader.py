import csv
from PIL import Image

def read_image_to_csv(image_path, output_csv_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Load image data
        img = img.convert('RGB')
        pixels = img.load()

        # Get image dimensions
        width, height = img.size

        # Open a CSV file for writing
        with open(output_csv_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the header
            csv_writer.writerow(['X', 'Y', 'R', 'G', 'B'])

            # Iterate through each pixel
            for y in range(height):
                for x in range(width):
                    # Access the pixel value at (x, y)
                    r, g, b = pixels[x, y]

                    # Check if the pixel matches the desired RGB value
                    if (r, g, b) == (135, 0, 1):
                        # Write the pixel data to the CSV file
                        csv_writer.writerow([x, y, r, g, b])

# Example usage: replace 'example.jpg' with your image path and 'output.csv' with your desired output file name
read_image_to_csv('/Users/kaixinxue/Desktop/M400/Attempt2/Data/Position1.jpg', 'Position1.csv')
read_image_to_csv('/Users/kaixinxue/Desktop/M400/Attempt2/Data/Position2.jpg', 'Position2.csv')
read_image_to_csv('/Users/kaixinxue/Desktop/M400/Attempt2/Data/Position3.jpg', 'Position3.csv')
read_image_to_csv('/Users/kaixinxue/Desktop/M400/Attempt2/Data/Position4.jpg', 'Position4.csv')