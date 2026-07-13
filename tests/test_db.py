from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


TEST_DB_URL = 'postgresql+psycopg2://vladislavponomaryov:donat6321@localhost:5432/marketplace_db_tests'
test_engine = create_engine(TEST_DB_URL)
TestSessionLocal = sessionmaker(bind=test_engine)

Base = declarative_base()

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()