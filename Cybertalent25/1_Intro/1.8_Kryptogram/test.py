cipher = "øwbxl hjcbx læxmx fpxfx lmrcb xlpxo rvøpl rlvrc hrjlø cjxøp brdrb xbræs xlxbb xfhxl yxocx lwfxy øvwjf dryxf xjhhy føvæf apxcp jyxjf yxbøb bxfoj jmwfx mjdxf"

mapping = {
    'ø': 'a',
    'w': 'f',
    'b': 't',
    'x': 'e',
    'l': 'n',
    'h': 'p',
    'j': 'o',
    'c': 's',
    'æ': 'b',
    'm': 'm',
    'f': 'r',
    'p': 'k',
    'r': 'i',
    'v': 'g',
    'd': 'v',
    'y': 'd',
    's': 'y',
    'o': 'l',
    'a': 'u',
}

out = []
for ch in cipher:
    if ch.lower() in mapping:
        out.append(mapping[ch.lower()])
    else:
        out.append(ch)  # mellomrom osv

print("".join(out))
