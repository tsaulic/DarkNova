from enum import Enum

from core import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    ship_name = db.Column(db.String(32), unique=False, nullable=False)
    turns = db.Column(db.Integer, unique=False, nullable=False)
    sector = db.relationship('Sector', backref=db.backref('players', lazy=True))
    sector_key = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=False)
    planets_key = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'ship_name': self.ship_name,
            'sector': self.sector.serialize(),
            'planets': self.planets.serialize()
        }

    def __repr__(self):
        return '<Player %r aboard %r>' % (self.username, self.ship_name)


class Sector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    beacon = db.Column(db.String, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'links': [link.to for link in self.links],
            'players': [player.username for player in self.players],
            'planets': [planet.name for planet in self.planets],
            'ports': [PortType(port.id).name for port in self.ports]
        }

    def __repr__(self):
        return '<Sector %r with players: %r>' % (self.name, self.players)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to = db.Column(db.Integer, unique=False, nullable=False)
    sector_key = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=False)
    sector = db.relationship('Sector', backref=db.backref('links', lazy=True))

    def serialize(self):
        return {
            'id': self.id,
            'sector': self.sector.id,
        }

    def __repr__(self):
        return '<Link to %r in sector: %r' % (self.to, self.sector)


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    sector_key = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=False)
    sector = db.relationship('Sector', backref=db.backref('planets', lazy=True))
    owner = db.Column(db.Integer, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'sector': self.sector.id,
            'owner': self.owner
        }

    def __repr__(self):
        return '<Planet %r in sector: %r owned by: %r>' % (self.name, self.sector, self.owner)


class Port(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    sector_key = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=False)
    sector = db.relationship('Sector', backref=db.backref('ports', lazy=True))

    def serialize(self):
        return {
            'id': self.id,
            'type': PortType(self.type).name,
            'sector': self.sector.id,
        }

    def __repr__(self):
        return '<%r port in sector: %r>' % (PortType(self.type).name, self.sector)


class PortType(Enum):
    SPECIAL = 0
    ENERGY = 1
    ORGANICS = 2
    GOODS = 3
    ORE = 4
