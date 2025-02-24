from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_people = db.relationship('Favorite_people')
    favorite_planets = db.relationship('Favorite_planets')
    favorite_vehicles = db.relationship('Favorite_vehicles')
    
    def __repr__(self):
        return self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "email": self.email,
            "favorite_people": [fav.serialize() for fav in self.favorite_people],
            "favorite_planets": [fav.serialize() for fav in self.favorite_planets],
            "favorite_vehicles": [fav.serialize() for fav in self.favorite_vehicles]
            # do not serialize the password, its a security breach
            
        }
    

class Planets(db.Model):
    __tablename__='planets'
    id = db.Column(db.Integer, primary_key=True)
    climate = db.Column(db.String(250), nullable= True)
    created = db.Column(db.String(250), nullable= True)
    diameter = db.Column(db.String(250), nullable= True)
    edited = db.Column(db.String(250), nullable= True)
    films = db.Column(db.String(250), nullable= False)
    gravity = db.Column(db.String(250), nullable= True)
    name = db.Column(db.String(250), nullable= False)
    orbital_period = db.Column(db.String(250), nullable= True)
    population = db.Column(db.String(250), nullable= True)
   
    def __repr__(self):
        return f'{self.name}'

    def serialize(self):
        return {
            "id": self.id,
            'climate': self.climate,
            'created': self.created,
            'diameter': self.diameter,
            'edited': self.edited,
            'films': self.films,
            'gravity': self.gravity,
            'name': self.name,
            'orbital_period': self.orbital_period,
            'population': self.population,
        }
    
class People(db.Model):
    __tablename__='people'
    id = db.Column(db.Integer, primary_key=True)
    birth_year = db.Column(db.String(250), nullable= False)
    eye_color = db.Column(db.String(250), nullable= True)
    films = db.Column(db.String(250), nullable= True)
    gender = db.Column(db.String(250), nullable= False)
    hair_color = db.Column(db.String(250), nullable= True)
    height = db.Column(db.Integer, nullable= True)
    planet = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable= False)
    mass = db.Column(db.Integer, nullable= True)
    name = db.Column(db.String(250), nullable= False)
    homeworld = db.relationship('Planets', foreign_keys=[planet])


    def __repr__(self): 
        return f'{self.name}'


    def serialize(self):
        return {
            'id': self.id,
            'birth_year': self.birth_year,
            'eye_color': self.eye_color,
            'films': self.films,
            'gender': self.gender,
            'hair_color': self.hair_color,
            'height': self.height,
            'homeworld': self.planet,
            'mass': self.mass,
            'name': self.name
            
        }
    

class Vehicles(db.Model):
    __tablename__='vehicles'
    id = db.Column(db.Integer, primary_key=True)
    cargo_capacity = db.Column(db.Integer, nullable= False)
    name = db.Column(db.String(250), nullable= True)
    cost_in_credits = db.Column(db.Integer, nullable= False)
    created = db.Column(db.String(250), nullable= True)
    crew = db.Column(db.Integer, nullable= True)
    edited = db.Column(db.String(250), nullable= True)

    def __repr__(self):
            return f'{self.name}'


    def serialize(self):
            return {
            'id': self.id,
            'cargo_capacity': self.cargo_capacity,
            'name': self.name,
            'cost_in_credits': self.cost_in_credits,
            'created': self.created,
            'crew': self.crew,
            'edited': self.edited
            }

# class Favorite(db.Model):
#      __tablename__='favorite'
#      id = db.Column(db.Integer, primary_key=True)
#      user_favorite_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#      user = db.relationship('User')
     
#      people_favorite_id = db.Column(db.Integer, db.ForeignKey('favorite_people.people_id'), nullable=True)
#      people = db.relationship('Favorite_people', backref='favorite')
     
#      planets_favorite_id = db.Column(db.Integer, db.ForeignKey('favorite_planets.planet_id'), nullable=True)
#      planets = db.relationship('Favorite_planets', backref='favorite')
    
#      vehicles_favorite_id = db.Column(db.Integer, db.ForeignKey('favorite_vehicles.vehicle_id'), nullable=True)
#      vehicles = db.relationship('Favorite_vehicles', backref='favorite')

#      def serialize(self):
#          return {
#                "id" : self.id,
#                "user": self.user,
#                "people": [fav.serialize() for fav in self.people],
#                'vehicles':[fav.serialize() for fav in self.vehicles],
#                'planets':[fav.serialize() for fav in self.planets]
#           }

class Favorite_people(db.Model):
     __tablename__='favorite_people'
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
     user = db.relationship('User', foreign_keys=[user_id])
     people_id = db.Column(db.Integer, db.ForeignKey('people.id'), unique=True, nullable=False)
     people = db.relationship('People', foreign_keys=[people_id])

     def serialize(self):
          return {
               'id': self.id,
               'people': self.people.serialize()
               
          }

class Favorite_planets(db.Model):
     __tablename__='favorite_planets'
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
     user = db.relationship('User', foreign_keys=[user_id])
     planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
     planet = db.relationship('Planets', foreign_keys=[planet_id])

     def serialize(self):
          return {
               'id': self.id,
               'planet': self.planet.serialize()
               
          }

class Favorite_vehicles(db.Model):
     __tablename__='favorite_vehicles'
     id = db.Column(db.Integer, primary_key=True)
     vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), unique=True, nullable=False)
     vehicle = db.relationship('Vehicles', foreign_keys=[vehicle_id])
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
     user = db.relationship('User', foreign_keys=[user_id])
     
     def serialize(self):
          return {
               'id': self.id,
               'vehicle': self.vehicle.serialize()
          }
            