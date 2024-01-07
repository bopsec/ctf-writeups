from scapy.all import rdpcap, IP, Raw

def extract_and_convert(packet):
    """Extracts and converts binary strings to text."""
    try:
        return chr(int(packet[1:], 2))
    except ValueError:
        return None

def is_reserved_bit_set(packet):
    """Check if the reserved bit is set in the IP header."""
    return (packet[IP].flags & 0x4) != 0  # Reserved bit is the second bit from the left

def main():
    # Load the pcap file
    packets = rdpcap('fangede_pakker.pcap')

    # Dictionary to store texts for each destination address where the reserved bit is set
    texts_by_address = {}

    # Iterate through packets
    for packet_num, packet in enumerate(packets):
        if IP in packet and Raw in packet and is_reserved_bit_set(packet):
            # Extract destination address
            dst_address = packet[IP].dst

            # Initialize a string for this address if not already present
            texts_by_address.setdefault(dst_address, "")

            # Extract the raw payload as a byte array and convert to string
            data_str = bytes(packet[Raw].load).decode(errors='ignore')

            # Process each character in the string
            for i in range(len(data_str) - 7):
                if data_str[i] == 'b' and all(c in '01' for c in data_str[i+1:i+8]):
                    char = extract_and_convert(data_str[i:i+8])
                    if char:
                        texts_by_address[dst_address] += char

    # Write the results to a file
    with open('output_reserved_bit.txt', 'w') as file:
        for dst_address, text in texts_by_address.items():
            header = f"Destination Address: {dst_address}\n"
            file.write(header + text + '\n')
            file.write("-" * 40 + '\n')

# Run the script
main()
