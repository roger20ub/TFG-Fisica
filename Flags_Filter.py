import os
import re
from concurrent.futures import ThreadPoolExecutor

def filter_and_update_rows(input_file):

    output_file = f'filtered_{input_file}'

    input_file = os.path.join(corr_cat_directory, input_file)
    output_file = os.path.join(output_directory, output_file)

    row_count = 0  # Initialize row count

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:

        for line in infile:
            # Check if the line does not start with a number
            if not re.match(r'^\s*\d', line):
                outfile.write(line)

            else:
                # Extract the last column value
                last_column = int(line.split()[-1])
                # Check if the last column value is less than 8
                if last_column < 8:

                    # Increment row count
                    row_count += 1
                    # Replace the first number in the row with the row count
                    updated_line = re.sub(r'^(\s*\d+)', r'{:10d}'.format(row_count), line)
                    outfile.write(updated_line)

if __name__ == '__main__':

    corr_cat_directory = '/home/roger/few_stars/concurrent_split_sex_one_image'
    output_directory = '/home/roger/few_stars/filtered_quadrants_image'

    WORKERS = 8

    # Paths to CAT files
    cats_paths = [f for f in os.listdir(corr_cat_directory) if f.endswith('.cat')]
    if not cats_paths:
        raise ValueError("No FITS files found in fits_directory")

    with ThreadPoolExecutor(max_workers = WORKERS) as executor:
        executor.map(filter_and_update_rows, cats_paths)

    print('All files filtered')
