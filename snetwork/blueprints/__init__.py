from . import users, posts, pictures

active = (('/api/', users.app),
          ('/api/', posts.app),
          ('/', pictures.app)
          )
