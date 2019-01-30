import os.path

def pos(c):
    return ord(c.upper())-ord('A')


def in_range_alpha(c):
    return pos(c) < 26 and pos(c) >= 0


def save_file(f):
    def wrapper_func(*args, **kwargs):
        res = f(*args, **kwargs)
        fileout = kwargs.get('fileout')
        if not fileout:
            return res
        if kwargs.get('type') == 'b':
            with open(fileout, 'wb') as file:
                for v in res:
                    file.write(bytes([v]))
        else:
            with open(fileout, 'w') as file:
                s = file.write(res)
        return res
    return wrapper_func


def open_file(f):
    def wrapper_func(*args, **kwargs):
        filename = kwargs.get('filename')
        if not filename or not os.path.isfile(filename):
            return f(*args, **kwargs)
        if kwargs.get('type') == 'b':
            with open(filename, 'rb') as file:
                byte = file.read(1)
                kwargs['text'] = []
                while byte:
                    kwargs['text'].append(ord(byte))
                    byte = file.read(1)
        else:
            with open(filename, 'r') as file:
                kwargs['text'] = file.read()
        kwargs['filename'] = None
        return f(*args, **kwargs)
    return wrapper_func
