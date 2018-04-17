import base64
from Crypto.Cipher import AES
from Crypto import Random
from enti.settings import AppConfig

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class AESCipher:
    def __init__(self, key=None):

        key = AppConfig.SECRET_KEY if key is None else key

        if len(key) > 32:
            key = key[:32]
        elif len(key) < 32:
            while len(key) < 32:
                key += '*'
        self.key = key

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def encrypt_utf8(self, raw):
        return self.encrypt(raw).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))

    def decrypt_utf8(self, enc):
        return self.decrypt(enc).decode('utf-8')

if __name__ == '__main__':

    print('Testing AES Cipher')

    key = AppConfig.SECRET_KEY
    cipher = AESCipher(key)
    input = 'password123!@#$%^&*(),./;:\'"[{]}\\|'
    encrypted = cipher.encrypt_utf8(input)
    decrypted = cipher.decrypt_utf8(encrypted)

    print('UTF-8 Secret Key:         {}'.format(key))
    print('UTF-8 Input String:       {}'.format(input))
    print('UTF-8 Encrypted String:   {}'.format(encrypted))
    print('UTF-8 Decrypted String:   {}'.format(decrypted))
    print('Encrypted String Length:  {}'.format(len(encrypted)))
    print('String Growth Factor:     {:.2f}'.format(len(encrypted)/len(decrypted)))

    assert input == decrypted, "Cipher failed to decrypt message"
    print('AES Cipher is working as expected')
