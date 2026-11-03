# Pixel Chaos Map

Generates a grayscale image showing local pixel intensity entropy.

This project calculates the Shannon entropy of grayscale pixel intensities within a small (e.g., 3x3) neighborhood around each pixel across an entire static image. The result is displayed as a new grayscale "entropy map," where brighter pixels indicate higher local entropy (more pixel intensity variation/randomness) and darker pixels indicate lower local entropy (more uniform pixel intensities).

## How to Run

1.  **Save the files:**
    Ensure `main.py`, `requirements.txt`, and `README.md` are in the same directory.

2.  **Install dependencies:**
    Ensure you have `pip` installed. Open your terminal or command prompt in the project directory and run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the script:**
    ```bash
    python main.py
    ```

The script will:
*   Generate a synthetic grayscale test image (`input_image.png`) with regions of low and high entropy.
*   Process this image to calculate the local entropy for each 3x3 pixel neighborhood.
*   Save the resulting entropy map as `entropy_map.png`.

This script is designed to run non-interactively without displaying any graphical windows, making it suitable for headless server environments or automated processing.