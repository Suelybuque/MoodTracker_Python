from sqlalchemy import create_engine, Column, Integer, String, Date, Text, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import DateTime
from datetime import datetime
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.environ.get("MOOD_DB_PATH", os.path.join(PROJECT_ROOT, "data", "mood_data.db"))
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


class MoodDB:

    """
    Simple SQLite wrapper using SQLALchemy Core.
    -Initialize the DB and table
    -insert records
    -query ranges
    -return results as panda lists/dicts
    """

    def __init__(self, db_path: str = DB_PATH):
        self.engine = create_engine(f"sqlite:///{db_path}", echo = False, future = True)
        self.metadata = MetaData()
        self.table = Table(
            'mood', self.metadata,
            Column('id', Integer, primary_key = True, autoincrement = True),
            Column('date', DateTime, nullable=False),
            Column('mood', Integer, nullable = False),
            Column('energy', Integer, nullable = False),
            Column('stress', Integer, nullable = False),
            Column('notes', Text, nullable = True),
        )
        self.metadata.create_all(self.engine)
        self.Session = sessionmaker (bind = self.engine)

    def insert(self, date_value: datetime, mood: int, energy: int, stress: int, notes: str = ""):
        with self.engine.begin() as conn :
            conn.execute(self.table.insert().values(
                date= date_value,
                mood= mood,
                energy= energy,
                stress= stress,
                notes = notes
            ))

    def fetch_all(self):
        with self.engine.connect() as conn:
            res = conn.execute(
                self.table.select().order_by(self.table.c.date.desc())
            )
            return [dict(r._mapping) for r in res]

    def fetch_range( self, start_date, end_date):
        with self.engine.connect() as conn:
            q = self.table.select().where(self.table.c.date.between(start_date, end_date)).order_by(self.table.c.date)
            res = conn.execute(q)
            return [dict (r) for r in res]
