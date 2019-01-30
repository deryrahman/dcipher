from dcipher import VigenereCipher, FullVigenereCipher, AutoKeyVigenereCipher, RunningKeyVigenereCipher, ExtendedVigenereCipher, PlayFairCipher

cipher = {}

def choose_key():
    filekey = bool(input('Key from file? (y/N) ') == 'y')
    key = ''
    if filekey:
        filekeyname = input('Key file : ')
        with open(filekeyname, 'r') as f:
            key = f.read()
    else:
        key = input('Key : ')
    return key

def choose_cipher(x):
    print("""
    1. VigenereCipher
    2. FullVigenereCipher
    3. AutoKeyVigenereCipher
    4. RunningKeyVigenereCipher
    5. ExtendedVigenereCipher
    6. PlayFairCipher
    """)
    x = int(input("Choose cipher : "))

    if cipher.get('VigenereCipher') == None:
        cipher['VigenereCipher'] = VigenereCipher()
    v = cipher.get('VigenereCipher')
    if x==4:
        print("WARNING! Key must have length greater than plain text")
    key = choose_key()
    if x == 2:
        if cipher.get('FullVigenereCipher') == None:
            cipher['FullVigenereCipher'] = FullVigenereCipher(
                seed=int(input("Seed number : ")))
        v = cipher['FullVigenereCipher']
    elif x == 3:
        if cipher.get('AutoKeyVigenereCipher') == None:
            cipher['AutoKeyVigenereCipher'] = AutoKeyVigenereCipher()
        v = cipher['AutoKeyVigenereCipher']
    elif x == 4:
        if cipher.get('RunningKeyVigenereCipher') == None:
            cipher['RunningKeyVigenereCipher'] = RunningKeyVigenereCipher()
        v = cipher['RunningKeyVigenereCipher']
    elif x == 5:
        if cipher.get('ExtendedVigenereCipher') == None:
            cipher['ExtendedVigenereCipher'] = ExtendedVigenereCipher()
        v = cipher['ExtendedVigenereCipher']
    elif x == 6:
        v = PlayFairCipher(key)
    return x, v, key

def choose_encrypt_decrypt():
    return bool(input("Encrypt/Decrypt? (E/d) ") != 'd')


def choose_filein():
    filein = input('File path : ')
    return filein

def choose_fileout():
    fileout = input('Fileout : ')
    return fileout

def choose_input(is_encrypt):
    is_filein = bool(input('File input? (y/N) ') == 'y')
    filein, text = None, None
    if is_filein:
        filein = choose_filein()
    else:
        text = input('Plain Text : ') if is_encrypt else input(
            'Encrypted Text : ')
    return text, filein


def choose_output():
    save = bool(input('Save? (y/N) ') == 'y')
    fileout = None
    if save:
        fileout = choose_fileout()
    return fileout

def mode():
    group = int(input('Group? (0 if no group) ') or "0")
    withsp = bool(input('With space? (Y/n) ') != 'n') if group == 0 else False
    return group, withsp

if __name__ == '__main__':
    x = 0
    while(x>=0):
        x, v, key = choose_cipher(x)
        if x>=1 and x<=6:
            is_encrypt = choose_encrypt_decrypt()
            is_byte = False
            if isinstance(v, ExtendedVigenereCipher):
                is_byte = bool(input('Any file? (y/N)') == 'y')
            text, filein = None, None
            if not is_byte:
                text, filein = choose_input(is_encrypt)
                fileout = choose_output()
                c = ''
                if is_encrypt:
                    group, withsp = mode()
                    if not filein and fileout:
                        c = v.encrypt(key=key, text=text, k=group if group >
                                      0 else 0, sp=withsp, fileout=fileout)
                    elif not filein:
                        c = v.encrypt(key=key, text=text,
                                      k=group if group > 0 else 0, sp=withsp)
                    if filein and fileout:
                        c = v.encrypt(key=key, filename=filein, k=group if group >
                                      0 else 0, sp=withsp, fileout=fileout)
                    elif filein:
                        c = v.encrypt(key=key, filename=filein,
                                      k=group if group > 0 else 0, sp=withsp)
                else:
                    if filein and fileout:
                        c = v.decrypt(key=key, filename=filein,
                                      fileout=fileout)
                    elif filein:
                        c = v.decrypt(key=key, filename=filein)
                    elif fileout:
                        c = v.decrypt(key=key, text=text, fileout=fileout)
                    else:
                        c = v.decrypt(key=key, text=text)

                if filein:
                    with open(filein, 'r') as f:
                        print(f.read())
                else:
                    print(text)
                print(c)
            else:
                filein = choose_filein()
                fileout = choose_fileout()
                if is_encrypt:
                    c = v.encrypt(key=key, filename=filein,
                                  fileout=fileout, type='b')
                else:
                    c = v.decrypt(key=key, filename=filein,
                                  fileout=fileout, type='b')
            print('================')
        elif x<0:
            continue
        else:
            print("Available 1-6")
