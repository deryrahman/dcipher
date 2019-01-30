from .cipher import Cipher
from .helper import pos, in_range_alpha, save_file, open_file
import string
import re


class PlayFairCipher(Cipher):
    def __init__(self, key):
        key, l = list(self.remove_nonalpha(key).upper()
                      ), list(string.ascii_uppercase)
        l.remove('J')
        if 'J' in key:
            key.remove('J')
        key = ''.join(key+l)
        r = []
        for v in key:
            if not v in r:
                r.append(v)
        self.table = [[r[5*i+j] for j in range(5)] for i in range(5)]
        self.map = {self.table[i][j]: (i, j)
                    for i in range(5) for j in range(5)}

    def remove_nonalpha(self, text):
        return re.sub(r'[^a-zA-Z_]', '', text)

    def get_bigram(self, plain_text):
        plain_text = plain_text.upper()
        i, j, edited_plain_text = 1, 1, self.remove_nonalpha(plain_text)
        while i < len(edited_plain_text):
            while edited_plain_text[i-1] != plain_text[j-1]:
                j += 1
            if edited_plain_text[i] == edited_plain_text[i-1]:
                edited_plain_text = edited_plain_text[:i] + \
                    'X' + edited_plain_text[i:]
                plain_text = plain_text[:j] + 'X' + plain_text[j:]
            i += 2
            j += 2
        edited_plain_text = edited_plain_text if len(
            edited_plain_text) % 2 == 0 else edited_plain_text+'X'
        return [edited_plain_text[i:i+2] for i in range(0, len(edited_plain_text), 2)], plain_text

    def get_translation(self, bigrams, en=True):
        res, shift = '', 1 if en else -1
        for v in bigrams:
            i, j = self.map[v[0]], self.map[v[1]]
            if i[0] == j[0]:
                res += self.table[i[0]][(i[1]+shift) %
                                        5] + self.table[j[0]][(j[1]+shift) % 5]
            elif i[1] == j[1]:
                res += self.table[(i[0]+shift) % 5][i[1]] + \
                    self.table[(j[0]+shift) % 5][j[1]]
            else:
                res += self.table[i[0]][j[1]] + self.table[j[0]][i[1]]
        return res

    @open_file
    @save_file
    def encrypt(self, text, key=None, k=0, sp=True, filename=None, fileout=None):
        plain_text = text.upper().replace('J', 'I')
        if not sp:
            plain_text = plain_text.replace(' ', '')
        bigrams, plain_text = self.get_bigram(plain_text)
        res = self.get_translation(bigrams)
        j = 0
        for v in plain_text:
            if not('A' <= v and v <= 'Z'):
                res = res[:j] + v + res[j:]
            j += 1
        return res

    @open_file
    @save_file
    def decrypt(self, text, key=None, filename=None, fileout=None):
        text = text.upper()
        cipher_text = self.remove_nonalpha(text.upper())
        bigrams = [cipher_text[i:i+2] for i in range(0, len(cipher_text), 2)]
        res = self.get_translation(bigrams, en=False).lower()
        j = 0
        for v in text:
            if not('A' <= v and v <= 'Z'):
                res = res[:j] + v + res[j:]
            j += 1
        return res
