import random

from bitarray import bitarray
from colorama import Fore

import corrector as c
from read_file import read_and_encode, read_and_decode


def main():
    # my_file = "file.bin"
    #
    # error_list = []
    # test = bytearray()
    #
    # for i in range(100):
    #     test.append(random.randint(0, 254))
    #
    # print(f"Startowy: {test}")
    # test_encoded = c.encode_byte_array(test)
    # corrupted = c.corrupt_byte_array(test_encoded, 75)
    # print(f"Popsuty: {c.decode_byte_array(corrupted)}")
    # corrected = c.correct_byte_array(corrupted)
    # print(f"Po korekcji: {c.decode_byte_array(corrected)}")
    # print(f"czy po korekcji wiadomość jest taka sama: {test_encoded == corrected}")
    try:
        user = str(input("Podaj czy chcesz enkodwać (e), denkodować (d)"))
        if user == 'e':
            read_and_encode()

        elif user == 'd':
            read_and_decode()
    except:
        print("Something goes wrong")


if __name__ == "__main__":
    main()
