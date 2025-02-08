# Lane Marking Labeling and Segmentation

This repository contains two Python scripts for lane marking labeling and segmentation in image sequences. The scripts facilitate manual labeling of lane points and automate the labeling process for subsequent frames. Additionally, segmentation masks are generated from the labeled points for training purposes.

## Files

### 1. `manual_labeling.py`
This script allows for manual annotation of lane markings on images and automates the labeling process for subsequent frames. The user manually selects lane points, and the script generates `.lines.txt` files containing the labeled points. It also enables automatic adjustment of lane points for consecutive frames based on user-defined directions.

#### **Key Features:**
- Allows manual selection of lane points on an image.
- Supports setting lane directions (left, right, up, down, straight) using arrow keys.
- Saves labeled points in `.lines.txt` files.
- Automates lane point adjustments for subsequent frames.
- Displays annotated frames for visualization.

#### **Usage:**
Modify the `input_dir` and `output_dir` variables to match your dataset structure. Run:
```bash
python manual_labeling.py
```

#### **Instructions for Use:**
- **Mouse Left-click**: Select a lane point.
- **'k' key**: Save the current lane and start a new one.
- **Arrow keys**: Set direction (Left, Right, Up, Down, default is Straight).
- **'Enter' key**: Finish selection and proceed.

---

### 2. `make_seg.py`
This script generates segmentation masks from lane markings stored in `.lines.txt` files. It reads image paths from `train.txt`, processes each image, and creates segmentation masks by connecting lane points with lines.

#### **Key Features:**
- Reads labeled points from `.lines.txt` files.
- Generates binary lane segmentation masks.
- Saves masks in a new directory (`laneseg_label_w16/images`).
- Updates the training file with new image-mask paths.

#### **Usage:**
Modify the `base_dir` variable to your dataset location. Run:
```bash
python make_seg.py
```

#### **Output:**
- The masks are saved as `.png` files in `laneseg_label_w16/images`.
- The updated `x_train.txt` file contains new image-mask paths.

---

## Setup
Ensure you have the required dependencies installed:
```bash
pip install opencv-python numpy
```

## Project Structure
```
repo/
│── manual_labeling.py  # Manual labeling and automation script
│── make_seg.py         # Lane segmentation mask generation script
│── datasets/
│   ├── assisttaxi2/
│   │   ├── train/
│   │   │   ├── images/  # Original images
│   │   │   ├── train.txt  # List of training images
│   │   │   ├── laneseg_label_w16/  # Output segmentation masks
│   ├── valid/
│   │   ├── images2/  # Validation images
│   │   ├── processed_images/  # Processed images with annotations
```

## Notes
- Ensure images are stored in the correct directories before running the scripts.
- Adjust `step_size` and `adjustment_factor` in `manual_labeling.py` for optimal automation.
