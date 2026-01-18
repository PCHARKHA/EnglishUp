# create_tables.py
from app.db.base import Base
from app.db.session import engine
from app.models.transcripts import Transcript
from app.models.user import User
from app.models.prompt import Prompt


# This will create all tables in the database if they don't exist
Base.metadata.create_all(bind=engine)
print("All tables created successfully.")
