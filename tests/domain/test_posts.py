# type: ignore
from datetime import datetime
from unittest.mock import Mock

import inject
import pytest

from src.domain.actions.create_post import CreatePost
from src.domain.actions.get_post import GetPost
from src.domain.actions.search_posts import SearchPosts
from src.domain.post import Post
from src.domain.database_interface import DatabaseInterface
from tests.utils.dates import datetime_to_rfc822_string


@pytest.fixture
def database() -> Mock:
    return Mock()


@pytest.fixture
def injector(database: Mock) -> None:
    inject.clear_and_configure(lambda binder: binder
                               .bind(DatabaseInterface, database))


@pytest.fixture
def post() -> Post:
    return Post(id=1,
                author_name='Alex',
                title='Test Post',
                body='A longer body for this post',
                created_at=datetime.now(),
                updated_at=datetime.now())


@pytest.fixture
def dict_post() -> dict:
    return {
        'authorName': 'Alex',
        'title': 'Test Post',
        'body': 'A longer body for this post',
        'createdAt': datetime_to_rfc822_string(datetime.now()),
        'updatedAt': datetime_to_rfc822_string(datetime.now()),
    }


class TestPosts:
    def test_get_posts(self, injector: None, database: Mock, post: Post) -> None:
        database.get_post.return_value = post

        result = GetPost().execute(1)

        assert result == post
        database.get_post.assert_called_once_with(1)

    def test_search_posts(self, injector: None, database: Mock, post: Post) -> None:
        database.search_posts.return_value = [post]
        database.count_posts.return_value = 100

        result = SearchPosts().execute(start_after=10, end_before=90)

        assert result == ([post], 100)
        database.search_posts.assert_called_once_with(start_after=10, end_before=90)
        database.count_posts.assert_called_once_with()

    def test_create_posts(self,
                          injector: None, database: Mock, dict_post: dict, post: Post) -> None:
        database.create_post.return_value = post

        result = CreatePost().execute(dict_post)

        assert result.title == post.title
        database.create_post.assert_called_once_with(dict_post)
