#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re

url = "https://vae-login.ctf.cybertalent.no"
session = requests.Session()

def decode_vectors(vectors):
    response = session.post(f"{url}/decode_predict", json={"z": vectors})
    return response.text

def parse_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    for box in soup.find_all('div', class_='result-box'):
        pred_p = box.find('p', string=re.compile(r'Predicted Digit:'))
        predicted = None
        if pred_p:
            pred_match = re.search(r'Predicted Digit:\s*(\w+)', pred_p.text)
            predicted = pred_match.group(1) if pred_match else None
        scores = {}
        for item in box.find_all('div', class_='digit-item'):
            text = item.get_text().strip()
            match = re.match(r'(\d+|unknown):\s*([-\d.]+)', text)
            if match:
                scores[match.group(1)] = float(match.group(2))
        if scores:
            results.append({'predicted': predicted, 'scores': scores})
    return results

best_vectors = {}
best_scores = {str(i): float('-inf') for i in range(10)}

print("searching for vectors...")
print("="*60)

for dim1 in range(20):
    for dim2 in range(dim1+1, 20):
        for val1 in [-3, -2, 2, 3]:
            for val2 in [-3, -2, 2, 3]:
                vector = [0.0] * 20
                vector[dim1] = val1
                vector[dim2] = val2
                
                html = decode_vectors([vector])
                results = parse_results(html)
                
                if results:
                    predicted = results[0]['predicted']
                    scores = results[0]['scores']
                    
                    if predicted and predicted.isdigit():
                        digit = predicted
                        score = scores.get(digit, 0)
                        if score > best_scores[digit]:
                            best_scores[digit] = score
                            best_vectors[digit] = vector.copy()
                            print(f"New best for {digit}: dim{dim1}={val1}, dim{dim2}={val2}, score={score:.2f}")

print("\n" + "="*60)
print("best vectors:")
print("="*60)
print("\nbest_vectors = {")
for digit in sorted(best_vectors.keys()):
    vec = best_vectors[digit]
    non_zero = [(i, v) for i, v in enumerate(vec) if v != 0]
    print(f"    '{digit}': {vec},  # score={best_scores[digit]:.2f}, dims={non_zero}")
print("}")