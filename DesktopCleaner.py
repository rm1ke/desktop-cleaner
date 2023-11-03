import os
import shutil
from datetime import datetime
import configparser
import logging
import socket
import platform

# logging
today_date = datetime.today().strftime('%Y-%m-%d')

log_filename = f'Log-{today_date}.txt'


logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# gather system info for logging
workstation_name = socket.gethostname()
system_info = platform.platform()
processor_info = platform.processor()
python_version = platform.python_version()
os_version = platform.platform()
home_dir = os.path.expanduser('~')
desktop_pathL = os.path.join(home_dir, 'Desktop')
start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)



# log the header information
logging.info(f'Log Start: {start_time}')
script_name = "Desktop Cleaner"
script_version = '1.0.1'
logging.info(f'Script Name: {script_name}')
logging.info(f'Script Version: {script_version}')
logging.info(f'Workstation: {workstation_name}')
logging.info(f'System Info: {system_info}')
logging.info(f'Processor Info: {processor_info}')
logging.info(f'Python Version: {python_version}')
logging.info(f'OS Version: {os_version}')
logging.info(f'Desktop Path: {desktop_pathL}')
logging.getLogger().addHandler(console_handler)
logging.info('-' * 50)  # log a separator line

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
    try:
        logging.info('Script started.')
        config_path = check_or_create_config()
        if config_path is None:
            raise ValueError("Could not read or create a valid 'extensions.config' file.")
        
        # Read configuration
        config = configparser.ConfigParser()
        config.read(config_path)
        extensions_to_organize = config.get('Settings', 'extensions').split(',')
    
        # Path to your desktop
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        if not os.path.exists(desktop_path):
            raise FileNotFoundError(f"Desktop path not found: {desktop_path}")
        
        # Provide feedback about the number of items on the desktop
        print(f"Organizing {len(os.listdir(desktop_path))} items on the desktop...")
        logging.info(f"Organizing {len(os.listdir(desktop_path))} items on the desktop...")
    
        # Get today's date to create a subfolder for archiving
        today_date = datetime.today().strftime('%Y-%m-%d')
    
        for item in os.listdir(desktop_path):
            item_path = os.path.join(desktop_path, item)
            print(f"Processing item: {item_path}")  # Debugging print statement
           # logging.info(f"Processing item: {item_path}")
    
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
                logging.info(f"Skipping file with unrecognized extension: {item_path}")
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
            logging.info(f"***** Moving {item_path} to {destination_path} *****")
            shutil.move(item_path, destination_path)
    
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        print(f"An error occurred: {e}")


# Call the function to organize the desktop
organize_desktop()
logging.info('Script finished.')
logging.info('-' * 50)  # log a separator line
logging.info('-' * 50)  # log another separator line for end incase its run again on same day to easily seperate 