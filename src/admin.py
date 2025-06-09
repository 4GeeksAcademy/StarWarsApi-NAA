#archivo admin va a servir para importar modelos y que se vean en la plataforma dinámica
import os
from flask_admin import Admin
from models import db, User, Character, Planets, Fav_character, Fav_planets
from flask_admin.contrib.sqla import ModelView


class FavCharacterAdmin(ModelView):
    form_columns = ['user', 'character']

class FavPlanetAdmin(ModelView):
    form_columns = ['user', 'planet']

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(FavCharacterAdmin(Fav_character, db.session))
    admin.add_view(FavPlanetAdmin(Fav_planets, db.session))

