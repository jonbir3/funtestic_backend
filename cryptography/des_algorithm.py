from cryptography.utilities import *


class Des:

    MAX_ROUND = 16
    KEY_LENGTH_BITS = 64

    INITIAL_PERMUTATION = [
        58, 50, 42, 34, 26, 18, 10,  2,
        60, 52, 44, 36, 28, 20, 12,  4,
        62, 54, 46, 38, 30, 22, 14,  6,
        64, 56, 48, 40, 32, 24, 16,  8,
        57, 49, 41, 33, 25, 17,  9,  1,
        59, 51, 43, 35, 27, 19, 11,  3,
        61, 53, 45, 37, 29, 21, 13,  5,
        63, 55, 47, 39, 31, 23, 15,  7
    ]

    FINAL_PERMUTATION = [
        40,  8, 48, 16, 56, 24, 64, 32,
        39,  7, 47, 15, 55, 23, 63, 31,
        38,  6, 46, 14, 54, 22, 62, 30,
        37,  5, 45, 13, 53, 21, 61, 29,
        36,  4, 44, 12, 52, 20, 60, 28,
        35,  3, 43, 11, 51, 19, 59, 27,
        34,  2, 42, 10, 50, 18, 58, 26,
        33,  1, 41,  9, 49, 17, 57, 25
    ]

    EXPANSION = [
        32,  1,  2,  3,  4,  5,  4,  5,
        6,  7,  8,  9,  8,  9, 10, 11,
        12, 13, 12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21, 20, 21,
        22, 23, 24, 25, 24, 25, 26, 27,
        28, 29, 28, 29, 30, 31, 32,  1
    ]

    S1 = [
        [14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
        [0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
        [4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
        [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]
    ]

    S2 = [
        [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
        [3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
        [0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
        [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]
    ]

    S3 = [
        [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
        [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
        [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
        [1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]
    ]

    S4 = [
        [7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
        [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
        [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
        [3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]
    ]

    S5 = [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ]

    S6 = [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ]

    S7 = [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ]

    S8 = [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]

    S_BOXES = [S1, S2, S3, S4, S5, S6, S7, S8]

    F_PERMUTATION = [
        16,  7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26,  5, 18, 31, 10,
        2,  8, 24, 14, 32, 27,  3,  9,
        19, 13, 30,  6, 22, 11,  4, 25
    ]

    PC1 = [
        57, 49, 41, 33, 25, 17,  9,
        1, 58, 50, 42, 34, 26, 18,
        10,  2, 59, 51, 43, 35, 27,
        19, 11,  3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14,  6, 61, 53, 45, 37, 29,
        21, 13,  5, 28, 20, 12,  4
    ]

    PC2 = [
        14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    ]

    @staticmethod
    def do_permutation(binary_text, matrix):
        """do permutation with given matrix on the given binary block"""
        output = ''
        for val in matrix:
            output += binary_text[val - 1]
        return output

    @staticmethod
    def left_rotate(string, n):
        """do n shift left on the string"""
        if n <= 0:
            raise ValueError('The number of rotation steps must be positive')
        return string[n:] + string[:n]

    def __init__(self, key, num_of_rounds):
        if not 0 < num_of_rounds <= Des.MAX_ROUND:
            raise ValueError('The number of rounds must be between 1 to {0}'.format(Des.MAX_ROUND))
        self.__binary_key = ''
        self.set_key(key)
        self.__plain_text = ''
        self.__cipher_text = ''
        self.__current_binary_text = ''  # intermediate values of the rounds
        self.__num_of_rounds = num_of_rounds
        self.__round_keys = []

    def get_plain_text(self):
        return self.__plain_text

    def set_plain_text(self, plain_text):
        assert_string(plain_text)
        if is_binary(plain_text):
            assert_n_bits(plain_text, 64)
        elif is_hex_number(plain_text):
            assert_n_characters(plain_text, 16)
        else:
            assert_n_characters(plain_text, 8)
        self.__plain_text = plain_text

    def get_cipher_text(self):
        return self.__cipher_text

    def set_cipher_text(self, hex_cipher_text):
        assert_string(hex_cipher_text)
        assert_n_bits(hex_cipher_text, 16)
        self.__cipher_text = hex_cipher_text

    def set_key(self, new_key):
        """set a private key. if the key has less than 64 bits- fills the missing bits with 0's"""
        binary_key = ascii_text_to_binary(new_key)
        if len(binary_key) < Des.KEY_LENGTH_BITS:
            for _ in range(Des.KEY_LENGTH_BITS - len(binary_key)):
                binary_key += '0'
        assert_n_bits(binary_key, 64)
        self.__binary_key = binary_key

    def initial_permutation_step(self):
        self.__current_binary_text = Des.do_permutation(self.__current_binary_text, Des.INITIAL_PERMUTATION)

    def final_permutation_step(self):
        assert_n_bits(self.__current_binary_text, 64)
        self.__current_binary_text = Des.do_permutation(self.__current_binary_text, Des.FINAL_PERMUTATION)

    def generate_round_keys(self, decrypt=False):
        """generate the round keys.
        if decrypt is true- save the keys reversed: key 16 for round 1, key 15 for round 2 etc."""
        self.__round_keys = []
        binary_key = Des.do_permutation(self.__binary_key, Des.PC1)  # PC_1 permutation
        assert_n_bits(binary_key, 56)
        left_key = binary_key[0:28]
        right_key = binary_key[28:56]
        for i in range(1, self.__num_of_rounds + 1):  # shift left
            if i in (1, 2, 9, 16):
                left_key = Des.left_rotate(left_key, 1)
                right_key = Des.left_rotate(right_key, 1)
            else:
                left_key = Des.left_rotate(left_key, 2)
                right_key = Des.left_rotate(right_key, 2)
            current_round_key = Des.do_permutation(left_key + right_key, Des.PC2)  # PC_2 permutation
            assert_n_bits(current_round_key, 48)
            self.__round_keys.append(current_round_key)
        if decrypt:
            self.__round_keys.reverse()

    def des_f_function(self, right_binary_text, round_number):
        assert_n_bits(right_binary_text, 32)
        if not 0 < round_number <= self.__num_of_rounds:
            raise ValueError('The round number must be between 1 to {0}'.format(self.__num_of_rounds))
        right_binary_text = Des.do_permutation(right_binary_text, Des.EXPANSION)  # E permutation
        assert_n_bits(right_binary_text, 48)
        right_binary_text = binary_xor(right_binary_text, self.__round_keys[round_number - 1])  # xor
        assert_n_bits(right_binary_text, 48)
        groups_of_6_bits = [right_binary_text[i * 6:i * 6 + 6] for i in range(len(right_binary_text) // 6)]
        if len(groups_of_6_bits) != 8:
            raise ValueError('Error while dividing the text to groups of 6 bits')
        text_after_s_boxes = ''
        for i in range(len(groups_of_6_bits)):  # s-boxes
            assert_n_bits(groups_of_6_bits[i], 6)
            binary_row = groups_of_6_bits[i][:1] + groups_of_6_bits[i][-1:]
            binary_col = groups_of_6_bits[i][1:-1]
            s_box_val = Des.S_BOXES[i][int(binary_row, 2)][int(binary_col, 2)]
            text_after_s_boxes += ascii_val_to_binary(s_box_val, 4)
        assert_n_bits(text_after_s_boxes, 32)
        return Des.do_permutation(text_after_s_boxes, Des.F_PERMUTATION)  # P permutation

    def des_algorithm(self, decrypt=False):
        if not decrypt and self.__plain_text == '' or decrypt and self.__cipher_text == '':
            raise Exception('There is no plain text')
        self.generate_round_keys(decrypt)
        self.initial_permutation_step()
        assert_n_bits(self.__current_binary_text, 64)
        left, right = '', ''
        for round_number in range(1, self.__num_of_rounds + 1):
            left = self.__current_binary_text[0:32]
            right = self.__current_binary_text[32:64]
            f_result = self.des_f_function(right, round_number)
            new_right = binary_xor(f_result, left)
            left = right
            right = new_right
            self.__current_binary_text = left + right
        self.__current_binary_text = right + left
        self.final_permutation_step()
        assert_n_bits(self.__current_binary_text, 64)

    def encrypt(self, text_to_encrypt):
        """
        text_to_encrypt can be ascii, hex or binary text.
        the encrypted text text is hex text.
        """
        self.set_plain_text(text_to_encrypt)
        self.set_cipher_text('')
        if is_binary(text_to_encrypt):
            self.__current_binary_text = text_to_encrypt
        elif is_hex_number(self.__plain_text):
            self.__current_binary_text = hex_to_binary(self.__plain_text)
        elif is_ascii(text_to_encrypt):
            self.__current_binary_text = ascii_text_to_binary(self.__plain_text)
        self.des_algorithm()
        self.set_cipher_text(binary_to_hex(self.__current_binary_text))
        self.set_plain_text('')
        self.__current_binary_text = ''

    def decrypt(self, text_to_decrypt):
        """
        text_to_decrypt must be hex text.
        the decrypted text is ascii or hex text.
        """
        self.set_plain_text('')
        self.set_cipher_text(text_to_decrypt)
        self.__current_binary_text = hex_to_binary(self.__cipher_text)
        self.des_algorithm(True)
        self.set_plain_text(binary_to_ascii_text(self.__current_binary_text))
        if not is_ascii(self.get_plain_text()):
            self.set_plain_text(binary_to_hex(self.__current_binary_text))
        self.set_cipher_text('')
        self.__current_binary_text = ''
