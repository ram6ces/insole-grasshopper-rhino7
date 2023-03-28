#from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
import crud, models, schemas
from models import User, Scan, Insole
import database
from database import SessionLocal, engine
from typing import List
import pandas as pd
import os
import uuid
import time
from PIL import Image,ImageEnhance
import cv2 as cv
from database import SessionLocal, engine
from sqlalchemy.exc import NoResultFound
import traceback

def image_processing(scan_id, db):
    path=None
    try:
        scan=crud.get_scan_by_scan_id(db=db,scan_id=scan_id)
        #print(scan.scann)
        img = Image.open(scan.scann)
        img.show()
        if scan.type_scan=="png":
            img=img.convert("RGB")
        scan_processed=img.convert("L")
        new_name=str(uuid.uuid4())+".jpg"
        #print(new_name)
        path=f'./scan_processed/{new_name}'
        scan_processed.save(path)
        print(path)


    except:
        print("Scan object doesn't exist")

    return path
    
        
    

def process():


    max_scan_id = SessionLocal().query(func.max(models.Scan.id)).scalar()
    print(max_scan_id)
    max_scan = SessionLocal().query(models.Scan).filter(models.Scan.id == max_scan_id).one()
    print(max_scan)
    max_insole_id = SessionLocal().query(func.max(models.Insole.id)).scalar()
    print(max_insole_id)
    try:
        max_insole = SessionLocal().query(models.Insole).filter(models.Insole.id == max_insole_id).one()
        print(max_insole)
    except NoResultFound:
        print('! No insole found')

    for scan_id in range(max_scan_id):
        try:
            if crud.get_insoles_by_scan_id(db=SessionLocal(), scan_id=scan_id) == None:
                scan_process=image_processing(scan_id, SessionLocal())
                insole = models.Insole(data=scan_process,scanner_id=scan_id)
                print(insole)
                #return crud.create_user(db=db, user=user)
                insole=crud.create_insole(db=SessionLocal(),insole=insole, scan_id=scan_id)
        
        except:
            traceback.print_exc()
            print(f"Image processing issue with scan: {scan_id}")

