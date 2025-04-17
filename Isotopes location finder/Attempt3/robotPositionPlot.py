import sys
import pandas as pd
import matplotlib.pyplot as plt

def plot_2d_trajectory(trajectory_csv, points_csv):
    # Close all existing figures
    plt.close('all')
    
    # Read the main trajectory CSV file
    trajectory_df = pd.read_csv(trajectory_csv)
    trajectory_df['x'] = pd.to_numeric(trajectory_df['x'], errors='coerce')
    trajectory_df['y'] = pd.to_numeric(trajectory_df['y'], errors='coerce')
    trajectory_df.dropna(subset=['x', 'y'], inplace=True)

    # Read the additional points CSV file
    points_df = pd.read_csv(points_csv)
    points_df['Closest Point X'] = pd.to_numeric(points_df['Closest Point X'], errors='coerce')
    points_df['Closest Point Y'] = pd.to_numeric(points_df['Closest Point Y'], errors='coerce')
    points_df.dropna(subset=['Closest Point X', 'Closest Point Y'], inplace=True)

    # Create a 2D plot
    plt.figure()
    
    # Plot the trajectory with a thinner line
    plt.plot(trajectory_df['x'], trajectory_df['y'], label='Trajectory', marker='', linestyle='-', linewidth=0.5)

    # Plot the additional points as smaller red dots
    plt.scatter(points_df['Closest Point X'], points_df['Closest Point Y'], color='red', s=10, label='Points of Interest')
    
    # Axes Labels
    plt.xlabel('X (meters)')
    plt.ylabel('Y (meters)')
    plt.title('2D Trajectory in XY Plane')

    # Show the plot
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Check if both CSV files are specified
    if len(sys.argv) != 3:
        print("Usage: python script.py <trajectory_csv> <points_csv>")
        sys.exit(1)

    trajectory_csv = sys.argv[1]
    points_csv = sys.argv[2]

    plot_2d_trajectory(trajectory_csv, points_csv)
