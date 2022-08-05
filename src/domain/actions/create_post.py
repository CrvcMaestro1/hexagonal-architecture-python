import inject

from src.domain.post import Post
from src.domain.database_interface import DatabaseInterface


class CreatePost:
    @inject.autoparams()
    def __init__(self, database: DatabaseInterface):
        self.__database = database

    def execute(self, post: dict) -> Post:
        return self.__database.create_post(post)
