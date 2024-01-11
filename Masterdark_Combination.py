import os
import numpy as np
from astropy.io import fits

FITS_EXTENSION = '.fts'

def create_master_dark(dark_directory, output_file):
    """
    Create a master dark frame from a directory of dark frames.
    Parameters:
        dark_directory (str): Path to the directory containing dark frames.
        output_file (str): Path to the output master dark FITS file.
    """
    dark_paths = [f for f in os.listdir(dark_directory) if f.endswith(FITS_EXTENSION)]
    if not dark_paths:
        raise FileNotFoundError(f"No FITS files found in {dark_directory}")

    dark_frames = [fits.getdata(os.path.join(dark_directory, dark_frame_path)) for dark_frame_path in dark_paths]

    # Calculate median of dark frames and convert to 32 bits
    masterdark = np.median(dark_frames, axis=0).astype(np.float32)
    # Create header for the master dark
    header = fits.getheader(os.path.join(dark_directory, dark_paths[0]))
    header['COMMENT'] = 'Master Dark Frame'
    header['NFRAMES'] = (len(dark_frames), 'Number of dark frames combined')

    master_dark_hdu = fits.PrimaryHDU(data=masterdark, header=header)
    with fits.HDUList([master_dark_hdu]) as master_dark_hdulist:
        master_dark_hdulist.writeto(output_file, overwrite=True)
    
if __name__ == "__main__":

    dark_directory = ''
    output_file = ''
    create_master_dark(dark_directory, output_file)
