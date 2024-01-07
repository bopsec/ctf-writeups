otp = [23, 2, 0, 5, 13, 16, 22, 7, 9, 4, 19, 21, 18, 10, 20, 11, 12, 14, 6, 1, 3, 8, 17, 15]

def reverse_explode(input, antall):
    storrelse = len(input) // antall
    fragmenter = []
    for i in range(0, len(input), storrelse):
        fragmenter.append(input[i:i + storrelse])
    return fragmenter

def reverse_transform(pinneved):
    fragments = reverse_explode(pinneved, 24)
    reordered_fragments = [None] * len(fragments)
    for index, fragment in enumerate(fragments):
        reordered_fragments[otp[index]] = ''.join([chr(ord(c) - 2) for c in fragment])
    return ''.join(reordered_fragments)

if __name__ == "__main__":
    with open("pinneved.txt", "r") as file:
        pinneved_content = file.read()

    slede_content = reverse_transform(pinneved_content)

    with open("slede_reversed.txt", "w") as file:
        file.write(slede_content)
