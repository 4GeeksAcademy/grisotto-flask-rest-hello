from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": [favorite.serialize() for favorite in self.favorites]
        }



class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(80), unique=True)
    gender: Mapped[str] = mapped_column(nullable=True)
    skin_color: Mapped[str] = mapped_column(nullable=True)
    hair_color: Mapped[str] = mapped_column(nullable=True)
    height: Mapped[str] = mapped_column(nullable=True)
    eye_color: Mapped[str] = mapped_column(nullable=True)
    mass: Mapped[str] = mapped_column(nullable=True)
    homeworld: Mapped[str] = mapped_column(nullable=True)
    birth_year: Mapped[str] = mapped_column(nullable=True)
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "height": self.height,
            "eye_color": self.eye_color,
            "mass": self.mass,
            "homeworld": self.homeworld,
            "birth_year": self.birth_year,
            

        }



class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False)
    
    climate: Mapped[str] = mapped_column(nullable=True)
    surface_water: Mapped[str] = mapped_column(nullable=True)
    diameter: Mapped[str] = mapped_column(nullable=True)
    rotation_period: Mapped[str] = mapped_column(nullable=True)
    gravity: Mapped[str] = mapped_column(nullable=True)
    orbital_period: Mapped[str] = mapped_column(nullable=True)
    population: Mapped[int] = mapped_column(nullable=True)
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "surface_water": self.surface_water,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population,
            
        }

class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=False)
    
    user: Mapped["User"] = relationship(back_populates="favorites")
    planet: Mapped["Planet | None"] = relationship(back_populates="favorites")
    character: Mapped["Character | None"] = relationship(back_populates="favorites")





