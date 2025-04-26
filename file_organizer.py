import os 
import shutil

def organize_files(directory):
    """
    Organize files in the specified directory by their extensions.
    Includes logging, duplicate handling, and undo functionality 
    """
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist")
        return
    
    # Change to the target directory 
    os.chdir(directory)

    # List all files in the directory, skipping hidden files
    files = [f for f in os.listdir(directory) if os.path.isfile(f) and not f.startswith('.')]

    if not files:
        print("No files found to organize.")
        return
    
    # Dictionary for undo functionality 
    undo_map = {}

    # Create a log file to track movements
    with open ("orgenizer_log.txt", "w") as log_file:
        log_file.write("file organizer Log\n")
        log_file.write("=" * 30 + "\n\n")

    # Organize files by their extensions
    for file in files:
        # Get the file extension
        _, ext = os.path.splitext(file)
        ext = ext[1:].upper()

        if not ext:
            ext = "NO_EXTENSION"

        if not os.path.exists(ext):
            os.mkdir(ext)


        # Handle duplicate files
        destination = os.path.join(ext, file)
        if os.path.exists(destination):
            base , extension = os.path.splitext(file)
            new_name = f"{base}_copy{extension}"
            destination = os.path.join(ext, new_name)

        # Move the file into the corresponding folder
        shutil.move(file, destination)

        # Log the action 
        log_file.write(f"Moved {file} to {destination}\n")

        # Store undo information
        undo_map[file]  = os.path.join(directory, file)

    print(f"Files in {directory} have been organzied successfully.")
    print("Log file created: organizer_log.txt")
    return undo_map


def undo_organization(undo_map):
    """
    Undo the file organization by moving filess back to their original locations.
    """
    for file, original_path in undo_map.items():
        folder = os.path.dirname(original_path)
        if os.path.exists(file):
            shutil.move(file, folder)
            print(f"Moved {file} back to {folder}")
        else:
            print(f"File {file} not found in the organized directory")


if __name__ == "__main__":
    print("File Organizer\n" + "=" * 20)
    print("1. Organize Files")
    print("2. Undo Organization")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        target_directory = input (" Enter the path of the directory to organize: ").strip()
        undo_map = organize_files(target_directory)
        # Save undo_map for potential later use
        with open("undo_map.txt", "w") as undo_file:
            for file, path in undo_map.items():
                undo_file.write(f"{file}:{path}\n")

    elif choice == "2":
        # Load undo_map from file if it exists
        if os.path.exists("undo_map.txt"):
            undo_map = {} # This creates the directory 
            with open("undo_map.txt", "r" ) as undo_file: # This open the file undo_map.txt as read only
                for line in undo_file: # This will iterate through undo_file
                    file, path = line.strip().split(":")
                    undo_map[file] = path
            undo_organization(undo_map)
        else:
            print("No undo information found.")
    else:
        print("Invalid choice . Exiting.")