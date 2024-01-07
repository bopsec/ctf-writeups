def reconstruct_text_from_indices(file_path, indices):
    with open(file_path, 'r') as file:
        content = file.read()
    reconstructed_text = ''.join([content[index] for index in indices])
    return reconstructed_text

file_path = 'Partisjoner/861e2a75-7b5f-4d89-aba1-bcb6a2c2f71c/nissetekst'
file_path_2 = 'nissetekst_2'
indices = [6793, 539, 4387, 0, 5815, 8316, 7006, 8628, 2750, 9710, 7513, 1344, 4841, 2172, 1949, 6157, 4629, 931, 2765, 6744, 8609, 2853, 3580, 7327, 450, 4323, 9871]
indices_2 = [1817, 1004, 2238, 1709, 18, 714, 2499, 3069, 2148, 854, 1480, 831, 2441, 373, 276, 374, 844, 2725, 736, 2204, 1107, 1478]
reconstructed_text = reconstruct_text_from_indices(file_path, indices)
print(reconstructed_text)

reconstructed_text_2 = reconstruct_text_from_indices(file_path_2, indices_2)
print(reconstructed_text_2)
