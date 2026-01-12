from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
# din scrip schemas.py, am importat clasa TaskCreate, care e un sablon. cand se creeaza un task, trebuie sa se trimita JSON cu title (string). FastAPI vlideaza automat
from schemas import TaskCreate, TaskUpdate

from database import engine, SessionLocal
from models import Base, Task
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()  # creare aplicatie
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# creaza tabele in DB daca nu exista deja
Base.metadata.create_all(bind=engine)


def get_db():  # creeaza o sesiune DB
    db = SessionLocal()
    try:
        yield db  # FastAPI ia aceasta sesiune si o da endpoint-ului
    finally:
        db.close()  # indiferent de ce se intampla, se inchide sesiunea (curat)


@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()  # to receive all of the rows from tasks tabel

# creeaza tabelul la pornire
# defineste o sesiune DB
# endpoint GET/ tasks


@app.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(title=task.title, completed=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"deleted": task_id}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = payload.completed
    db.commit()
    db.refresh(task)

    return task
