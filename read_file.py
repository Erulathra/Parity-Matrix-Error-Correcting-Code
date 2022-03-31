import corrector as c

# odczytaj bajty pliku, zakoduj
# i zapisz rezultat do innego pliku
def read_and_encode():
    in_file = open("plik.txt", 'rb').read()
    encoded_file = c.encode_byte_array(bytearray(in_file))
    out_file = open("encoded.txt", 'wb')
    out_file.write(encoded_file)

# Odczytaj bajty pliku, popraw, zdekoduj
# i zapisz rezultat to innego pliku
def read_and_decode():
    in_file = open("encoded.txt", 'rb').read()
    encoded_file = c.correct_byte_array(bytearray(in_file))
    encoded_file = c.decode_byte_array(encoded_file)
    out_file = open("fixed.txt", 'wb')
    out_file.write(encoded_file)
