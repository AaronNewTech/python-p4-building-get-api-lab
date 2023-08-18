from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'

    # this definition makes fixes the recusion error when working with database relationships, syntax tablename from the other class, class
    serialize_rules = ('-baked_goods.bakery',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Establish the one-to-many relationship between Bakery and BakedGood
    baked_goods = db.relationship('BakedGood', back_populates='bakery')

class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'

    # this definition makes fixes the recusion error when working with database relationships, syntax tablename from the other class, class
    serialize_rules = ('-bakeries, bakedgood',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Establish the relationship back to Bakery
    bakery = db.relationship('Bakery', back_populates='baked_goods')
