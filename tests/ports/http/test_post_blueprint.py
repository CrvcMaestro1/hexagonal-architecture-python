from datetime import datetime, timedelta
from unittest.mock import Mock

import inject
import pytest
from flask import Flask
from flask.testing import FlaskClient
from pytest_mock import MockFixture

from src.domain.actions.create_post import CreatePost
from src.domain.actions.get_post import GetPost
from src.domain.actions.search_posts import SearchPosts
from src.domain.post import Post
from src.ports.http.post_blueprint import create_post_blueprint
from tests.utils.dates import datetime_to_rfc822_string


@pytest.fixture
def get_post(mocker: MockFixture) -> Mock:
    return mocker.patch('src.ports.http.post_blueprint.GetPost')


@pytest.fixture
def search_posts(mocker: MockFixture) -> Mock:
    return mocker.patch('src.ports.http.post_blueprint.SearchPosts')


@pytest.fixture
def create_post(mocker: MockFixture) -> Mock:
    return mocker.patch('src.ports.http.post_blueprint.CreatePost')


@pytest.fixture
def injector(get_post: Mock, search_posts: Mock, create_post: Mock) -> None:
    inject.clear_and_configure(lambda binder: binder  # type: ignore
                               .bind(GetPost, get_post)
                               .bind(SearchPosts, search_posts)
                               .bind(CreatePost, create_post))


@pytest.fixture
def client(injector: None) -> FlaskClient:
    application = Flask(__name__)
    application.register_blueprint(create_post_blueprint())
    application.testing = True
    return application.test_client()


@pytest.fixture
def post() -> Post:
    return Post(id=1,
                author_name='Alex',
                title='Test Post',
                body='A longer body for this post',
                created_at=datetime.now(),
                updated_at=datetime.now() + timedelta(hours=1))


@pytest.fixture
def dict_post() -> dict:
    return {'author_name': 'Alex', 'title': 'Test Post', 'body': 'A longer body for this post'}


class TestPostBlueprint:
    def test_list_searches_posts(self, search_posts: Mock, client: FlaskClient,
                                 post: Post) -> None:
        search_posts.execute.return_value = [post], 100

        response = client.get('/posts')

        search_posts.execute.assert_called_once_with(start_after=None, end_before=None)
        assert response.json == {
            'results': [{
                'id': 1,
                'authorName': 'Alex',
                'title': 'Test Post',
                'body': 'A longer body for this post',
                'createdAt': datetime_to_rfc822_string(post.created_at),
                'updatedAt': datetime_to_rfc822_string(post.updated_at),
            }],
            'count': 100
        }

    def test_post_list_parses_query_string(self, search_posts: Mock, client: FlaskClient,
                                           post: Post) -> None:
        search_posts.execute.return_value = [post], 100

        client.get('/posts?start_after=10&end_before=100')

        search_posts.execute.assert_called_once_with(start_after=10, end_before=100)

    def test_detail_gets_post(self, get_post: Mock, client: FlaskClient, post: Post) -> None:
        get_post.execute.return_value = post

        response = client.get('/posts/20')

        get_post.execute.assert_called_once_with(post_id=20)
        assert response.json == {
            'id': 1,
            'authorName': 'Alex',
            'title': 'Test Post',
            'body': 'A longer body for this post',
            'createdAt': datetime_to_rfc822_string(post.created_at),
            'updatedAt': datetime_to_rfc822_string(post.updated_at),
        }

    def test_create_post(self,
                         create_post: Mock,
                         client: FlaskClient, post: Post, dict_post: dict) -> None:
        create_post.execute.return_value = post

        response = client.post('/posts', json=dict_post)

        create_post.execute.assert_called_once_with(post=dict_post)
        assert response.json == {
            'id': 1,
            'authorName': 'Alex',
            'title': 'Test Post',
            'body': 'A longer body for this post',
            'createdAt': datetime_to_rfc822_string(post.created_at),
            'updatedAt': datetime_to_rfc822_string(post.updated_at),
        }
