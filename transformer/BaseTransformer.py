from abc import ABCMeta, abstractmethod


class BaseTransformer:
    __metaclass__ = ABCMeta

    @abstractmethod
    def transform(self, *args, **kwargs):
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if cls is BaseTransformer:
            if any("transform" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented

    def __init__(self, params):
        pass
