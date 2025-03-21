import rospy
import rosbag
from nav_msgs.msg import Odometry
import csv
import sys

def read_bag_to_csv(bag_file_path, csv_file_path, topic_name='/odom'):
    try:
        # Open the bag file
        bag = rosbag.Bag(bag_file_path, 'r')

        # Open the CSV file for writing
        with open(csv_file_path, mode='w') as csv_file:
            csv_writer = csv.writer(csv_file)
            # Write the CSV header
            csv_writer.writerow(["timestamp", "x", "y", "z", "ox", "oy", "oz", "ow"])

            # Iterate through the bag messages
            for topic, msg, t in bag.read_messages(topics=[topic_name]):
                # Extract data
                x = msg.pose.pose.position.x
                y = msg.pose.pose.position.y
                z = msg.pose.pose.position.z
                ox = msg.pose.pose.orientation.x
                oy = msg.pose.pose.orientation.y
                oz = msg.pose.pose.orientation.z
                ow = msg.pose.pose.orientation.w
                timestamp = t.to_sec()

                # Write to CSV
                csv_writer.writerow([timestamp, x, y, z, ox, oy, oz, ow])

                rospy.loginfo("Odometry data written to CSV: [%f, %f, %f, %f, %f, %f, %f, %f]",
                              timestamp, x, y, z, ox, oy, oz, ow)

        # Close the bag file
        bag.close()
        rospy.loginfo(f"Finished writing to {csv_file_path}")

    except rosbag.ROSBagException as e:
        rospy.logerr(f"Error reading bag file: {e}")
    except IOError as e:
        rospy.logerr(f"Error writing CSV file: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script_name.py <input_bag_file.bag> <output_file.csv>")
        sys.exit(1)

    input_bag_path = sys.argv[1]
    output_csv_path = sys.argv[2]

    # Call the function to read bag and write CSV
    read_bag_to_csv(input_bag_path, output_csv_path)