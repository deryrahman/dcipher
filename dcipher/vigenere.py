from .cipher import Cipher
from .helper import pos, in_range_alpha, save_file, open_file
import re
import random
import string


class VigenereCipher(Cipher):
    def __init__(self):
        self.table = [[chr(ord('A')+(i+j) % 26)
                       for j in range(26)] for i in range(26)]

    def remove_nonalpha(self, text):
        return re.sub(r'[^a-zA-Z_]', '', text)

    def get_repeated_key(self, key, plain_text):
        key = self.remove_nonalpha(key.upper())
        plain_text = self.remove_nonalpha(plain_text)
        return (key*(len(plain_text)//len(key)+1))[:len(plain_text)]

    @open_file
    @save_file
    def encrypt(self, key, text, filename=None, k=0, sp=True, fileout=None, type=None):
        plain_text = text.upper()
        repeated_key = self.get_repeated_key(key, plain_text)
        plain_text = plain_text.replace(' ', '') if not sp else plain_text
        j, res = 0, ''
        for v in plain_text:
            if not in_range_alpha(v):
                res += v
            else:
                res += self.table[pos(repeated_key[j])][pos(v)]
                j += 1
        res = ' '.join([res[i:i+k]
                        for i in range(0, len(res), k)]) if k > 0 else res
        return res

    @open_file
    @save_file
    def decrypt(self, key, text, filename=None, fileout=None, type=None):
        cipher_text = text.upper()
        repeated_key = self.get_repeated_key(key, cipher_text)
        j, res = 0, ''
        for v in cipher_text:
            if not in_range_alpha(v):
                res += v
            else:
                res += chr(ord('a')+self.table[pos(repeated_key[j])].index(v))
                j += 1
        return res


class FullVigenereCipher(VigenereCipher):
    def __init__(self, table=None, seed=None):
        if seed:
            random.seed(seed)
        if table:
            super.__init__(self)
            return
        s = string.ascii_uppercase
        self.table = [random.sample(s, len(s)) for i in range(26)]


class AutoKeyVigenereCipher(VigenereCipher):
    def get_repeated_key(self, key, plain_text):
        try:
            return self.saved_key
        except:
            edited_plain_text = self.remove_nonalpha(''.join(plain_text))
            key = (key.upper()+edited_plain_text)[:len(edited_plain_text)]
            self.saved_key = super().get_repeated_key(key, plain_text)
        return self.saved_key


class RunningKeyVigenereCipher(VigenereCipher):
    def get_repeated_key(self, key, plain_text):
        if len(key) < len(plain_text):
            raise Exception("Key must has length larger than plain text")
        return super().get_repeated_key(key, plain_text)


class ExtendedVigenereCipher(VigenereCipher):
    def __init__(self):
        self.table = [[(i+j) % 256 for j in range(256)] for i in range(256)]

    def get_repeated_key(self, key, plain_text):
        return (key*(len(plain_text)//len(key)+1))[:len(plain_text)]

    @open_file
    @save_file
    def encrypt(self, key, text, filename=None, k=None, sp=None, fileout=None, type=None):
        plain_text = text
        repeated_key = self.get_repeated_key(key, plain_text)
        if type == 'b':
            return [self.table[ord(j)][i] for i, j in zip(plain_text, repeated_key)]
        return ''.join([chr(self.table[ord(j) % 256][ord(i) % 256]) for i, j in zip(plain_text, repeated_key)])

    @open_file
    @save_file
    def decrypt(self, key, text, filename=None, fileout=None, type=None):
        cipher_text = text
        repeated_key = self.get_repeated_key(key, cipher_text)
        if type == 'b':
            return [self.table[ord(j)].index(i) for i, j in zip(cipher_text, repeated_key)]
        return ''.join([chr(self.table[ord(j) % 256].index(ord(i) % 256)) for i, j in zip(cipher_text, repeated_key)])
