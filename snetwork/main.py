from snetwork.core import app, login_manager, cache, oauth
from snetwork.models import *
from snetwork.blueprints import active
from datetime import datetime, timedelta
from flask_login import current_user


for url, blueprint in active:
    app.register_blueprint(blueprint, url_prefix=url)


@login_manager.user_loader
def load_user(user_id):
    app.logger.debug(user_id)
    return User.query.filter(User.username == user_id).first()


@login_manager.request_loader
def request_loader(request):
    pass


@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


@oauth.grantgetter
def load_grant(client_id, code):
    return cache.get('snetwork_grant_'+str(client_id)+'_'+str(code))


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    expires = datetime.utcnow + timedelta(seconds=100)
    grant = Grant(client_id,
                  code=code['code'],
                  redirect_uri=request.redirect_uri,
                  _scopes=' '.join(request.scopes),
                  user=current_user,
                  expires=expires)
    cache.set('snetwork_grant_'+str(client_id)+'_'+str(code), timeout=100)
    return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(client_id=request.client.client_id,
                                 user_id=request.user.id)
    for t in toks:
        db.session.delete(t)
    expires_in = token.get('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)
    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
        )
    db.session.add(tok)
    db.session.commit()
    return tok


@oauth.usergetter
def get_user(username, password, *args, **kwargs):
    user = User.query.filter_by(username=username).first()
    app.logger.debug(user.password)
    db.session.commit()
    if user and user.is_correct_password(password):
        return user
    return None


if __name__ == '__main__':
    app.run()
    app.db.create_all()
