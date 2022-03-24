import corrector as c

def read_and_encode():
    in_file = open("plik.txt", 'rb').read()
    encoded_file = c.encode_byte_array(in_file)
    out_file = open("encoded.txt", 'wb')
    out_file.write(encoded_file)

read_and_encode()