def unique_characters_in_order(text):
    unique_chars = []
    for char in text:
        if char not in unique_chars:
            unique_chars.append(char)
    return ''.join(unique_chars)

def decode_using_unique_characters(numbers, unique_chars):
    decoded_text = ''
    for index in numbers.split(', '):
        decoded_text += unique_chars[int(index)]
    return decoded_text

poem = (
    "{}+"
    "tells det å telle, gjør det det?+"
    "nummer en, nummer to, nummer tre,+"
    "en rekkefølge man må se.++"
    "oversikt og sekvens, en viktig oppgave i alle fall,+"
    "hva ellers er vel vitsen med tall?"
)
# I replated \n with "+" because python would interpret \n as two seperate characters.

numbers = '26, 6, 3, 0, 16, 4, 8, 4, 7, 21, 19, 14, 7, 3, 4, 5, 5, 25, 16, 11, 1'

unique_characters = unique_characters_in_order(poem)

# Decoding the message
decoded_message = decode_using_unique_characters(numbers, unique_characters)
print(decoded_message)
