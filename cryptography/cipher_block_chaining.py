from cryptography.des_algorithm import Des
from cryptography.utilities import (DES_NUM_OF_ROUNDS,
                                    BLOCK_LENGTH_ASCII,
                                    divide_text_to_blocks,
                                    assert_ascii_string,
                                    binary_xor,
                                    ascii_text_to_binary,
                                    hex_to_binary,
                                    assert_n_characters,
                                    assert_hex,
                                    BLOCK_LENGTH_HEX,
                                    ascii_or_hex_to_binary,
                                    binary_to_ascii_text,
                                    remove_null_char_from_end)


class CBC:
    def __init__(self, key, initial_vector):
        assert_ascii_string(key)
        assert_n_characters(key, 8)
        self.__key = key
        assert_ascii_string(key)
        assert_n_characters(key, 8)
        self.__IV = initial_vector
        self.des_engine = Des(key, DES_NUM_OF_ROUNDS)

    def encrypt(self, stream_ascii_text):
        assert_ascii_string(stream_ascii_text)
        list_of_blocks = divide_text_to_blocks(stream_ascii_text, BLOCK_LENGTH_ASCII)
        current_vector = ascii_text_to_binary(self.__IV)
        encrypted_text = ''
        for block in list_of_blocks:
            plain_text = binary_xor(ascii_text_to_binary(block), current_vector)
            self.des_engine.encrypt(plain_text)
            cipher_text = self.des_engine.get_cipher_text()
            encrypted_text += cipher_text
            current_vector = hex_to_binary(cipher_text)
        return encrypted_text

    def decrypt(self, stream_hex_text):
        assert_hex(stream_hex_text)
        list_of_blocks = divide_text_to_blocks(stream_hex_text, BLOCK_LENGTH_HEX)
        current_vector = ascii_text_to_binary(self.__IV)
        decrypted_text = ''
        for block in list_of_blocks:
            self.des_engine.decrypt(block)
            plain_text_before_xor = self.des_engine.get_plain_text()
            binary_plain_text = binary_xor(ascii_or_hex_to_binary(plain_text_before_xor), current_vector)
            decrypted_text += binary_to_ascii_text(binary_plain_text)
            current_vector = hex_to_binary(block)
        return remove_null_char_from_end(decrypted_text)
