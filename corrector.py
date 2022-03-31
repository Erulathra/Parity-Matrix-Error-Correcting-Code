import random

import bitarray as bitarray
import numpy as np
from bitarray import *

# constant values, improves readability
number_of_parity_bits = 8
number_of_bits_in_byte = 8

# Matrix which satisfies two conditions:
# - there are no repeating rows
# - each row has unique sum of all of its values
matrix_H = np.array((
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
))


class CorrectingError(Exception):
    pass


# Code markings description:
# [UTIL] - self-describing, simple function, 
#          exist mainly to improve code readability
# [TEST] - code written for testing only, doesn't
#          add any real functionality


# read byte_array and encode each byte
# by passing it to encode_byte()
# and append first two bits
def encode_byte_array(byte_array: bytearray):
    result = bytearray()
    for byte in byte_array:
        byte_as_bit_array = byte_to_bit_array(byte)
        encoded_byte = bytearray(encode_byte(byte_as_bit_array).tobytes())
        result.append(encoded_byte[0])
        result.append(encoded_byte[1])
    return result


# read every second byte from encoded_byte_array
# and return
def decode_byte_array(encoded_byte_array: bytearray):
    return encoded_byte_array[::2]


# read every second byte from encoded_byte_array
# combine info byte and guard byte together as bitarray
# correct resulting bitarray via correct_byte()
# and append first two bits at the end
def correct_byte_array(encoded_byte_array: bytearray):
    result = bytearray()
    for i in range(0, len(encoded_byte_array), 2):
        byte_as_bit_array = encoded_byte_to_bit_array(encoded_byte_array[i], encoded_byte_array[i + 1])
        corrected_byte = bytearray(correct_byte(byte_as_bit_array).tobytes())

        result.append(corrected_byte[0])
        result.append(corrected_byte[1])
    return result


# [UTIL]
# convert byte to array of bits
def byte_to_bit_array(byte: int) -> bitarray:
    result = ''
    for i in range(number_of_bits_in_byte):
        result += str(byte % 2)
        byte = int(np.floor(byte / 2))
    return bitarray(result[::-1])


# [UTIL]
# convert two bytes to a single bitarray
#   [a, b, c], [d, e, f] -> [a, b, c, d, e, f]
def encoded_byte_to_bit_array(byte_one, byte_two) -> bitarray:
    byte_as_bit_array = bitarray()

    for j in range(number_of_bits_in_byte):
        byte_as_bit_array.append(byte_to_bit_array(byte_one)[j])

    for j in range(number_of_parity_bits):
        byte_as_bit_array.append(byte_to_bit_array(byte_two)[j])

    return byte_as_bit_array


# encode byte by adding parity byte:
# slice hamming_matrix to have number of rows equal to number_of_parity_bits
# calculate parity byte:
#   (hamming_matrix * T(word_array)) % 2
# and finally combine information and parity byte:
#   [a, b, c], [d, e, f] -> [a, b, c, d, e, f]
# return the result
def encode_byte(one_byte: bitarray) -> bitarray:
    hamming_matrix = matrix_H[0:, :number_of_parity_bits]
    word_array = bit_array_to_vector(one_byte)

    parity_byte = hamming_matrix.dot(word_array.T)
    parity_byte %= 2

    encoded_byte = bitarray()
    for i in range(number_of_bits_in_byte):
        encoded_byte.append(word_array[i])

    for i in range(number_of_parity_bits):
        encoded_byte.append(parity_byte[i])

    return encoded_byte


# [UTIL]
# convert bitarray to np.array containing int from bits
def bit_array_to_vector(bits: bitarray) -> np.ndarray:
    result = []
    for i in range(len(bits)):
        result.append(int(bits[i]))
    return np.array(result)


# calculate:
#   matrix_H * np.array(coded_byte) % 2
# returns column that should be equal
# to one of the matrix_H column
def calculate_syndrome(coded_byte) -> np.ndarray:
    syndrome_array = bit_array_to_vector(coded_byte)
    result: np.ndarray = matrix_H.dot(syndrome_array)
    return result % 2


# [UTIL]
# returns true if there are no 1's in array
def check_coded_byte(syndrome: np.ndarray) -> bool:
    return np.count_nonzero(syndrome) == 0


# calculates coded_byte syndrome and then
# tries to correct it
def correct_byte(coded_byte: bitarray):
    syndrome = calculate_syndrome(coded_byte)
    coded_byte_copy = coded_byte.copy()

    if check_coded_byte(syndrome):
        return coded_byte

    try:
        return try_correct_one_bit(coded_byte_copy, syndrome)
    except CorrectingError:
        pass
    try:
        return try_correct_two_bits(coded_byte_copy, syndrome)
    except CorrectingError:
        raise CorrectingError()


# checks if syndrome array has
# corresponding column in transformed matrix_H
# if so, flip the bit on position equal to column number
# else raise error (there was more than one corrupted bit)
def try_correct_one_bit(coded_byte: bitarray, syndrome: np.ndarray):
    i = 0
    for column in matrix_H.T:
        # check if corresponding values of syndrome and column
        # are equal to each other
        if np.equal(syndrome, column).all():
            coded_byte[i] ^= 1
            return coded_byte
        i += i

    raise CorrectingError()


# function sums two different rows of matrix_H,
#  making sure each element has either 0 or 1 as value
# if the syndrom and sum are identical, bits of coded_byte
#  on positions of rows in sum are corrected
# else raise error (there was more than two corrupted bits)
def try_correct_two_bits(coded_byte: bitarray, syndrome: np.ndarray):
    i = 0
    j = 0
    for column in matrix_H.T:
        for column2 in matrix_H.T:
            if i == j:
                continue

            sum_of_two_columns = (column + column2) % 2
            if np.equal(sum_of_two_columns, syndrome).all():
                coded_byte[i] ^= 1
                coded_byte[j] ^= 1
                return coded_byte
            j += 1
        i += 1
        j = 0

    raise CorrectingError()


# [UTIL]
# return first 8 bits of bitarray
def decode_byte(coded_byte: bitarray) -> bitarray:
    return coded_byte[:8]



# [TEST]
# simulate data corruption in transmission
def corrupt_byte_array(encoded_byte_array: bytearray, corrupted_percentage: float):
    result = encoded_byte_array.copy()

    result = bytearray()
    for i in range(0, len(encoded_byte_array), 2):
        corrupted_byte = encoded_byte_array[i:i+2]
        if random.random() <= (corrupted_percentage / 100):
            byte_as_bit_array = encoded_byte_to_bit_array(encoded_byte_array[i], encoded_byte_array[i + 1])
            corrupted_byte = bytearray(simulate_noise(byte_as_bit_array, 2).tobytes())

        result.append(corrupted_byte[0])
        result.append(corrupted_byte[1])
    return result


# [TEST], [UTIL]
# helper function for corrupt_byte_array()
# simulates byte corruption by switching
# value of bits in coded_byte
# in quantity of number_of_switched_bits
def simulate_noise(coded_byte: bitarray, number_of_switched_bits: int):
    result = coded_byte.copy()

    coded_byte_range = range(0, number_of_parity_bits + number_of_bits_in_byte - 1)
    switched_bits_indexes = random.sample(coded_byte_range, number_of_switched_bits)
    for i in switched_bits_indexes:
        result[i] ^= 1
    return result
