from core import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    ship_name = db.Column(db.String(32), unique=True, nullable=False)
    sector = db.relationship('Sector', backref=db.backref('players', lazy=True))
    sector_key = db.Column(db.Integer, db.ForeignKey('sector.id'), unique=False, nullable=False)
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

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'players': [player.username for player in self.players],
            'planets': [planet.name for planet in self.planets]
        }

    def __repr__(self):
        return '<Sector %r with players: %r>' % (self.name, self.players)


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=False)
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