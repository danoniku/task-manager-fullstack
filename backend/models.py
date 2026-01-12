from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Task(Base):  # clasa Task, clasa Python
    __tablename__ = "tasks"  # definirea tabelei tasks, numle tabelului in SQLite

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)
