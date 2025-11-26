from database import Base, engine
import model
# Create the tables in the database
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")