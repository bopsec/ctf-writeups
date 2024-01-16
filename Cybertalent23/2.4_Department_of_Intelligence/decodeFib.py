import string


def base(c):
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
    return alphabet.index(c)

# Function to convert BITS64 character to binary
def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)

input = "FEBuTk4E9JRf68Hq9Tg9Zl8JRU7nOnoPUb38JwCsPrkh5Ti6mu5TnpWq9D1iZxsfYgJK0fGmVCm9TiCshBz+pzB2Kpb+0NJalkoPMQMLDMw+koQPMdDD8TiwsY2EloPdelwADMM7nuhBStMwVyHMbgF6OHYfSUnTE1OMU7nENMMwuJRrkPUbiwsrkEloPBWi6mO35h5zKha7co7mQ/JRUb3wA7MDcY+05EhZXJUboHmPUbg15uJwwsrkPBGmN0delsSwsfGmO3ZMb3wADsPJqbGGqN0Ubg15PdubSUghZXJJCz+haHmQvSWJJiBOMfYgUbn7mAbYWJMwPJK0dmap2uJRBWg9JRMwALwWJhORdTi+0ZGImdYSU305hhB+pboWqtbGmupboWM7HMboTU3E6VCmlap2PJKRUb3MMhmaTEmN0fS0KhaZgUbiS0wEaq9TnHGMbi6ciCsQjZp2PdzKJ0Y2ArzMwhBzyA/gZxsY2VCmtb6co7mh5Ti6cgtSYgdmBOMhuzB2nOHaqlBGYhORJK0Y2u5D125hJwSUnXJhO0Dzw8JwoWqNRMwOPMJKRYWq9zKhB2ZGImNwwsJqzY2O/JRU7wEYrEqdlwA7c30NB2nO35AblEYJqboWqFzmIM7HqlBGYdD1GYdeYYgJiB25PB2wkoOvSYgY2OPMrEM7w8ZYCMGImtzdO0dmBG6uJRfSUg1NrkQH6VCmNwCshpzh+TnDsQ3NYWqN0Y2VSiGGGYi+0NhOw6MmlaHmAjaxsrkVSi+wADsADz2NY2QTtJaYWJdTn/koQzATUo7coHmVSghZxsdma/kIMbiYgYWG4KJ0JCziZDMGYg9pzYWMLmFzuSGmQHaqNw68KZl8pb6mhpbCsADzG6OnoOvSCMq9DmtzY2OTtdDDM0dubWJJqbS0nElIMLDkBOMhmaDd3wAD9wMMdznENMhmaHmO3NDToxsheYSE1GYfo2QvSCNDMRBWnTUiwshORdeY+0NDzKpbCsuJ0JKRrEM7w0ZGY38ZlEaGYgloALwoWqN0dzwQtDD1+JRUbo7mhhBOMBW30NDTnXJMwADz+pzJKRJqbWJBWoxsY2hBzuSCdgF6PUb3kIGY3EYdDDszdeYCNDEzGaM7nALw6MmdYo2hBzG6QvSWJdDmNwwsfWJDT30NU7w0NUbnpWM7wkouhB2NfSU30NY2OTtUb3E6O3NMQMLDszdORf6M12NJiBiZ78Kha7mVS3wAxsMwVSg9haxsrkVywEaGYnpWML1mouhaHmQzA/wATE1G6ADzOMhGz25ExATUiCshJRfGmhJRDT3sSCMqN0DT3gZDsArbGGM7nExADdgF6QzA7GqdlkIGI1yAxshelsS+05AbYYgDTg1NDDDcYSUiSUn7cgtSCsPdTnDdiGGGYi6mQjZ7MmtbWJDDDEzStfYgY2hZlMMJiBStYWGI1uSYgJqzdOwWJfSUiCdoD9KBziZxsrEqlByATUoT0wQtJ6TiwsY2hZYwsDT3kIGYoDd3gZTU3koVyw8pzrkVSoDNDEzmohpboWMboXJJiBmoOH6PdDDkBG6Q3NMQGYiCN1iZDsAjaDN1G6h5DmNw6mQnoERtrkQ3NY2uhBStdDDsb68w8JRduzhO0JiBG6uJRBWi6ciWJYWGImlaXJfS0wgZ7mQ3ZMb305ENMrEG4KpzdmaTEDEz+haT0w0Nhubo2uhBStdzwMMhO0DzwMMhOw+EYJiBuSCNmN0rkVSg1NrkAblQtdmaDNmtzfWJULDszJKRdD12NrkhZl0NrkupzdeYwsY2PJiaDMqN0JalEYdma7muBzGaGImtbYghubGmPdORrkhpzdeYGmAblQtdTgFYBWiYgDTo7MD8D1GYdTn7c3sS6mVSiwsDTnZgJaYSUgFaMbg9B"
bin = ""

for c in input:
    l = base(c)
    b = '{0:06b}'.format(l)[::-1]
    bin += b
#print(len(bin))

class Decoder:
    def __init__(self, stream):
        self.stream = stream

    def decode_fibonacci_number(self):
        acc = ""
        while len(self.stream) > 0:
            acc += self.stream[0]
            self.stream = self.stream[1:]
            if len(acc) > 2 and acc[-1] == "1" and acc[-2] == "1":
                acc = acc[:-1]  # Remove the trailing '11'
                sum = 0
                for i in range(len(acc)):
                    if acc[i] == '1':
                        sum += fib(i+2)
                return sum

    def decode_bitty_text(self):
        text = ""
        while len(self.stream) > 1:  # Ensure there are enough bits to process
            # Decode the length of the next segment
            segment_length = self.decode_fibonacci_number()
            print(segment_length)
            if segment_length is None or len(self.stream) < segment_length:
                break  # Not enough bits left for the next segment
            # Decode the segment into text
            char_bits = self.stream[:(segment_length)]
            self.stream = self.stream[(segment_length):]
            try:
                char = int(char_bits,2)
                char = str(char)
                text += char
            except OverflowError:
                print("test")
            #print(text)
        return (text + "---------")

    def decode(self):
        # Decode the overall length of the message (unused in this context)
        self.decode_fibonacci_number()
        # Decode the type of the message (unused in this context)
        self.decode_fibonacci_number()
        # Decode the text using the BITTY format
        decoded_text = self.decode_bitty_text()
        return decoded_text

decoder = Decoder(bin)
decoded_text = decoder.decode()
#print(decoded_text)
# Write the decoded text to a binary file
with open('decoded_text.bin', 'wb') as file:
    file.write(decoded_text.encode())
