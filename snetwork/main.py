from snetwork.core import app, login_manager
from snetwork.models import User
from snetwork.blueprints import active

for url, blueprint in active:
    app.register_blueprint(blueprint, url_prefix=url)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.username == user_id).first()


@login_manager.request_loader
def request_loader(request):
    pass


if __name__ == '__main__':
    app.run()
    app.db.create_all()
