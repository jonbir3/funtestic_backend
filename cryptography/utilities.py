from math import ceil

MAX_ASCII_VAL = 127
DES_NUM_OF_ROUNDS = 16
BLOCK_LENGTH_HEX = 16
BLOCK_LENGTH_ASCII = 8
PADDING_CHAR = '\0'


def assert_string(arg):
    if not isinstance(arg, str):
        raise TypeError('The argument must be of string type')


def assert_ascii_string(text):
    assert_string(text)
    for ch in text:
        assert_ascii(char_to_ascii_val(ch))


def assert_char(arg):
    assert_string(arg)
    if len(arg) != 1:
        raise TypeError('The argument is not a character')


def assert_hex(text):
    assert_string(text)
    for ch in text:
        if not is_hex_number(ch):
            raise TypeError('The text must be hex')


def assert_ascii(arg):
    if type(arg) != int or not 0 <= arg <= MAX_ASCII_VAL:
        raise TypeError('The argument must be an ascii value')


def assert_n_characters(text, n):
    if len(text) != n and text != '':
        raise TypeError('The text must be with {0} characters'.format(n))


def assert_n_bits(text, n):
    if len(text) != n and text != '':
        raise TypeError('The text must be with {0} bits'.format(n))


def assert_binary(text):
    chars_set = set(text)
    if not (chars_set == {'0', '1'} or chars_set == {'0'} or chars_set == {'1'}):
        raise TypeError('The variable must be binary')


def char_to_ascii_val(char):
    assert_char(char)
    return ord(char)


def ascii_val_to_char(ascii_val):
    assert_ascii(ascii_val)
    return chr(ascii_val)


def binary_to_ascii_val(binary_val):
    assert_string(binary_val)
    return int(binary_val, 2)


def ascii_val_to_binary(ascii_val, max_bits=8):
    assert_ascii(ascii_val)
    return '{0:0{1}b}'.format(ascii_val, max_bits)


def ascii_text_to_binary(text):
    return ''.join([ascii_val_to_binary(char_to_ascii_val(ch)) for ch in text])


def binary_to_ascii_text(binary_text):
    assert_binary(binary_text)
    if len(binary_text) % 8 != 0:
        raise ValueError('The binary text length must be a duplicate of 8')
    return ''.join(chr(int(binary_text[i * 8: i * 8 + 8], 2)) for i in range(len(binary_text) // 8))


def binary_to_hex(binary_text):
    assert_binary(binary_text)
    if len(binary_text) % 8 != 0:
        raise ValueError('The binary text length must be a duplicate of 8')
    return ''.join('{0:02X}'.format(int(binary_text[i * 8: i * 8 + 8], 2)) for i in range(len(binary_text) // 8))


def hex_to_binary(hex_text):
    if len(hex_text) % 2 != 0:
        raise ValueError('The hex text length must be a duplicate of 2')
    return ''.join('{0:08b}'.format(int(hex_text[i * 2: i * 2 + 2], 16)) for i in range(len(hex_text) // 2))


def binary_xor(left_element, right_element):
    """do binary xor on the bits of the two elements"""
    assert_string(left_element)
    assert_string(right_element)
    assert_n_bits(left_element, len(right_element))
    return '{0:0{1}b}'.format(int(left_element, 2) ^ int(right_element, 2), len(right_element))


def is_hex_number(text):
    try:
        int(text, 16)
        return True
    except ValueError:
        return False


def is_ascii(text):
    return all(ord(c) <= MAX_ASCII_VAL for c in text)


def is_binary(text):
    set_of_chars = set(text)
    return set_of_chars in ({'0', '1'}, {'0'}, {'1'})


def divide_text_to_blocks(ascii_text, block_bit_size):
    blocks = [ascii_text[i * block_bit_size:i * block_bit_size + block_bit_size]
              for i in range(ceil(len(ascii_text) / block_bit_size))]
    last_block = blocks[-1]
    return blocks[:-1] + [last_block_padding(last_block)]


def last_block_padding(ascii_block):
    if len(ascii_block) < BLOCK_LENGTH_ASCII:
        for _ in range(BLOCK_LENGTH_ASCII - len(ascii_block)):
            ascii_block += PADDING_CHAR
    return ascii_block


def ascii_or_hex_to_binary(text):
    if is_hex_number(text):
        return hex_to_binary(text)
    elif is_ascii(text):
        return ascii_text_to_binary(text)
    else:
        raise TypeError('The text must be hex or ascii')


def remove_null_char_from_end(text):
    while text[-1] == '\0':
        text = text[:-1]
    return text
