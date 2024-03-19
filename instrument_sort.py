import os
import shutil

# Determine the script's directory
script_dir = os.path.dirname(os.path.realpath(__file__))

def safe_make_directory(path):
    """Safely create a directory if it doesn't already exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def get_instrument_and_quality(filename):
    """Extract the instrument and quality from the filename."""
    parts = filename.split('_')
    if len(parts) >= 2:
        return parts[0], parts[1]
    else:
        return None, None

def copy_files(source_dir, target_dir, log_file_path):
    """Copy files into organized directory structure with progress."""
    files = os.listdir(source_dir)
    total_files = len(files)

    # Load log to find out where we left off
    processed_files = set()
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            processed_files = set(line.strip() for line in log_file)
    
    # Initialize counters
    processed_count = len(processed_files)
    for filename in files:
        # Skip if already processed
        if filename in processed_files:
            continue

        instrument, quality = get_instrument_and_quality(filename)
        if instrument and quality:
            instrument_dir = os.path.join(target_dir, instrument)
            quality_dir = os.path.join(instrument_dir, quality)
            safe_make_directory(quality_dir)
            
            # Copy file to the new location
            shutil.copy2(os.path.join(source_dir, filename), quality_dir)
            
            # Log this file as processed
            with open(log_file_path, 'a') as log_file:
                log_file.write(filename + '\n')

            processed_count += 1

        # Print progress
        print(f"Processed {processed_count}/{total_files} files.", end='\r', flush=True)


if __name__ == "__main__":
    source_directory = 'data_in'  # Change this to your source directory
    target_directory = 'data_out'  # Change this to your target directory
    log_file = 'log.txt'  # Path to log file

    safe_make_directory(target_directory)  # Ensure target directory exists
    copy_files(source_directory, target_directory, log_file)
