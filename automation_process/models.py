import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm

import database as _database
import datetime as dt

class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name= _sql.Column(_sql.String)
    surname= _sql.Column(_sql.String)
    email = _sql.Column(_sql.String)

    scans = _orm.relationship("Scan", back_populates="owner")

    def __init__(self, name, surname, email):
        self.name=name
        self.surname=surname
        self.email=email
    

class Scan(_database.Base):
    __tablename__ = "scan"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    scann= _sql.Column(_sql.String, index=True)
    type_scan = _sql.Column(_sql.String)
    size = _sql.Column(_sql.Float, index=True)
    unit_s= _sql.Column(_sql.String, index=True)
    weight= _sql.Column(_sql.Integer, index=True)
    unit_w= _sql.Column(_sql.String)

    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    owner = _orm.relationship("User", back_populates="scans")
    insoles = _orm.relationship("Insole", back_populates="scanner")

    def __init__(self,scann,size,unit_s,weight,unit_w,owner_id):
        self.scann=scann
        self.type_scan=str(scann)[-3:]
        self.size=size
        self.unit_s=unit_s
        self.weight=weight
        self.unit_w=unit_w
        self.owner_id=owner_id
        self.date_created=dt.date.today()
        #date_created=today.strftime("%d/%m/%Y")

class Insole(_database.Base):
    __tablename__="insole"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    data =_sql.Column(_sql.String, index=True)
    data_gcode=_sql.Column(_sql.String, index=True)
    data_stl= _sql.Column(_sql.String, index=True)

    scanner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("scan.id"))

    scanner = _orm.relationship("Scan", back_populates="insoles")

    def __init__(self,data,scanner_id):
        self.data=data
        self.scanner_id=scanner_id
        self.data_gcode=None
        self.data_stl=None

