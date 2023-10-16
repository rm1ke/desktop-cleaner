import os
import shutil
from datetime import datetime

def organize_desktop():
    # Path to desktop
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

    # List of file extensions to organize..I would later like to add a way to have a
    # config file that the exe looks for and you can config your own file extension types
    extensions_to_organize = [
        '.pdf', '.txt', '.rpt', '.rdl',
        '.xls', '.xlsx', '.doc', '.docx'
    ]

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
