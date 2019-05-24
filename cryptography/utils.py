from cryptography.cipher_block_chaining import CBC
from funtestic_backend.settings import DES_KEY, CBC_IV


class CbcEngine:

    def __init__(self):
        self.cbc = CBC(DES_KEY, CBC_IV)

    def encrypt(self, ascii_text):
        return self.cbc.encrypt(ascii_text)

    def decrypt(self, hex_text):
        return self.cbc.decrypt(hex_text)

    def decrypt_child_json(self, child_json):
        child_json['id_number'] = self.decrypt(child_json['id_number'])
        child_json['name'] = self.decrypt(child_json['name'])
        child_json['age'] = self.decrypt(child_json['age'])
        child_json['gender'] = self.decrypt(child_json['gender'])
        child_json['parent_id'] = self.decrypt(child_json['parent_id'])
        child_json['parent'] = self.decrypt_parent_json(child_json['parent'])
        return child_json

    def decrypt_parent_json(self, parent_json):
        parent_json['phone_number'] = self.decrypt(parent_json['phone_number'])
        user_json = parent_json['user']
        user_json['first_name'] = self.decrypt(user_json['first_name'])
        user_json['last_name'] = self.decrypt(user_json['last_name'])
        user_json['email'] = self.decrypt(user_json['email'])
        parent_json['user'] = user_json
        return parent_json

    __instance = None

    @staticmethod
    def get_engine():
        if not CbcEngine.__instance:
            CbcEngine.__instance = CbcEngine()
        return CbcEngine.__instance
