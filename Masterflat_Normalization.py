import numpy as np
from astropy.io import fits

def normalize(input_filename, output_filename, window_size=32):
    # Open the original FITS file
    with fits.open(input_filename) as hdul:
        # Get the data from the primary HDU
        data = hdul[0].data

    height, width = data.shape
    
    # Set negative values to 0
    data[data < 0] = 0
    data_float32 = data.astype(np.float32)
    zero_pixels = np.where(data_float32 == 0)
    new_data = np.copy(data_float32)

    for y, x in zip(zero_pixels[0], zero_pixels[1]):
        # Calculate the starting and ending indices of the window
        y_start = max(0, y - window_size//2)
        y_end = min(height, y + window_size//2)
        x_start = max(0, x - window_size//2)
        x_end = min(width, x + window_size//2)
        # Extract the window around the zero pixel
        window = data_float32[y_start:y_end, x_start:x_end]
        # Calculate the average of non-zero values in the window
        non_zero_values = window[window != 0]
        if non_zero_values.size > 0:
            average_value = np.mean(non_zero_values)
            new_data[y, x] = average_value

    try:
        # Find the max value of pixel values
        max_pixel_value = np.max(new_data)
        # Normalize the image 
        normalized_data = new_data / max_pixel_value
        # Save the normalized image to a new FITS file
        normalized_fits_file = fits.PrimaryHDU(normalized_data)
        normalized_fits_file.writeto(output_filename, overwrite=True)
        print("FITS file normalized and saved as:", output_filename)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':

    input_filename = ''
    output_filename = ''
  
    normalize(input_filename, output_filename)
    
