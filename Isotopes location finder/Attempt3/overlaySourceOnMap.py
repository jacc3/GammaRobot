import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy.ndimage import rotate

def plot_trajectory_with_map(trajectory_csv, points_csv, map_png, angle_degrees=0, scale_factor=1.0, shift_x=0.0, shift_y=0.0, flip_left_right=False, flip_up_down=False):
    # Close all existing figures
    plt.close('all')
    
    # Load the 2D map image
    map_img = mpimg.imread(map_png)
    
    # Rotate the map image
    rotated_map = rotate(map_img, angle_degrees, reshape=True, mode='nearest')

    # Flip the map left to right if specified
    if flip_left_right:
        rotated_map = np.fliplr(rotated_map)

    # Flip the map up to down if specified
    if flip_up_down:
        rotated_map = np.flipud(rotated_map)

    # Read trajectory data
    trajectory_df = pd.read_csv(trajectory_csv)
    trajectory_df['x'] = pd.to_numeric(trajectory_df['x'], errors='coerce')
    trajectory_df['y'] = pd.to_numeric(trajectory_df['y'], errors='coerce')
    trajectory_df.dropna(subset=['x', 'y'], inplace=True)

    # Read additional points data
    points_df = pd.read_csv(points_csv)
    points_df['Closest Point X'] = pd.to_numeric(points_df['Closest Point X'], errors='coerce')
    points_df['Closest Point Y'] = pd.to_numeric(points_df['Closest Point Y'], errors='coerce')
    points_df.dropna(subset=['Closest Point X', 'Closest Point Y'], inplace=True)

    # Create a plot
    fig, ax = plt.subplots()

    # Calculate the extent while considering the scaling and shifting
    x_min, x_max = trajectory_df['x'].min(), trajectory_df['x'].max()
    y_min, y_max = trajectory_df['y'].min(), trajectory_df['y'].max()
    extent = [
        x_min * scale_factor + shift_x, x_max * scale_factor + shift_x,
        y_min * scale_factor + shift_y, y_max * scale_factor + shift_y
    ]

    # Display the transformed map image
    ax.imshow(rotated_map, extent=extent, origin='lower', alpha=1)

    # Plot the trajectory
    plt.plot(trajectory_df['x'], trajectory_df['y'], label='Trajectory', color='red', linestyle='-', linewidth=1, marker='')

    # Plot the additional points as smaller red dots
    plt.scatter(points_df['Closest Point X'], points_df['Closest Point Y'], color='red', s=10, label='Points of Interest')
    
    # Axes Labels
    plt.xlabel('X (meters)')
    plt.ylabel('Y (meters)')
    plt.title('2D Trajectory with Adjusted Map')

    # Show the plot
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Ensure enough arguments are specified
    if len(sys.argv) != 10:
        print("Usage: python script.py <trajectory_csv> <points_csv> <map_png> <angle> <scale> <shift_x> <shift_y> <flip_lr> <flip_ud>")
        sys.exit(1)

    trajectory_csv = sys.argv[1]
    points_csv = sys.argv[2]
    map_png = sys.argv[3]
    angle_degrees = float(sys.argv[4])
    scale_factor = float(sys.argv[5])
    shift_x = float(sys.argv[6])
    shift_y = float(sys.argv[7])
    flip_left_right = sys.argv[8].lower() in ['true', '1', 'yes']
    flip_up_down = sys.argv[9].lower() in ['true', '1', 'yes']

    plot_trajectory_with_map(trajectory_csv, points_csv, map_png, angle_degrees, scale_factor, shift_x, shift_y, flip_left_right, flip_up_down)
