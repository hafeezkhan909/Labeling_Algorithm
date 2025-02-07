import os
import cv2
import numpy as np
import shutil
import time

# Global variables for storing points and direction
points = []
lanes_points = []  # List to store points for each lane
lane_directions = []  # List to store direction for each lane

def click_event(event, x, y, flags, param):
    """
    Mouse callback function to capture points on click.
    """
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        # Add the clicked point to the list
        points.append((x, y))
        # Visual feedback: draw a circle where clicked
        cv2.circle(param, (x, y), 4, (0, 0, 255), -1)
        cv2.imshow("Image", param)

def select_points(image, lines_file):
    """
    Allow the user to select points on the image and store them in the lines.txt file.
    User can press arrow keys to set direction for the lane's automation.
    """
    global points, lanes_points, lane_directions
    points = []  # Reset points for each image
    direction = 'straight'  # Default direction is straight
    img = image.copy()
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", click_event, img)

    while True:
        key = cv2.waitKey(0) & 0xFF

        if key == ord('k'):  # Start a new lane (store current lane and reset)
            save_points_to_file(lines_file)
            lanes_points.append(points.copy())  # Save points for this lane
            lane_directions.append(direction)  # Save the direction for this lane
            points = []  # Reset current lane points for new lane
            direction = 'straight'  # Reset direction

        elif key == 13:  # Enter key to finish selection
            if points:
                save_points_to_file(lines_file)  # Save the last lane
                lanes_points.append(points.copy())  # Save points for this lane
                lane_directions.append(direction)  # Save the direction for the last lane
            break

        elif key == ord('r'):  # Redo the current frame if needed
            print("Redoing the current frame...")
            points = []  # Clear all points
            img = image.copy()  # Reset the image
            cv2.imshow("Image", img)  # Redisplay the image for re-selection

        elif key == 81:  # Left arrow key
            print("Direction: Left")
            direction = 'left'

        elif key == 82:  # Up arrow key
            print("Direction: Up")
            direction = 'up'

        elif key == 83:  # Right arrow key
            print("Direction: Right")
            direction = 'right'

        elif key == 84:  # Down arrow key
            print("Direction: Down")
            direction = 'down'

    cv2.destroyAllWindows()

def save_points_to_file(file_path):
    """
    Save the collected points to the .lines.txt file.
    """
    global points
    with open(file_path, 'a') as file:
        file.write(' '.join(f'{x} {y}' for x, y in points) + '\n')

def auto_adjust_points(initial_points, frame_number, direction, adjustment_factor=1):
    """
    Automatically adjust points for the next frames by applying a small translation
    based on the selected direction.
    """
    if direction == 'left':
        adjusted_points = [(x - frame_number * adjustment_factor, y) for (x, y) in initial_points]
    elif direction == 'right':
        adjusted_points = [(x + frame_number * adjustment_factor, y) for (x, y) in initial_points]
    elif direction == 'up':
        adjusted_points = [(x, y - frame_number * 0.01) for (x, y) in initial_points]
    elif direction == 'down':
        adjusted_points = [(x, y + frame_number * adjustment_factor) for (x, y) in initial_points]
    else:  # Default is straight
        adjusted_points = [(x, y) for (x, y) in initial_points]

    return adjusted_points

def process_image_sequence(input_dir, output_dir, step_size=250, adjustment_factor=0.1):
    """
    Process the images and lines.txt files in sequence, allowing manual input every 60 frames
    and automating the next 59 frames with directional adjustments.
    """
    files = sorted([f for f in os.listdir(input_dir) if f.endswith('.jpg')], key=lambda x: int(x.split('.')[0]))

    for i in range(0, len(files), step_size):
        image_path = os.path.join(input_dir, files[i])
        lines_file = image_path.replace('.jpg', '.lines.txt')
        lines_file_output = os.path.join(output_dir, os.path.basename(lines_file))

        image = cv2.imread(image_path)

        print(f"Processing frame {i+1}/{len(files)} - {files[i]}")

        # 1. Manual point selection for the first frame in each set of 60 frames
        lanes_points.clear()  # Clear lane points for new image
        lane_directions.clear()  # Clear lane directions for new image
        select_points(image, lines_file_output)

        # 2. Automate for the next 59 frames
        for j in range(1, step_size):
            if i + j >= len(files):
                break
            next_image_path = os.path.join(input_dir, files[i + j])
            next_image = cv2.imread(next_image_path)
            next_lines_file_output = os.path.join(output_dir, os.path.basename(next_image_path).replace('.jpg', '.lines.txt'))

            # Adjust points for each lane based on its direction
            for lane_index, initial_lane_points in enumerate(lanes_points):
                direction = lane_directions[lane_index]
                adjusted_points = auto_adjust_points(initial_lane_points, j, direction, adjustment_factor)

                # Display the automated points on the next image for 1 second
                for x, y in adjusted_points:
                    cv2.circle(next_image, (int(x), int(y)), 4, (0, 255, 0), -1)  # Green circle for adjusted points

                # Save the adjusted points to the corresponding .lines.txt file
                with open(next_lines_file_output, 'a') as file:
                    file.write(' '.join(f'{x:.2f} {y:.2f}' for x, y in adjusted_points) + '\n')

            cv2.imshow("Automated Frame", next_image)
            cv2.waitKey(50)  # Display for 1 second

        cv2.destroyAllWindows()

# Example usage
input_dir = 'datasets/assisttaxi2/valid/images2'
output_dir = 'datasets/assisttaxi2/valid/processed_images'
os.makedirs(output_dir, exist_ok=True)

process_image_sequence(input_dir, output_dir, step_size=60, adjustment_factor=1.5)

print(f"Finished processing all images and saving them to {output_dir}.")
