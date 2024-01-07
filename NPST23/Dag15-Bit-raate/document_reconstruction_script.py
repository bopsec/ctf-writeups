
import os
import zipfile
from collections import Counter
import hashlib

def read_file(file_path):
    '''
    Reads the content of a file given its path.
    '''
    with open(file_path, 'rb') as file:
        return file.read()

def reconstruct_document_excluding_chars(backup_dir, backup_files, excluded_chars):
    '''
    Reconstructs a document from backup files, excluding specified characters.
    '''
    # Convert excluded characters to their byte equivalents
    excluded_bytes = [ord(char) for char in excluded_chars]

    # Initialize a list to store the byte-wise content of each file
    all_files_content = []

    # Read all backup files and store their content
    for file_name in backup_files:
        file_path = os.path.join(backup_dir, file_name)
        file_content = read_file(file_path)
        all_files_content.append(file_content)

    # Reconstruct the document byte-by-byte
    reconstructed_document = bytearray()

    # Iterate over each byte position
    for byte_index in range(len(all_files_content[0])):
        # Extract the same byte from each file
        bytes_at_index = [file_content[byte_index] for file_content in all_files_content]

        # Count the frequency of each byte, excluding the forbidden characters
        byte_frequency = Counter(bytes_at_index)
        for excluded_byte in excluded_bytes:
            if excluded_byte in byte_frequency:
                del byte_frequency[excluded_byte]

        # If all bytes are excluded, use the original most common byte (handle extreme cases)
        most_common_byte = byte_frequency.most_common(1)[0][0] if byte_frequency else Counter(bytes_at_index).most_common(1)[0][0]

        # Append the most common valid byte to the reconstructed document
        reconstructed_document.append(most_common_byte)

    return reconstructed_document

def main():
    # Define the directory containing the backup files and the list of files
    backup_dir = 'backups'  # Replace with the path to your backup directory
    backup_files = sorted(os.listdir(backup_dir))

    # Characters to exclude
    excluded_characters = "{}#$[]§¤@"

    # Reconstruct the document
    reconstructed_document = reconstruct_document_excluding_chars(backup_dir, backup_files, excluded_characters)

    # Calculate the MD5 checksum of the reconstructed document
    md5_checksum = hashlib.md5(reconstructed_document).hexdigest()

    # Print the formatted response
    print(f'PST{{{md5_checksum}}}')

    # Save the reconstructed document to a file
    reconstructed_file_path = 'reconstructed_document.bin'  # Change the file name and extension as needed
    with open(reconstructed_file_path, 'wb') as file:
        file.write(reconstructed_document)
    print(f'Reconstructed document saved to {reconstructed_file_path}')

if __name__ == "__main__":
    main()
