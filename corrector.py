import numpy as np
from bitarray import *

number_of_parity_bits = 8
number_of_bits_in_byte = 8

matrix_H = np.array((
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1])
)


def bit_array_to_vector(bits: bitarray) -> np.ndarray:
    result = []
    for i in range(len(bits)):
        result.append(int(bits[i]))
    return np.array(result)


def check_word(dword: bitarray) -> bool:
    dword_array = bit_array_to_vector(dword)
    result: np.ndarray = matrix_H.dot(dword_array)
    result %= 2
    return result.sum() == 0


def encode_word(word: bitarray) -> bitarray:
    hamming_matrix = matrix_H[0:, :number_of_parity_bits]
    word_array = bit_array_to_vector(word)

    parity_byte = hamming_matrix.dot(word_array.T)
    parity_byte %= 2

    encoded_byte = bitarray()
    for i in range(number_of_bits_in_byte):
        encoded_byte.append(word_array[i])

    for i in range(number_of_parity_bits):
        encoded_byte.append(parity_byte[i])

    return encoded_byte


def decode_word(dword: bitarray) -> bitarray:
    return dword[:8]
