import zipfile

def extract_from_corrupt_zip(zip_path, output_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_path)
        print(f"Files extracted to {output_path}")
    except zipfile.BadZipFile:
        print("Error: The ZIP file is corrupted and cannot be opened.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
zip_path = 'extracted_package.zip'  # Replace with your ZIP file path
output_path = 'path_to_extract_directory'  # Replace with your desired output directory

extract_from_corrupt_zip(zip_path, output_path)
