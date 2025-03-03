# TO INSTALL OpenCV ON RASPBERRY PI. PIP CAUSES error: externally-managed-environment
# sudo apt install python3-venv

import cv2
import numpy as np
import os
from astar import Astar
import json

# kumar: this changed from bw to clr image detection to detect that green and red start and destination dot respectively
# the bitmap looks fine tho to me, also gpt code so haha idk how things work here.

def detect_generalized_edges(image_path, scale_percent=50, blur_kernel_size=(15, 15), 
                             canny_threshold1=50, canny_threshold2=150, dilation_iterations=2, 
                             closing_kernel_size=(10, 10)):
    """
    Detects generalized edges in an image and also returns the resized color image for further processing.
    """
    # Read the original color image
    color_image = cv2.imread(image_path)

    # Resize the image
    width = int(color_image.shape[1] * scale_percent / 100)
    height = int(color_image.shape[0] * scale_percent / 100)
    resized_color_image = cv2.resize(color_image, (width, height), interpolation=cv2.INTER_AREA)

    # Convert to grayscale for edge detection
    gray_image = cv2.cvtColor(resized_color_image, cv2.COLOR_BGR2GRAY)

    # Apply a larger blur
    blurred_image = cv2.GaussianBlur(gray_image, blur_kernel_size, 0)

    # Detect edges using Canny
    edges = cv2.Canny(blurred_image, canny_threshold1, canny_threshold2)

    # Remove thin lines using morphological closing
    closing_kernel = np.ones(closing_kernel_size, np.uint8)
    closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, closing_kernel)

    # Dilate the edges to make them thicker
    dilation_kernel = np.ones((5, 5), np.uint8)
    dilated_edges = cv2.dilate(closed_edges, dilation_kernel, iterations=dilation_iterations)

    return dilated_edges, resized_color_image  # Return both grayscale edges and color image


def average_pooling_binary(array, pool_size, threshold=127):
    """
    Reduces the size of an array by averaging over non-overlapping square blocks 
    and converts it into a binary map of 0s and 1s.

    :param array: The original 2D array (e.g., an image).
    :param pool_size: The size of the square block to average over (e.g., (2,2) for 2x2 blocks).
    :param threshold: The threshold to determine filled (1) or not filled (0).
    :return: A smaller 2D binary array.
    """
    output_shape = (
        array.shape[0] // pool_size[0],
        array.shape[1] // pool_size[1]
    )

    binary_array = np.zeros(output_shape, dtype=np.uint8)

    for i in range(output_shape[0]):
        for j in range(output_shape[1]):
            block = array[
                i * pool_size[0]:(i + 1) * pool_size[0],
                j * pool_size[1]:(j + 1) * pool_size[1]
            ]
            # If the average intensity is above the threshold, mark as 1 (filled), else 0
            binary_array[i, j] = 1 if np.mean(block) > threshold else 0

    return binary_array

# def display_edges(edges_array):
#     """
#     Displays a 2D NumPy array of edges as a grayscale image.

#     :param edges_array: A 2D NumPy array representing the edges in the image.
#     """
#     # Display the image in grayscale
#     plt.imshow(edges_array, cmap='gray')
#     # Hide axis labels
#     plt.axis('off')
#     # Display the image
#     plt.show()

def detect_red_marker(image):
    """
    Detects a red marker in an image using HSV color thresholding.
    Returns the center coordinates (x, y) of the red marker or None if not found.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define red color range in HSV
    lower_red1, upper_red1 = np.array([0, 120, 70]), np.array([10, 255, 255])
    lower_red2, upper_red2 = np.array([170, 120, 70]), np.array([180, 255, 255])

    # Create masks for red detection
    mask = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)

    # Find contours of the detected red areas
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)

        if M["m00"] != 0:  # Avoid division by zero
            cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            return cx, cy  # Center of the detected red marker
    return None  # No marker found

def detect_green_marker(image):
    """
    Detects a green marker in an image using HSV color thresholding.
    Returns the center coordinates (x, y) of the green marker or None if not found.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define green color range in HSV
    lower_green = np.array([40, 40, 40])   # Adjusted for better detection
    upper_green = np.array([90, 255, 255]) # Covers most shades of green

    # Create mask for green detection
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours of the detected green areas
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)

        if M["m00"] != 0:  # Avoid division by zero
            cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            return cx, cy  # Center of the detected green marker

    return None  # No green marker found


