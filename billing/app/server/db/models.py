# ------- local imports -------
from .extensions import db

# ------- 3rd party imports -------
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship


class Provider(db.Model):
    __tablename__ = 'provider'
    id = Column(Integer, primary_key=True)

    name = Column(String(16), unique=True)

    rates = relationship("Rate", backref="provider")
    trucks = relationship("Truck", backref="provider")

    def __repr__(self):
        return f'PROVIDER id: {self.id}\nname: {self.name}\nrates: {self.rates}'


class Rate(db.Model):
    __tablename__ = 'rate'
    id = Column(Integer, primary_key=True)

    product_id = Column(String(50))
    rate = Column(Integer)
    scope = Column(String(50))

    provider_id = Column(Integer, ForeignKey('provider.id'))

    def __repr__(self):
        return f'RATE prod id: {self.id} rate: {self.rate} scope: {self.scope}'


class Truck(db.Model):
    __tablename__ = 'truck'
    id = Column(Integer, primary_key=True)

    truck_id = Column(String(50))

    provider_id = Column(Integer, ForeignKey('provider.id'))

    def __repr__(self):
        return f'provider: {self.provider_id}'


class HealthCheck(db.Model):
    __tablename__ = 'HealthCheck'
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f'health check {self.id}'
