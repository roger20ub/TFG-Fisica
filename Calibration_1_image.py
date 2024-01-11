from astropy.io import fits
from numba import vectorize, float32, float64, uint16

@vectorize([float32(uint16, float32, float32, float64)])					 
def corr(image_data, dark_data, flat_data, exposure_time):
    # Apply dark correction
    corrected_image_data = image_data - dark_data * exposure_time
    # Apply flat correction
    corrected_image_data = corrected_image_data / flat_data
  
    return corrected_image_data

if __name__=="__main__":
    
    fits_frame_path = ''
    dark_frame_path = ''
    flat_frame_path = ''
    output_path = ''
    
    # Load FITS image
    with fits.open(fits_frame_path) as image_hdulist:
        image_data = image_hdulist[0].data
        header = image_hdulist[0].header

    # Load dark and flat frames
    with fits.open(dark_frame_path) as dark_hdulist, fits.open(flat_frame_path) as flat_hdulist:
        dark_data = dark_hdulist[0].data
        flat_data = flat_hdulist[0].data

    # Get the exposure time from the FITS header
    exposure_time = header['EXPTIME']  
    # Get calibrated data
    calibrated_image_data = corr(image_data, dark_data, flat_data, exposure_time)
    # Create a new FITS header and HDU
    hdu = fits.PrimaryHDU(calibrated_image_data, header)
    # Save the calibrated image
    hdu.writeto(output_path, overwrite=True)
    print("Corrected image saved as:", output_path)
