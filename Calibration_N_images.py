import os
from astropy.io import fits
from concurrent.futures import ThreadPoolExecutor
from numba import vectorize, float32, float64

fits_directory = '/home/roger/220731'
# Paths to FITS files
fits_paths = [f for f in os.listdir(fits_directory) if f.endswith('.fts')]
if not fits_paths:
    raise ValueError("No FITS files found in fits_directory")
  
# How many images
N = 10
fits_paths_N = fits_paths[:N]

@vectorize([float32(float32, float32, float32, float64)], nopython = True)					 
def corr(image_data, dark_data, flat_data, exposure_time):

    # Apply dark correction
    corrected_image_data = image_data - dark_data * exposure_time
    # Apply flat correction
    corrected_image_data = corrected_image_data / flat_data

    return corrected_image_data

def corr_image(fits_path):
    """
    Corrects a FITS image for dark and flat field effects and saves the corrected image.
    fits_path (str): Path to the input FITS file.
    """
    fits_file_path = os.path.join(fits_directory, fits_path)
    output_file_path = os.path.join(output_directory, fits_path)
    try:
        # Load FITS image
        with fits.open(fits_file_path) as image:
            # Extract data arrays
            image_data = image[0].data
            # Create a new FITS header and HDU
            header = image[0].header
          
        # Apply flat correction
        corrected_image_data = corr(image_data, dark_data, flat_data, header['EXPTIME'])
        # Save the corrected image
        hdu = fits.PrimaryHDU(corrected_image_data, header)
        hdu.writeto(output_file_path, overwrite=True)
    except Exception as e:
        print(f"Error processing {fits_path}: {e}")

if __name__ == '__main__':

    dark_frame_path = ''
    flat_frame_path = ''
    output_directory = ''

    # Load dark and flat frames
    with fits.open(dark_frame_path) as dark_hdulist:
        dark_data = dark_hdulist[0].data

    with fits.open(flat_frame_path) as flat_hdulist:
        flat_data = flat_hdulist[0].data

    WORKERS = 8
    with ThreadPoolExecutor(max_workers = WORKERS) as executor:
        executor.map(corr_image, fits_paths_N)

print('All FITS Corrected')
