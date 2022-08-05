import inject
from flask import Blueprint, jsonify, Response, request

from src.domain.actions.create_post import CreatePost
from src.domain.actions.get_post import GetPost
from src.domain.actions.search_posts import SearchPosts


@inject.autoparams()
def create_post_blueprint(
        search_posts: SearchPosts,
        get_post: GetPost,
        create_post: CreatePost
) -> Blueprint:
    post_blueprint = Blueprint('post', __name__)

    @post_blueprint.route('/posts')
    def post_list() -> Response:
        start_after_request = request.args.get('start_after')
        start_after = int(start_after_request) if start_after_request else None
        end_before_request = request.args.get('end_before')
        end_before = int(end_before_request) if end_before_request else None

        posts, count = search_posts.execute(start_after=start_after, end_before=end_before)

        return jsonify({
            'results': [post.to_dict() for post in posts],  # type: ignore
            'count': count
        })

    @post_blueprint.route('/posts/<int:post_id>')
    def post_detail(post_id: int) -> Response:
        post = get_post.execute(post_id=post_id)
        return jsonify(post.to_dict())  # type: ignore

    @post_blueprint.route('/posts', methods=['POST'])
    def post_create() -> Response:
        data: dict | None = request.get_json()
        post = create_post.execute(post=data)  # type: ignore
        return jsonify(post.to_dict())  # type: ignore

    return post_blueprint
