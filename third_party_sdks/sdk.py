from abc import ABC, abstractclassmethod


class SDK(ABC):
    @abstractclassmethod
    def get_query():
        ...

    @abstractclassmethod
    def post_query():
        ...

    @abstractclassmethod
    def new_position(self, **kwargs):
        ...

    @abstractclassmethod
    def get_account(self):
        ...
