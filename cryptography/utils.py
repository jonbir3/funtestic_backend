from cryptography.cipher_block_chaining import CBC
from funtestic_backend.settings import DES_KEY, CBC_IV


class CbcEngine:

    def __init__(self):
        self.cbc = CBC(DES_KEY, CBC_IV)

    def encrypt(self, ascii_text):
        return self.cbc.encrypt(ascii_text)

    def decrypt(self, hex_text):
        return self.cbc.decrypt(hex_text)

    __instance = None

    @staticmethod
    def get_engine():
        if not CbcEngine.__instance:
            CbcEngine.__instance = CbcEngine()
        return CbcEngine.__instance
