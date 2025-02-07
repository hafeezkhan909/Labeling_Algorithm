import os
import cv2
import numpy as np

def visualize_and_save_lane_markings(base_dir, train_txt, output_dir, new_train_txt):
    # Create output directory for masks if it doesn't exist
    mask_dir = os.path.join(output_dir, 'images')
    if not os.path.exists(mask_dir):
        os.makedirs(mask_dir)

    # Open the new_train.txt to store the updated paths
    with open(new_train_txt, 'w') as new_train_file:
        # Read the image paths from train.txt
        with open(train_txt, 'r') as train_file:
            image_paths = train_file.readlines()
            
            for img_path in image_paths:
                img_path = img_path.strip()  # Remove any leading/trailing whitespaces
                # Construct full image path
                full_image_path = os.path.join(base_dir, img_path)
                # Construct corresponding .lines.txt path
                full_lines_path = full_image_path.replace('.jpg', '.lines.txt')

                # Load the image
                image = cv2.imread(full_image_path)
                if image is None:
                    print(f"Error: Could not load image from {full_image_path}")
                    continue

                # Create a blank mask of the same size as the image
                mask = np.zeros_like(image)

                # Read points from the .lines.txt file and plot them onto the mask
                try:
                    with open(full_lines_path, 'r') as lines_file:
                        lines = lines_file.readlines()
                        for index, line in enumerate(lines):
                            points = line.strip().split()
                            points_x = []
                            points_y = []

                            # Extract x, y points from each line
                            for i in range(0, len(points), 2):
                                x = int(round(float(points[i])))  # Round and convert to integer
                                y = int(round(float(points[i + 1])))  # Round and convert to integer
                                points_x.append(x)
                                points_y.append(y)

                            # Draw lines connecting the points on the mask
                            for ptStart, ptEnd in zip(range(len(points_x) - 1), range(1, len(points_y))):
                                pt1 = (points_x[ptStart], points_y[ptStart])
                                pt2 = (points_x[ptEnd], points_y[ptEnd])
                                if 0 <= pt1[0] < image.shape[1] and 0 <= pt1[1] < image.shape[0] and \
                                   0 <= pt2[0] < image.shape[1] and 0 <= pt2[1] < image.shape[0]:  # Ensure points are within bounds
                                    cv2.line(mask, pt1, pt2, [(index+1)]*4, 3, lineType=cv2.LINE_8)  # Draw lines on the mask

                except Exception as e:
                    print(f"Error reading or plotting points from {full_lines_path}: {e}")
                    continue

                # Save the mask as a PNG file in the output directory
                mask_filename = os.path.join(mask_dir, os.path.basename(full_image_path).replace('.jpg', '.png'))
                cv2.imwrite(mask_filename, mask)

                # Write the new paths to new_train.txt
                new_train_file.write(f"{img_path} train/laneseg_label_w16/images/{os.path.basename(mask_filename)}\n")

    print(f"Finished processing and saving masks. Updated paths saved to {new_train_txt}")

# Example usage
base_dir = 'datasets/assisttaxi2/train'  # Base directory containing images and labels
train_txt = os.path.join(base_dir, 'train.txt')  # Path to the train.txt file
output_dir = os.path.join(base_dir, 'laneseg_label_w16')
new_train_txt = os.path.join(base_dir, 'x_train.txt')  # Path to store the updated train.txt

visualize_and_save_lane_markings(base_dir, train_txt, output_dir, new_train_txt)
