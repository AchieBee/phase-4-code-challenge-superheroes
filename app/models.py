from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Hero_Power = db.Table(
    'hero_powers',
    db.Column('hero_id', db.Integer, db.ForeignKey('heroes.id'), primary_key=True),
    db.Column('power_id', db.Integer, db.ForeignKey('powers.id'), primary_key=True),
    db.Column('created_at', db.DateTime, server_default=db.func.now()),
    db.Column('updated_at', db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
)

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    powers = db.relationship(
        'Power',
        secondary=Hero_Power,
        back_populates='heroes'
    )

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heroes = db.relationship(
        'Hero',
        secondary=Hero_Power,
        back_populates='powers'
    )
