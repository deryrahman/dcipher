from abc import ABC, abstractmethod


class Cipher(ABC):
    @abstractmethod
    def encrypt(self, *args, **kwargs):
        pass

    @abstractmethod
    def decrypt(self, *args, **kwargs):
        pass
