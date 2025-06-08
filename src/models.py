from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorite_characters: Mapped[list['Fav_character']]= relationship(back_populates= 'user', cascade='all, delete-orphan')
    favorite_planets: Mapped[list['Fav_planets']] = relationship(back_populates = 'user', cascade='all, delete-orphan')


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "favorite_characters": [favorite.serialize() for favorite in self.favorite_characters],
            "favorite_planets": [favorite.serialize() for favorite in self.favorite_planets]


             # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    eye_color: Mapped[str] = mapped_column(String(120), nullable=False)
    favorite_by_links: Mapped['Fav_character']= relationship(back_populates= 'character', cascade='all, delete-orphan')


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "eye_color": self.eye_color,
        }


class Fav_character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'), nullable=False)
    user: Mapped['User']= relationship(back_populates= 'favorite_characters')
    character: Mapped['Character']= relationship(back_populates= 'favorite_by_links')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user.id,
            "character_id": self.character.id,
        } 


class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=False)
    terrain: Mapped[str] = mapped_column(String(120), nullable=False)
    favorite_by_links: Mapped['Fav_planets']= relationship(back_populates= 'planet', cascade='all, delete-orphan')


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain         
        }
    
class Fav_planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'), nullable=False)
    user: Mapped['User']= relationship(back_populates= 'favorite_planets')
    planet: Mapped['Planets']= relationship(back_populates= 'favorite_by_links') 
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user.id,
            "planet_id": self.planet.id,
        }

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)
#     is_active = db.Column(db.Boolean(), default=True)

#     favorite_characters = relationship("Fav_character", back_populates="user")
#     favorite_planets = relationship("Fav_planets", back_populates="user")

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             "is_active": self.is_active
#         }

# class Character(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120))
#     gender = db.Column(db.String(50))
#     eye_color = db.Column(db.String(50))

#     favorited_by = db.relationship('Fav_character', back_populates='character')

#     def serialize(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "gender": self.gender,
#             "eye_color": self.eye_color
#         }

# class Planets(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120))
#     climate = db.Column(db.String(120))
#     terrain = db.Column(db.String(120))

#     favorited_by = db.relationship('Fav_planets', backref='planet', lazy=True)

#     def serialize(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "climate": self.climate,
#             "terrain": self.terrain
#         }

# class Fav_character(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     character_id = db.Column(db.Integer, db.ForeignKey('character.id'))

#     user = relationship("User", back_populates="favorite_characters")
#     character = relationship("Character")

#     def serialize(self):
#         return {
#             "id": self.id,
#             "user_id": self.user_id,
#             "character_id": self.character_id
#         }

# class Fav_planets(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)

#     user = relationship("User", back_populates="favorite_planets")
#     planet = relationship("Planets")

#     def serialize(self):
#         return {
#             "id": self.id,
#             "user_id": self.user_id,
#             "planet_id": self.planet_id
#         }