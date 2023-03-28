from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import crud, models, schemas
from models import User, Scan, Insole
import database
from database import SessionLocal, engine
from typing import List
import pandas as pd
import os
import uuid
import processing

app = FastAPI()

crud.create_database()
@app.get("/")
async def root():
    return {"message": "Hello World"}

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/users',response_model=schemas.User)
def add_user(name:str, surname:str, email:str, db: Session = Depends(get_db)):
    user = models.User(name,surname,email)
    
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_user(skip: int = 0, limit: int = 100,db: Session = Depends(get_db)):
    users = crud.get_user(db=db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_users(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db=db, user_id=user_id)
    return {"message": f"successfully deleted post with id: {user_id}"}

@app.put("/user/{user_id}", response_model=schemas.User)
def update_user(user_id: int,user: schemas.User, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user=user, user_id=user_id)

@app.post('/scan',response_model=schemas.Scan)
def add_scan(scann:UploadFile, size:str, unit_s:str, weight:str,unit_w:str, owner_id:int,db: Session = Depends(get_db)):
    new_name=str(uuid.uuid4())+"."+str(scann.filename)[-3:]
    print(new_name)
    path=f'./uploaded_scan/{scann.filename}'
    print(path)
    if os.path.isfile(path)==False:
        print("The file already exists")
        with open(f'./uploaded_scan/{scann.filename}', 'wb') as f:
            f.write(scann.file.read())
        scan = models.Scan(f'./uploaded_scan/{scann.filename}',size,unit_s,weight,unit_w,owner_id)
    
    else:
    # Rename the file
        with open(f'./uploaded_scan/{new_name}', 'wb') as f:
            f.write(scann.file.read())
        scan = models.Scan(f'./uploaded_scan/{new_name}',size,unit_s,weight,unit_w,owner_id)
    
    return crud.create_scan(db=db, scan=scan,owner_id=owner_id)

@app.get("/scan/", response_model=List[schemas.Scan])
def read_scan(skip: int = 0, limit: int = 100,db: Session = Depends(get_db)):
    users = crud.get_scans(db=db, skip=skip, limit=limit)
    return users

@app.get("/scan/{user_id}", response_model=schemas.Scan)
def read_scan_by_user_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_scan_by_user(db, owner_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    return db_user

@app.get("/scans/{scan_id}", response_model=schemas.Scan)
def read_scan_by_scan_id(scan_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_scan_by_scan_id(db=db, scan_id=scan_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    return db_user

@app.delete("/scan/{scan_id}")
def delete_user(scan_id: int, db: Session = Depends(get_db)):
    crud.delete_scan(db=db, scan_id=scan_id)
    return {"message": f"successfully deleted scan with id: {scan_id}"}

@app.put("/scans/{scan_id}", response_model=schemas.Scan)
def update_scanner(scan_id: int, new_scan: UploadFile,db: Session = Depends(get_db)):
    new_name=str(uuid.uuid4())+"."+str(new_scan.filename)[-3:]
    print(new_name)
    path=f'./uploaded_scan/{new_scan.filename}'
    print(path)
    if os.path.isfile(path)==False:
        print("The file already exists")
        with open(f'./uploaded_scan/{new_scan.filename}', 'wb') as f:
            f.write(new_scan.file.read())
        scan=crud.get_scan_by_scan_id(db=db,scan_id=scan_id)
        return crud.update_scanner(db=db,scan_id=scan_id, new_scan=new_scan, scan=scan)
        
    else:
    # Rename the file
        with open(f'./uploaded_scan/{new_name}', 'wb') as f:
            f.write(new_scan.file.read())
        scan=crud.get_scan_by_scan_id(db=db,scan_id=scan_id)
        return crud.update_scanner(db=db,scan_id=scan_id, new_scan=new_name, scan=scan)
    

@app.put("/scan/{scan_id}", response_model=schemas.Scan)
def update_scan(scan_id: int,scan: schemas.Scan, db: Session = Depends(get_db)):
    return crud.update_scan(db=db, scan=scan, scan_id=scan_id)

# @app.post("/insole/{insole_id}",response_model=schemas.Insole)
# def upload_modelisation(mode: UploadFile, scan_id: int,)
@app.get("/insole/", response_model=List[schemas.Scan])
def read_scan(skip: int = 0, limit: int = 100,db: Session = Depends(get_db)):
    insole = crud.get_insoles(db=db, skip=skip, limit=limit)
    return insole

@app.delete("/insole/{scan_id}")
def delete_user(insole_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_insole(db=db, id=insole_id)
        return {"message": f"successfully deleted scan with id: {insole_id}"}
    except:
        return{"No insole to delete"}



get_db()


processing.process()
