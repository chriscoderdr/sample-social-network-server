from flask import Blueprint, send_file

app = Blueprint('snetwork.blueprints.pictures', __name__)


@app.route('picture/<int:picture_id>')
def show_picture(picture_id):
    return send_file('static/test.jpg', mimetype='image/png')
