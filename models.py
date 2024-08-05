from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

# Define the base class for SQLAlchemy models
Base = declarative_base()

# Define the ChatHistory model with the specified column order
class ChatHistory(Base):
    __tablename__ = 'chat_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # Unique identifier for each record
    user_id = Column(Integer, default=1, nullable=False)        # New column with default value of 1
    role = Column(String, nullable=False)                        # Role of the person or entity sending the message
    message = Column(String, nullable=False)                     # Text of the message

# Set up the database URL (for SQLite in this case)
DATABASE_URL = 'sqlite:///chat_history.db'  # Update the path if necessary

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create the session factory
Session = sessionmaker(bind=engine)

# Create the tables in the database (if they don't exist)
def create_tables():
    Base.metadata.create_all(engine)

# Optional: Call this function to create tables when needed
if __name__ == "__main__":
    create_tables()
