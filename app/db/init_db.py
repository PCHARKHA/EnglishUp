# app/db/init_db.py
from app.db.session import engine
from app.db.base import Base

# Import ALL models so SQLAlchemy registers them
from app.models.user import User
from app.models.prompt import Prompt
from app.models.transcripts import Transcript
from app.models.attempt import Attempt
from app.models.score import Score

def init_db():
    """
    Creates all tables in the database.
    """
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")

if __name__ == "__main__":
    init_db()

