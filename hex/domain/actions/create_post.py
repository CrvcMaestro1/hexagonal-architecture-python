import inject

from hex.domain.post import Post
from hex.domain.database_interface import DatabaseInterface


class CreatePost:
    @inject.autoparams()
    def __init__(self, database: DatabaseInterface):
        self.__database = database

    def execute(self, post: dict) -> Post:
        return self.__database.create_post(post)
