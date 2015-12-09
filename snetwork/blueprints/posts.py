from flask import Blueprint, jsonify, url_for, request
from snetwork.models import Post
from snetwork.core import oauth

app = Blueprint('snetwork.blueprints.posts', __name__)
mimetype = 'application/vnd.api+json'


@app.route('me/feed', methods=['GET'])
def get_user_feed():
    fields = request.args.get('fields[posts]', '').split(',')
    posts = Post.query.order_by(Post.id.desc()).all()
    posts_dict_list = list()
    for post in posts:
        post_dict = {
            'type': 'posts',
            'id': str(post.id)
            }
        attributes = dict()
        relationships = dict()
        if 'message' in fields:
            attributes.update(dict(message=post.message))
        if 'created_at' in fields:
            attributes.update(dict(created_at=post.created_at
                                   .strftime('%Y-%m-%dT%H:%M:%Sz')))
        if attributes:
            post_dict.update(dict(attributes=attributes))
        if 'user' in fields:
            user_dict = \
                {
                    'links': {
                        'self': url_for(
                            'snetwork.blueprints.users.get_user',
                            user_id=post.user_id, _external=True),
                        'related': url_for(
                            'snetwork.blueprints.posts.get_post_relationship',
                            post_id=post.id, relationship='user',
                            _external=True)
                        },
                    'data': {'type': 'users', 'id': post.user_id}
                    }
            relationships.update(user=user_dict)
            post_dict.update(relationships=relationships)
        posts_dict_list.append(post_dict)
    response_dict = \
        {
            'data': posts_dict_list
        }
    response = jsonify(response_dict)
    response.mimetype = mimetype
    return response


@app.route('posts/<int:post_id>/relationships/<string:relationship>')
def get_post_relationship(post_id, relationship):
    return ''


@app.route('posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)
    response_dict = \
        {
            'data': {
                'type': 'posts',
                'id': post.id
            }
        }
    fields = request.args.get('fields[posts]', '').split(',')
    user_fields = request.args.get('fields[users]', '').split(',')
    picture_fields = request.args.get('fields[pictures]', '').split(',')
    includes = request.args.get('include', '')
    attributes = dict()
    relationships = dict()
    if 'message' in fields:
        attributes.update(dict(message=post.message))
    if 'created_at' in fields:
        attributes.update(dict(created_at=post.created_at.strftime('%Y-%m-%dT%H:%M:%Sz')))
    if attributes:
        response_dict['data']['attributes'] = attributes
    if 'user' in fields:
        user_dict = \
            {
                'links': {
                    'self': url_for(
                        'snetwork.blueprints.users.get_user',
                        user_id=post.user_id, _external=True),
                    'related': url_for(
                        'snetwork.blueprints.posts.get_post_relationship',
                        post_id=post.id, relationship='user',
                        _external=True)
                },
                'data': {'type': 'users', 'id': post.user_id}
            }
        relationships.update(user=user_dict)
        response_dict['data']['relationships'] = relationships
    response_dict['included'] = []
    if 'user' in includes:
        user_dict = \
            {
                'type': 'users',
                'id': post.user.id,
            }
    attributes = dict()

    if 'first_name' in user_fields:
        attributes.update(dict(first_name=post.user.first_name))
    if 'last_name' in user_fields:
        attributes.update(dict(last_name=post.user.last_name))
    if attributes:
        user_dict.update(dict(attributes=attributes))
    if 'picture' in user_fields:
        picture_dict = \
            {
                'type': 'pictures',
                'id': post.user.picture.id
            }

    if 'picture' in includes and post.user.picture:
        picture_dict = \
            {
                'type': 'pictures',
                'id': post.user.picture.id
            }
        picture_attributes = dict()
        if 'url' in picture_fields:
            picture_url = url_for('snetwork.blueprints.pictures.show_picture',
                                  picture_id=post.user.picture.id,
                                  _external=True)
            picture_attributes.update(dict(url=picture_url))
        if picture_attributes:
            picture_dict.update(dict(attributes=picture_attributes))
        response_dict['included'].append(dict(data=picture_dict))
    response_dict['included'].append(dict(data=user_dict))

    response = jsonify(response_dict)
    response.mimetype = mimetype
    return response
