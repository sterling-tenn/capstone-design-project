import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect_generalized_edges(image_path, scale_percent=50, blur_kernel_size=(15, 15), canny_threshold1=50, canny_threshold2=150, dilation_iterations=2, closing_kernel_size=(10, 10)):
    """
    Detects generalized edges in an image by resizing the image, applying a larger blur,
    detecting edges, removing thin lines, and dilating the edges.

    :param image_path: Path to the image file.
    :param scale_percent: Percent of the original size to scale the image.
    :param blur_kernel_size: Size of the Gaussian blur kernel.
    :param canny_threshold1: First threshold for the hysteresis procedure in Canny.
    :param canny_threshold2: Second threshold for the hysteresis procedure in Canny.
    :param dilation_iterations: Number of times to apply dilation.
    :param closing_kernel_size: Size of the kernel used in morphological closing.
    :return: A 2D array representing thick, generalized edges.
    """
    # Read the image
    image = cv2.imread(image_path)
    # Resize the image
    image = cv2.resize(image, (int(image.shape[1] * scale_percent / 100), int(image.shape[0] * scale_percent / 100)), interpolation=cv2.INTER_AREA)
    # Convert to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a larger blur
    blurred_image = cv2.GaussianBlur(image, blur_kernel_size, 0)
    # Detect edges using Canny
    edges = cv2.Canny(blurred_image, canny_threshold1, canny_threshold2)

    # Remove thin lines using morphological closing
    closing_kernel = np.ones(closing_kernel_size, np.uint8)
    closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, closing_kernel)

    # Dilate the edges to make them thicker
    dilation_kernel = np.ones((5, 5), np.uint8)
    dilated_edges = cv2.dilate(closed_edges, dilation_kernel, iterations=dilation_iterations)

    return dilated_edges
def average_pooling(array, pool_size):
    """
    Reduces the size of an array by averaging over non-overlapping square blocks.

    :param array: The original 2D array (e.g., an image).
    :param pool_size: The size of the square block to average over (e.g., (2, 2) for 2x2 blocks).
    :return: A smaller 2D array with each value being the average of a block.
    """
    # Calculate the shape of the output array
    output_shape = (
        array.shape[0] // pool_size[0],
        array.shape[1] // pool_size[1]
    )

    # Initialize the output array
    pooled_array = np.zeros(output_shape, dtype=array.dtype)

    # Iterate over each block in the array
    for i in range(output_shape[0]):
        for j in range(output_shape[1]):
            # Extract the block from the original array
            block = array[
                i * pool_size[0]:(i + 1) * pool_size[0],
                j * pool_size[1]:(j + 1) * pool_size[1]
            ]

            # Calculate the average of the block, and round to the nearest integer
            pooled_array[i, j] = round(np.mean(block) / 255) * 255

    return pooled_array
def display_edges(edges_array):
    """
    Displays a 2D NumPy array of edges as a grayscale image.

    :param edges_array: A 2D NumPy array representing the edges in the image.
    """
    # Display the image in grayscale
    plt.imshow(edges_array, cmap='gray')
    # Hide axis labels
    plt.axis('off')
    # Display the image
    plt.show()

def main(image_path):
    edges = detect_generalized_edges(image_path)
    pooled_edges = average_pooling(edges, pool_size=(6, 6))
    print(len(pooled_edges),len(pooled_edges[0]))
    display_edges(pooled_edges)

if __name__ == '__main__':
    import sys
    main(sys.argv[1])