def mark_on_bitmap(binary_array, green_marker_coords, red_marker_coords, image_shape):
    """
    Marks the detected green and red marker on the binary map.
    """
    
    if green_marker_coords:
        marker_x = green_marker_coords[0] * binary_array.shape[1] // image_shape[1]
        marker_y = green_marker_coords[1] * binary_array.shape[0] // image_shape[0]

        # Ensure marker is within bounds
        marker_x = min(marker_x, binary_array.shape[1] - 1)
        marker_y = min(marker_y, binary_array.shape[0] - 1)

        binary_array[marker_y, marker_x] = 2  # Start marker

    if red_marker_coords:
        marker_x = red_marker_coords[0] * binary_array.shape[1] // image_shape[1]
        marker_y = red_marker_coords[1] * binary_array.shape[0] // image_shape[0]

        # Ensure marker is within bounds
        marker_x = min(marker_x, binary_array.shape[1] - 1)
        marker_y = min(marker_y, binary_array.shape[0] - 1)

        binary_array[marker_y, marker_x] = 3  # Destination marker

    return binary_array


def save_binary_map_txt(binary_array, output_path):
    """
    Saves the binary map as a text file with 0s, 1s, and 2s (for the red marker).
    """
    np.savetxt(output_path, binary_array, fmt='%d', delimiter='')
    

def convert_bitmap_txt_to_coordinates(file_path="binary_map.txt", grid_scale=1):
    """
    Reads a bitmap text file and converts it into a coordinate system where (0,0) is at the bottom-left.
    """
    if not os.path.exists(file_path):
        print(f"❌ File '{file_path}' not found.")
        return None

    try:
        # Read the file into a list of rows
        with open(file_path, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        if not lines:
            print(f"❌ Error: The file '{file_path}' is empty.")
            return None

        # Convert to 2D array
        binary_map = np.array([list(map(int, list(row))) for row in lines])

        height, width = binary_map.shape
        obstacles, open_space = [], []
        start_point, destination_point = None, None

        # Flip Y-axis so (0,0) is bottom-left
        for y in range(height):
            for x in range(width):
                real_x = x * grid_scale
                real_y = (height - y - 1) * grid_scale  # Flip Y

                if binary_map[y, x] == 1:
                    obstacles.append((real_x, real_y))
                elif binary_map[y, x] == 0:
                    open_space.append((real_x, real_y))
                elif binary_map[y, x] == 2:
                    start_point = (real_x, real_y)
                elif binary_map[y, x] == 3:
                    destination_point = (real_x, real_y)

        astar_path = []
 
        if start_point and destination_point:
            pathfinder = Astar(height, width, obstacles, start_point, destination_point)
            astar_path = pathfinder.find_path()
        else:
            print("Missing start or destination marker in the file.")

        data = {
            "obstacles": obstacles,
            "dimensions": [width, height],
            "path": astar_path,
        }

        # Save to JSON
        with open("map.json", "w") as f:
            json.dump({
                "obstacles": obstacles,
                "dimensions": [width, height],
            }, f)
            
        with open("path.json", "w") as f:
            json.dump({"path": astar_path}, f)

        return data

    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None



def generate(image_path):
    """
    Full pipeline:
    - Detects edges
    - Converts them into a binary map
    - Detects a red marker in the image
    - Marks the red marker as '2' in the binary map
    - Saves the final binary map as a text file
    """
    edges, resized_image = detect_generalized_edges(image_path)
    pooled_edges = average_pooling_binary(edges, pool_size=(6, 6))

    red_marker_coords = detect_red_marker(resized_image)
    green_marker_coords = detect_green_marker(resized_image)
    
    print(f"Red Marker Found At: {red_marker_coords}")
    print(f"Green Marker Found At: {green_marker_coords}")
    
    # Update binary map with markers
    updated_map = mark_on_bitmap(pooled_edges, green_marker_coords, red_marker_coords, resized_image.shape)

    # Save updated binary map
    save_binary_map_txt(updated_map, "binary_map.txt")

    print("✅ Binary map generated and saved as binary_map.txt")

# generate("floorplans.png")
# print(convert_bitmap_txt_to_coordinates())