from pathlib import Path  # Import Path for object-oriented filesystem paths

# Get the current working directory (where the script is run from)
current_dir = Path.cwd()

# Get the name of the current Python file
# __file__ is the path to this script; .name extracts just the filename
current_file = Path(__file__).name

# Print the directory being scanned
print(f"Files in {current_dir}:")

# Iterate over all files and folders in the current directory
for filepath in current_dir.iterdir():

    # Skip the current script file to avoid reading itself
    if filepath.name == current_file:
        continue

    # Print the name of the file or directory
    print(f"  - {filepath.name}")

    # Check if the path is a file (not a directory)
    if filepath.is_file():
        # Read the entire contents of the file as text using UTF-8 encoding
        content = filepath.read_text(encoding='utf-8')

        # Print the file's contents
        print(f"    Content: {content}")
