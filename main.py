import numpy as np
import cv2

def generate_synthetic_image(width=256, height=256):
    """
    Generates a synthetic grayscale image with varying entropy regions.
    - Top-left: Solid black (low entropy)
    - Top-right: Solid white (low entropy)
    - Bottom-left: Solid mid-gray (low entropy)
    - Bottom-right: Random noise (high entropy)
    """
    img = np.zeros((height, width), dtype=np.uint8)

    # Top-left quadrant: Solid black (0)
    img[0:height//2, 0:width//2] = 0

    # Top-right quadrant: Solid white (255)
    img[0:height//2, width//2:width] = 255

    # Bottom-left quadrant: Solid mid-gray (128)
    img[height//2:height, 0:width//2] = 128

    # Bottom-right quadrant: Random noise
    noise = np.random.randint(0, 256, size=(height//2, width//2), dtype=np.uint8)
    img[height//2:height, width//2:width] = noise

    return img

def calculate_shannon_entropy(neighborhood):
    """
    Calculates the Shannon entropy of a given pixel neighborhood.
    The neighborhood is expected to be a 2D array (e.g., 3x3) of pixel values.
    """
    # Flatten the neighborhood to a 1D array for easier processing
    flat_neighborhood = neighborhood.flatten()

    # Get unique pixel values and their counts
    # np.unique is efficient for small arrays like a 3x3 window (9 pixels)
    unique_values, counts = np.unique(flat_neighborhood, return_counts=True)

    # Calculate probabilities of each unique pixel value
    probabilities = counts / float(len(flat_neighborhood))

    # Calculate Shannon entropy: H = -sum(p * log2(p))
    # We only sum for probabilities > 0, which np.unique inherently handles
    # as it only returns values that are present.
    entropy = -np.sum(probabilities * np.log2(probabilities))

    return entropy

def main():
    print("Starting Pixel Chaos Map generation...")

    # 1. Generate a synthetic input image
    input_image = generate_synthetic_image(width=256, height=256)
    cv2.imwrite("input_image.png", input_image)
    print("Generated input_image.png (synthetic test image)")

    # The synthetic image is already grayscale, so no conversion needed.
    grayscale_image = input_image

    # 2. Define the neighborhood size for entropy calculation
    neighborhood_size = 3 # e.g., 3x3 window
    pad_width = neighborhood_size // 2 # For 3x3, pad_width is 1

    # 3. Pad the grayscale image to handle border pixels
    # Using 'BORDER_REFLECT' ensures edge pixels have a valid neighborhood,
    # and the output entropy map will be the same size as the input.
    padded_image = cv2.copyMakeBorder(grayscale_image, pad_width, pad_width,
                                      pad_width, pad_width, cv2.BORDER_REFLECT)

    # 4. Initialize the entropy map
    # It will store float values before normalization to 0-255.
    entropy_map = np.zeros(grayscale_image.shape, dtype=np.float32)

    # 5. Iterate through each pixel of the original image
    # For each pixel, extract its 3x3 neighborhood from the padded image
    # and calculate its Shannon entropy.
    rows, cols = grayscale_image.shape
    for r in range(rows):
        for c in range(cols):
            # Extract the neighborhood (e.g., 3x3) from the padded image
            # The window's center in the padded image is (r + pad_width, c + pad_width)
            neighborhood = padded_image[r : r + neighborhood_size,
                                        c : c + neighborhood_size]

            # Calculate entropy for this neighborhood
            entropy_value = calculate_shannon_entropy(neighborhood)

            # Store the entropy value in the map at the corresponding pixel location
            entropy_map[r, c] = entropy_value

    # 6. Normalize the entropy map to 0-255 for display as an 8-bit grayscale image
    # Higher entropy values indicate more variation/randomness (brighter pixels).
    # Handle cases where the entropy_map might be entirely flat (max entropy is 0).
    max_entropy_value = np.max(entropy_map)
    if max_entropy_value > 0:
        normalized_entropy_map = (entropy_map / max_entropy_value) * 255
    else:
        # If all entropy values are zero, make the output map all black.
        normalized_entropy_map = np.zeros_like(entropy_map)

    # Convert the normalized map to an 8-bit unsigned integer type
    normalized_entropy_map_uint8 = normalized_entropy_map.astype(np.uint8)

    # 7. Save the resulting entropy map to a file
    cv2.imwrite("entropy_map.png", normalized_entropy_map_uint8)
    print("Generated entropy_map.png (grayscale visualization of local entropy)")

    print("Pixel Chaos Map generation complete. Check 'input_image.png' and 'entropy_map.png'.")

if __name__ == "__main__":
    main()