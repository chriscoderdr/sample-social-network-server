from flask import (Blueprint, request, jsonify, current_app, url_for,
                   render_template)
from flask_login import login_user, login_required, current_user
from snetwork.models import User, Client, Post
from snetwork.core import oauth

app = Blueprint('snetwork.blueprints.users', __name__)
mimetype = 'application/vnd.api+json'


@app.route('user/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter(User.username == username).first()
    if (not user or not password) or user.password != password:
        return jsonify({'status': 'error', 'data': None,
                        'message': 'Error trying to log in'})
    login_user(user)
    return jsonify({'status': 'success', 'data': None,
                   'message': 'User has been logged in'})


@app.route('me/feed', methods=['POST'])
@oauth.require_oauth()
def new_post():
    message = request.form.get('message', None)
    if message:
        post = Post(message=message, user=request.oauth.user)
        current_app.db.session.add(post)
        current_app.db.session.commit()
        response_dict = \
            {
                'data': {
                    'type': 'posts',
                    'id': post.id,
                    'attributes': {
                    }

                }
            }
        response = jsonify(response_dict)
        response.mimetype = mimetype
        response.headers["Location"] = url_for(
            'snetwork.blueprints.posts.get_post',
            post_id=post.id)
        response.status_code = 201
        return response


@app.route('me', defaults={'user_id': None})
@app.route('<int:user_id>')
@oauth.require_oauth()
def get_user(user_id):
    if user_id is None:
        user = request.oauth.user
    else:
        user = User.query.get(user_id)
    fields = request.args.get('fields[users]', '').split(',')
    picture_fields = request.args.get('fields[pictures]', '').split(',')
    includes = request.args.get('include', '')
    included = []
    user_dict = \
        {
            'type': 'users',
            'id': str(user.id),
        }
    attributes = dict()

    if 'first_name' in fields:
        attributes.update(dict(first_name=user.first_name))
    if 'last_name' in fields:
        attributes.update(dict(last_name=user.last_name))
    if attributes:
        user_dict.update(dict(attributes=attributes))
    if 'picture' in fields:
        picture_dict = \
            {
                'type': 'pictures',
                'id': str(user.picture.id)
            }
        user_dict.update(dict(relationships=dict(picture=picture_dict)))

    if 'picture' in includes and user.picture:
        picture_dict = \
            {
                'type': 'pictures',
                'id': str(user.picture.id)
            }
        picture_attributes = dict()
        if 'url' in picture_fields:
            picture_url = url_for('snetwork.blueprints.pictures.show_picture',
                                  picture_id=user.picture.id, _external=True)
            picture_attributes.update(dict(url=picture_url))
        if picture_attributes:
            picture_dict.update(dict(attributes=picture_attributes))
        included.append(picture_dict)
    response_dict = \
        {
            'data': user_dict
        }
    if included:
        response_dict.update(dict(included=included))
    response = jsonify(response_dict)
    response.mimetype = mimetype
    return response


@app.route('oauth/authorize', methods=['GET', 'POST'])
@login_required
@oauth.authorize_handler
def authorize(*args, **kwargs):
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        current_app.logger.debug(kwargs)
        return ''
    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'


@app.route('oauth/token')
@oauth.token_handler
def access_token():
        return {'version': '0.1.0'}
