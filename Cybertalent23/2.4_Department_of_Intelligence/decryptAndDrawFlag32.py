import base64
import string
import numpy as np
import matplotlib.pyplot as plt

# Function to decrypt the image data
def decrypt(bitstream, initial_key, size=32, g=3):
    k = size - 1
    mask = (1 << size) - 1
    key = initial_key
    decrypted = []
    for b in bitstream:
        decrypted_bit = (key >> k) ^ b
        decrypted.append(decrypted_bit)
        key = (g * key) & mask
    return decrypted

# Function to convert base64 to binary
def base(c):
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
    return alphabet.index(c)

# Function to compute Fibonacci numbers
def fib(n):
    if n == 0: return 0
    if n == 1: return 1
    return fib(n-1) + fib(n-2)

# Convert base64 encoded input to binary
input_sequence = "EiCjJCOdwH4p78jCGGcxGY/45vAAz9eW//IgbI3M8O+4//P/0Xg//A/Gz5/fEem7Y7HOVQAI9H8KgF424/8HLSgPd//Agf47T3+og5jzBg9JuSw7AYA0/Mol4/+5A/EIou/AQxAmJGs77AwF04/e9R82P+OChK/ujzTn7DeYAgb2133G4B8Y9bEXOAwR/kYjBcG6A/f6+m+tAcehgfuH2HC9/vgeiMmiTOoDJzn/RaEef9bgzf3NiHAzQ/tTyy/rDmw43TO/nMzcb8Yv+wbw/i+jh4u2DOFLQEJq8lbCkJAP+lD3joLNz78BGCJ/CwZgJATbP838nI+4GGbwN2qCOfCI+YBzPOWCdJE67TI5fjsOKzZdPbS+xzI7KcdGEO9UY//EWc/5a+BM2dq2DMsfHgBKjPXH/Lglns89waYp84xvWfHc+Fl1cnesqCCfCksRjinU4mibMwd1e+3z+bA1AaYhQIi2L0y/17IeS/3XGDInw8wfMwZ/1xo9wS2dw8H2bMw2H4wAy/Nu1xfb46eCghDOVvMszDg8SJvxM7JNAGH91L4/4q0LOv3FYx/mYGRVyA9GAwWEOpmla+cB8G6l78L+z3YDI9/P+BAY/SJYOgKXfvwgn6wfaxYYg74IirusftMneGYQz/+d/h/9bRYghXueEAk3ABAUU/IPPP+PX8zYtybRMHM6AuDxkAyOGjdGj3plZ4KEfPO+/ghGsiai/RDm5Z0RPYhwSgP7bD/HtAECzokP+Yb69eGunn4D3b0vj2VOovBBcJGwHg7d+yzTYX+TJ1Q8Qb9vnAjVtnpheHckjHoslFuj8YRwxvuHu8P7ht8Bpoh8hjnUOB53RTGqvNIA3Ilh/XXDs8p/gBAPuSAlH/hRf+6mxLxfTx/OgCBFgLiTwB87jJXRr6b/dPqCxQPt8Gn+9eV0MTTQHjBcICovRZgCgMA7M9/ZiY9DhkJj8+6TcGgX79/3HRgDEAAkLw/Oouv7BQOc8o/7fUACEfA8H4PwfLBqxfDcc/BY6eF3Bq/j6/PAymT3JPOdf+ZU+/jSbgPQbA+/HgzACC88BAALMM/z/h8zdDzeXkr9DeAbEIK4TGO+8FQ4v5T+j/vZ/ZmDAOmBEbAwfm/wMhvhFDmX12HCBfZMy0RgueOPeHk5/DP3d4nL8PBwFOw5rg/Z2/P4P8dpBc+9fvfnHynkQfExjAg4k0+N/w//ggAWg0/FPgNeklH+znU2DChuyNHuZH43/HF8w38JNHJeeuOh0rXYDQ4//5fAOi7jDeY/MG"  # Your base64 encoded input here
bin_sequence = ""
for c in input_sequence:
    l = base(c)
    b = '{0:06b}'.format(l)[::-1]
    bin_sequence += b

# Decoder class to extract length, type, width, and height
class Decoder:
    def __init__(self, stream):
        self.stream = stream
    def decode(self):
        acc = ""
        while len(self.stream) > 0:
            acc += self.stream[0]
            self.stream = self.stream[1:]
            if len(acc) > 2 and acc[-1] == "1" and acc[-2] == "1":
                acc = acc[:-1]
                sum = 0
                for i in range(len(acc)):
                    if acc[i] == '1':
                        sum += fib(i+2)
                acc = ""
                return sum

# Decode length, type, width, and height
dec = Decoder(bin_sequence)
length = dec.decode()
print(length)
typ = dec.decode()
print(typ)
w = dec.decode()
print(w)
h = dec.decode()
print(h)

# Decrypting the image data
encrypted_img_data = [int(bit) for bit in dec.stream]
key = 2920247797
decrypted_img_data = decrypt(encrypted_img_data, key)
# Convert decrypted data into an image
print(decrypted_img_data)
data = np.zeros((h, w))
c = 0
for i in range(h):
    for j in range(w):
        data[i, j] = 255 if decrypted_img_data[c] == 1 else 0
        c += 1

# Display the image
plt.imshow(data, cmap='gray')
plt.axis('off')
plt.show()
