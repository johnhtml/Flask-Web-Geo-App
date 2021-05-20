from . import db # import from the current directory
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class WallDesign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    design_name = db.Column(db.String(150))
    gs = db.Column(db.Float(3))# materials unit weight
    gb = db.Column(db.Float(3))# soils unit weight
    phi = db.Column(db.Float(3))# soils friction angle
    bc = db.Column(db.Float(3))# bearing capacity
    bb = db.Column(db.Float(3))# base
    bh = db.Column(db.Float(3))# toe high
    p = db.Column(db.Float(3))# frontal toe length
    H = db.Column(db.Float(3))# Retaining wall total high
    B = db.Column(db.Float(3))# Wall thickness
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_on = db.Column(db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    wall_designs = db.relationship('WallDesign')
