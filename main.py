from bitarray import bitarray

import corrector as c


def main():
    byte = bitarray('10101101')
    encoded = c.encode_word(byte)
    print(f"encoded: {encoded}")
    print(f"Czy jest encoded jest parzysty: {c.check_word(encoded)}")
    encoded_with_error = encoded.copy()
    encoded_with_error[1] = 1
    print(f"encoded z błędem: {encoded_with_error}")
    print(f"Czy jest encoded z błędem jest parzysty: {c.check_word(encoded_with_error)}")
    print(f"dekodowanie: {c.decode_word(encoded)}")


if __name__ == "__main__":
    main()
