from sqlalchemy import create_engine, MetaData

# Set up the database engine
engine = create_engine('sqlite:///users.db')
metadata = MetaData()

# Reflect the existing database
metadata.reflect(bind=engine)

# Drop the `buildings` table if it exists
if "problems" in metadata.tables:
    metadata.tables["problems"].drop(engine)
    print("problems table dropped.")

# Recreate all tables
from server import Base  # Replace with your actual server code file name
Base.metadata.create_all(engine)
print("problems table recreated.")
