from snetwork.models import *
from snetwork.core import app

app.db.drop_all()
app.db.reflect()
app.db.create_all()
user = User(first_name='Cristian', last_name='Gomez',
            username='cgomez', password='elcj2304')
app.logger.debug(user.password)
picture = Picture(user=user)
post = Post(user=user,
        message=("Es increíble como hay personas que prefieren irse a"
            " Estados Unidos a limpiar baños para vacacionar en RD, en"
            " vez de estudiar en RD para poder ir a EU a vacacionar."))
post2 = Post(user=user,
             message="Joder que incomodo es mi sofa despues de estar 12 horas tirado sobre el")
post3 = Post(user=user,
             message="For another thing, good nights !")
post4 = Post(user=user,
             message="I have noticed some people don't pay close enough attention.")
app.db.session.add(user)
app.db.session.add(picture)
app.db.session.add(post)
app.db.session.add(post2)
app.db.session.add(post3)
app.db.session.add(post4)
app.db.session.commit()
client = Client(client_secret='abc')
client.default_scopes = 'users'
client.redirect_uris = 'http://cristiangomez.me'
app.db.session.add(client)
app.db.session.commit()
