from datetime import date
from pipeline.db import MoodDB

def collect_and_store(mood: int, energy: int, stress: int, notes: str= ""):
    """Collects today's values and stores tem in the DB."""
    db= MoodDB()
    db.insert(date.today(), mood, energy, stress, notes)
    return True

#Seed demo data
def seed_demo_data(rows= 14):
    import random
    from datetime import  timedelta
    db= MoodDB()
    today = date.today()
    for i in range(rows):
        d= today - timedelta(days=i)
        db.insert(d, random.randit(1,5), random.randint(1, 5), random.randint(1, 5), f"Demo note{i}")
        return True