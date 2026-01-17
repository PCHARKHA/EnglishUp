from app.db.session import engine
from app.db.base import Base

# Import all models here to ensure tables are registered
from app.models.user import User
from app.models.prompt import Prompt
from app.models.transcripts import Transcript 

def init_db():
    """
    Creates all tables in the database.
    All models must be imported above before calling this function.
    """
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")

if __name__ == "__main__":
    init_db()

