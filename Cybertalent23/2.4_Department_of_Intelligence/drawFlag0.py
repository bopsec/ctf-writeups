import base64
import string
import numpy
import matplotlib.pyplot as plt

def base(c):
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
    return alphabet.index(c)

input = "EiCjJCONAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM4D+gHgBYAHgD4B+4DeA+gP4DHgDcAOwBYAHAO4D+gHAgPgBgDHAAAADAAAw/9D+A3AH+j/4H+gPwH4B+gf+jfgf4H+xH4BfgH8hPwHAH+hf4DA4P+AwxHAAAgDAAA4/+B/wfgBjxYMHfwHcH8gDwAjxcwAMADcH8wYwDjxHcHADDwAOAAMGfAwMGAAAgBAAAYYMAecMwgxAMGDMADGDb4A+nxYM+n/5fGDbYMshxADGDu5f+nDgHGDMgbGDfwHwAAAAsNGAJGAYgPwDzBGgBjxNsD/jPMH/z/8PjxNAG3AYgBjh/8P/zO4H+AG4Pghf4HYAAAA+ADwMDAMwH4h/ADwgxYG+DGwH+DGgBYgxYGghZAGwgx4cYAG4PGGfADOHYAMADMAAAAfgx4n5DDMGwhbgBYwY+HnBDMGuBDwAMwY+HY4fgBYwYMMMADcG/zYgBDDG4H+BMAAAgNwY8z8BDGDwAOwAMYM/jxgBGD4gBYAGYM/DG8PYAMYMGGGgBGj/ZMwghhB+j/ADAAAwAYMD7YgBjZYgDYAGcHwwYwAjBOwAMADcHwgBADGAGcHnDDwAjxAMGYw5YAjxYgBAAA8D/3z7Pwg/8H+g/5f8B+wP+j/4D+j/4P8B+4P4j/4f8B/7P+D/wf+j/x/+j/5fwAAAA+h/755DYgP8BPw/8PcAfwD/hP8A/xf8HcAf8H8xf8PcA39H/BPwH+w/wd/h74OYAAAAAAAAAAAcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOAAAAAAAAAAAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)

bin = ""
for c in input:
    l = base(c)
    b = '{0:06b}'.format(l)[::-1]
    bin += b
print(len(bin))

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

dec = Decoder(bin)
length = dec.decode()
typ  = dec.decode()
w = dec.decode()
print("Width: ",w)
h = dec.decode()
print("Height: ",h)
data = numpy.zeros((h, w))

img = dec.stream
print(img)
c = 0
try:
    for i in range(h):
        for j in range(w):
            if img[c] == "1":
                data[i,j] = 255
            else:
                data[i,j] = 0
            c = c+1
except:
    pass

plt.imshow(data)
plt.show()
