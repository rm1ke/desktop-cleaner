import os
import shutil

def organize_desktop():
    # Path to your desktop
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

    # List of file extensions to organize
    extensions_to_organize = [
        '.pdf', '.txt', '.rpt', '.rdl',
        '.xls', '.xlsx', '.doc', '.docx'
    ]

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
        destination_directory = os.path.join(desktop_path, file_extension.lstrip('.').upper())

        # Create the destination directory if it doesn't exist
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        # Move the file
        shutil.move(item_path, os.path.join(destination_directory, item))

# Call the function to organize the desktop
organize_desktop()
