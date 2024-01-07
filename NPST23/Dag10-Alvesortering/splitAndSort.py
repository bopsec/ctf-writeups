def split_and_sort_by_length(file_path, output_file_path):
    with open(file_path, 'rb') as file:
        content = file.read()

    # Splitting the file into segments based on null bytes
    segments = content.split(b'\x00')

    # Sorting the segments by length
    segments_sorted_by_length = sorted(segments, key=len)

    # Saving the sorted segments to a file
    with open(output_file_path, 'w') as output_file:
        for i, segment in enumerate(segments_sorted_by_length):
            # Writing each segment as a line in the file
            # Converting bytes to string for saving
            segment_str = segment.decode('utf-8', errors='ignore')
            output_file.write(f"Segment {i+1}: {segment_str}\n")

    return f"Sorted segments saved to {output_file_path}"

# Example usage
file_path = 'random_text.bin'  # Replace with your file path
output_file_path = 'output.txt'  # Replace with the path where you want to save the sorted segments
result = split_and_sort_by_length(file_path, output_file_path)

print(result)
