from astropy.io import fits

# Path to FITS file
fits_file = ''
try:
    # Open FITS file
    with fits.open(fits_file) as hdulist:
        # Get information about HDUs 
        hdulist.info()
        # Access specific HDU 
        hdu = hdulist[0]
        # Access data and header of specific HDU
        data = hdu.data
        header = hdu.header
      
    # Prints 'data' and 'header' 
    print("\nDATA \n", data)
    header_lines = [f"{key:8s}: {value}" for key, value in header.items()]
    print("\nHEADER\n" + "\n".join(header_lines))
except Exception as e:
    print(f"Error: {e}")
