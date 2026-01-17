from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1️⃣ Database URL (SQLite for MVP)
SQLALCHEMY_DATABASE_URL = "sqlite:///./englishup.db"  # this will create englishup.db in project root

# 2️⃣ Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # required for SQLite
)

# 3️⃣ Create SessionLocal class for DB sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 4️⃣ Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
