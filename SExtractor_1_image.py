import subprocess
from astropy.io import fits
from concurrent.futures import ThreadPoolExecutor

split_fits_directory = ''
sex_output_directory = ''

config_path = ''
param_path = ''
filter_path = ''

# Number of subimages n^2, eg n=2 --> 4 subimages, n=3 --> 9 subimages
n = 2
# Number of threads
WORKERS = 8

def run_sextractor(args):
    i, j, quadrant = args

    quadrant_filename = f'{split_fits_directory}/quadrant_{i}_{j}.fts'
    fits.PrimaryHDU(quadrant).writeto(quadrant_filename, overwrite=True)

    # Command to run SExtractor
    sextractor_command = [
        'sex',
        quadrant_filename,
        '-CATALOG_NAME',
        quadrant_filename.replace('.fts', '.cat'),
        '-c',
        config_path,
        '-PARAMETERS_NAME',
        param_path,
        '-FILTER_NAME',
        filter_path
    ]
    
    try:
        subprocess.run(sextractor_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error running SExtractor for {quadrant_filename}: {e}')

if __name__ == '__main__':

    file_path = ''

    with fits.open(file_path) as hdul:
        # Access the image data
        image_data = hdul[0].data

    # Divide the image into rows and columns of equal-sized quadrants
    quarter_height = image_data.shape[0] // n
    quarter_width = image_data.shape[1] // n

    quadrants = [(i, j, image_data[i * quarter_height:(i + 1) * quarter_height, j * quarter_width:(j + 1) * quarter_width]) 
                for i in range(n) for j in range(n)]

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        executor.map(run_sextractor, quadrants)

    print('All FITS SExtracted')
