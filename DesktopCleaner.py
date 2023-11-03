import os
import shutil
from datetime import datetime
import configparser
import logging

# logging
today_date = datetime.today().strftime('%Y-%m-%d') 
script_dir = os.path.dirname(os.path.abspath(__file__))  #gets dir where script is located

log_dir = os.path.join(script_dir, today_date)
os.makedirs(log_dir, exist_ok=True)

log_path = os.path.join(log_dir, 'log.txt')

logging.basicConfig(filename='log.txt', level=logging.DEBUG)


def check_or_create_config():
    config_path = 'extensions.config'
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
        try:
            # Attempt to read the extensions option to check the file's format
            config.get('Settings', 'extensions')
        except configparser.NoSectionError:
            print("Error: Missing '[Settings]' section in 'extensions.config'.")
            return None  # Or handle this error in some other way
        except configparser.NoOptionError:
            print("Error: Missing 'extensions' option in '[Settings]' section of 'extensions.config'.")
            return None  # Or handle this error in some other way
    else:
        # Create a default config file if none exists
        config['Settings'] = {
            'extensions': '.pdf,.csv,.txt,.rpt,.rdl,.xls,.xlsx,.doc,.docx, .xml'
        }
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    return config_path

def organize_desktop():
    logging.info('Script started.')
    config_path = check_or_create_config()
    if config_path is None:
        print("Error: Could not read or create a valid 'extensions.config' file.")
        logging.error("Error: Could not read or create a valid 'extensions.config' file.")
        return  # Exit the function if the config file is missing or invalid
    
    # Read configuration
    config = configparser.ConfigParser()
    config.read(config_path)
    extensions_to_organize = config.get('Settings', 'extensions').split(',')

    # Path to your desktop
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

    # Provide feedback about the number of items to be organized
    print(f"Organizing {len(os.listdir(desktop_path))} items on the desktop...")
    logging.info(f"Organizing {len(os.listdir(desktop_path))} items on the desktop...")

    # Get today's date to create a subfolder for archiving
    today_date = datetime.today().strftime('%Y-%m-%d')

    for item in os.listdir(desktop_path):
        item_path = os.path.join(desktop_path, item)
        print(f"Processing item: {item_path}")  # Debugging print statement
        logging.info(f"Processing item: {item_path}")

        # Skip if item is a directory
        if os.path.isdir(item_path):
            print(f"Skipping directory: {item_path}")  # Debugging print statement
            logging.info(f"Skipping directory: {item_path}")
            continue

        # Get file extension
        file_extension = os.path.splitext(item)[1].lower()

        # Skip files whose extension is not in the list
        if file_extension not in extensions_to_organize:
            print(f"Skipping file with unrecognized extension: {item_path}")  # Debugging print statement
            logging.info(f"Skipping file with unrecognized extension: {item_path}")  # Debugging logging statement
            continue

        # Determine the destination directory
        extension_folder = os.path.join(desktop_path, file_extension.lstrip('.').upper())
        date_subfolder = os.path.join(extension_folder, today_date)
        
        # Create the destination directories if they don't exist
        if not os.path.exists(date_subfolder):
            os.makedirs(date_subfolder)

        # Move the file
        destination_path = os.path.join(date_subfolder, item)
        print(f"Moving {item_path} to {destination_path}")  # Debugging print statement
        logging.info(f"Moving {item_path} to {destination_path}")  # Debugging logging statement
        shutil.move(item_path, destination_path)


logging.info('Script finished.')

# Call the function to organize the desktop
organize_desktop()
