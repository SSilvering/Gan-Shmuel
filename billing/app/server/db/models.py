# ------- local imports -------
from .extensions import db

# ------- 3rd party imports -------
from sqlalchemy import Integer, ForeignKey, String, Column, Float, UniqueConstraint
from sqlalchemy.orm import relationship


class Provider(db.Model):
    __tablename__ = 'provider'
    id = Column(Integer, primary_key=True)

    name = Column(String(50), unique=True)

    trucks = relationship("Truck", backref="provider")
    rates = relationship("Rate", backref="provider")

    def __repr__(self):
        return f'PROVIDER id: {self.id}\nname: {self.name}\nrates: {self.rates}'


class Rate(db.Model):
    __tablename__ = 'rate'
    __table_args__ = (UniqueConstraint('product_name', 'scope'),)
    # id = Column(Integer, primary_key=True)
    
    product_name = Column(String(50),  primary_key=True)
    rate = Column(Integer)
    scope = Column(Integer, ForeignKey('provider.id'))
     

    def __repr__(self):
        return f'RATE product_name: {self.product_name} rate: {self.rate} scope: {self.scope}'

class Truck(db.Model):
    __tablename__ = 'truck'
    id = Column(Integer, primary_key=True)

    truck_id = Column(String(50), unique=True)
    weight = Column(Float)
    unit = Column(String(50))

    provider_id = Column(Integer, ForeignKey('provider.id'))

    def __repr__(self):
        return f'truck_id: {self.track_id} belongs_to: {self.provider_id}'


class HealthCheck(db.Model):
    __tablename__ = 'HealthCheck'
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f'health check {self.id}'
