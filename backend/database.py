from sqlalchemy import create_engine  # conexiune DB
from sqlalchemy.orm import sessionmaker, declarative_base

# foloseste SQLite, fisierul DB este tasks.db in folderul curent
DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(  # motorul care stie sa vorbeasca cu DB
    # connect_args : SQLite pe windows are o regula legata de Threads.
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(  # sesiune DB ( o conversatie cu DB ). Prin sesiuni se fac quiery-uri, insert-uri, updates etc
    autocommit=False, autoflush=False, bind=engine
)

# clasa de baza pentru modele. toate tabelele vor mosteni de aici
Base = declarative_base()
