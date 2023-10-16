import os
import shutil
from datetime import datetime
import configparser

def check_or_create_config():
    config_path = 'extensions.config'
    if not os.path.exists(config_path):
        # Create a default config file if none exists
        config = configparser.ConfigParser()
        config['Settings'] = {
            'extensions': '.pdf,.txt,.rpt,.rdl,.xls,.xlsx,.doc,.docx'
        }
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    return config_path

def organize_desktop():
    config_path = check_or_create_config()
    # Read configuration
    config = configparser.ConfigParser()
    config.read(config_path)
    extensions_to_organize = config.get('Settings', 'extensions').split(',')

    # Path to your desktop
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

    # Get today's date to create a subfolder for archiving
    today_date = datetime.today().strftime('%Y-%m-%d')

    for item in os.listdir(desktop_path):
        item_path = os.path.join(desktop_path, item)

        # Skip if item is a directory
        if os.path.isdir(item_path):
            continue

        # Get file extension
        file_extension = os.path.splitext(item)[1].lower()

        # Skip files whose extension is not in the list
        if file_extension not in extensions_to_organize:
            continue

        # Determine the destination directory
        extension_folder = os.path.join(desktop_path, file_extension.lstrip('.').upper())
        date_subfolder = os.path.join(extension_folder, today_date)
        
        # Create the destination directories if they don't exist
        if not os.path.exists(date_subfolder):
            os.makedirs(date_subfolder)

        # Move the file
        shutil.move(item_path, os.path.join(date_subfolder, item))

# Call the function to organize the desktop
organize_desktop()
