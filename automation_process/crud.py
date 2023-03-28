from sqlalchemy.orm import Session
import models, schemas
import database
from database import SessionLocal
from schemas import User as _User
from schemas import Scan as _Scan
from schemas import Insole as _Insole
import datetime as dt

import processing

def create_database():
    #database.Base.metadata.drop_all()
    return database.Base.metadata.create_all(bind=database.engine)

def get_user(db: Session, skip: int=0, limit: int =100, user_id: int=None):
    #return db.query(models.User).filter(models.User.id == user_id).first()
    return db.query(models.User).offset(skip).limit(limit).all()

def get_users(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def get_user_by_surname(db: Session, surname: str):
    return db.query(models.User).filter(models.User.surname == surname).first()

def create_user(db: Session, user: schemas.User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()

def update_user(db: Session, user_id: int, user: schemas.User):
    db_user= get_users(db=db, user_id=user_id)
    if user.name!= "string":
        db_user.name = user.name
    if user.surname!= "string":
        db_user.surname = user.surname
    if user.email!= "string":
        db_user.email=user.email
    db.commit()
    db.refresh(db_user)
    return db_user

def get_scans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Scan).offset(skip).limit(limit).all()

def get_scan_by_user(db: Session, owner_id: int):
    return db.query(models.Scan).filter(models.Scan.owner_id == owner_id).first()

def get_scan_by_scan_id(db: Session, scan_id: int):
    return db.query(models.Scan).filter(models.Scan.id == scan_id).first()


def get_name_scan_by_id(db: Session, scan_id: int):
    return db.query(models.Scan).filter(models.Scan.id == scan_id).first()

def get_scan_by_date(db: Session, date: int):
    return db.query(models.Scan).filter(models.Scan.date_created == date).first()

def create_scan(db: Session, scan: schemas.Scan, owner_id: int):
    
    db_scan=models.Scan(scann=scan.scann, size=scan.size, unit_s=scan.unit_s,weight=scan.weight,unit_w=scan.unit_w, owner_id=owner_id)
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return db_scan

def delete_scan(db: Session, scan_id: int):
    db.query(models.Scan).filter(models.Scan.id == scan_id).delete()
    db.commit()

def update_scan(db: Session, scan_id: int, scan: schemas.Scan):
    db_user= get_scan_by_scan_id(db=db, scan_id=scan_id)
    # db_user.scann = scan.scann
    # db_user.type_scan = str(scan.scann)[-3:]
    if scan.size!=0:
        db_user.size=scan.size
    if scan.weight!=0:
        db_user.weight=scan.weight
    if scan.owner_id!=0:
        db_user.owner_id=scan.owner_id
    db_user.date_created=dt.date.today()
    db.commit()
    db.refresh(db_user)
    return db_user

def update_scanner(db: Session, scan_id: int, new_scan: str,scan: schemas.Scan):
    db_scan= get_scan_by_scan_id(db=db, scan_id=scan_id)
    db_scan.scann=str(new_scan)
    db_scan.type_scan=str(new_scan)[-3:]
    db.commit()
    db.refresh(db_scan)
    
    return db_scan


def create_insole(db: Session, insole: schemas.Insole,scan_id:int):
    db.add(insole)
    db.commit()
    db.refresh(insole)
    return insole

def get_insoles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Insole).offset(skip).limit(limit).all()

def get_insoles_by_scan_id(db:Session, scan_id:int):
    #return db.query(models.Insole).filter(models.Scan.id == scan_id).first()
    return db.query(models.Insole).join(models.Scan).filter(models.Scan.id == scan_id).first()

def delete_insole(db: Session, id: int):
    db.query(models.Insole).filter(models.Insole.id == id).delete()
    db.commit()