from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///users.db')
Session = sessionmaker(bind=engine)
session = Session()

class Building(Base):
    __tablename__ = 'buildings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    building_number = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    id_manager = Column(Integer, ForeignKey('users.id'), nullable=False)

# Table Definitions
class Apartment(Base):
    __tablename__ = 'apartments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    building_id = Column(Integer, ForeignKey('buildings.id'), nullable=False)
    tenant_details = Column(Text, nullable=False)

class Problem(Base):
    __tablename__ = 'problems'
    id = Column(Integer, primary_key=True, autoincrement=True)
    apartment_id = Column(Integer, ForeignKey('apartments.id'), nullable=False)
    problem_type_code = Column(Integer, ForeignKey('problem_types.id'), nullable=False)
    status_code = Column(Integer, ForeignKey('statuses.id'), nullable=False)
    description = Column(String, nullable=True)

class ProblemType(Base):
    __tablename__ = 'problem_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)

class Status(Base):
    __tablename__ = 'statuses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)

# Create all tables
Base.metadata.create_all(engine)

# Insert Initial Data
# Problem Types
def populate_problem_types():
    problem_types = [
        "Leaking roof",
        "Broken heater",
        "Plumbing issue",
        "Window repair",
        "Elevator malfunction",
        "Parking problem",
        "OTHER"
    ]
    for description in problem_types:
        session.add(ProblemType(description=description))
    session.commit()

# Statuses
def populate_statuses():
    statuses = ["Open", "In Progress", "Resolved"]
    for description in statuses:
        session.add(Status(description=description))
    session.commit()

# Example Data for Apartments
def populate_apartments():
    example_apartments = [
        {"building_id": 1, "tenant_details": "Tenant 1 details"},
        {"building_id": 1, "tenant_details": "Tenant 2 details"},
        {"building_id": 2, "tenant_details": "Tenant 3 details"},
        {"building_id": 3, "tenant_details": "Tenant 4 details"},
    ]
    for apartment in example_apartments:
        session.add(Apartment(**apartment))
    session.commit()

# Example Data for Problems
def populate_problems():
    example_problems = [
        {"apartment_id": 1, "problem_type_code": 1, "status_code": 1, "description":"blabla"},
        {"apartment_id": 2, "problem_type_code": 3, "status_code": 2, "description":"blabla"},
        {"apartment_id": 3, "problem_type_code": 5, "status_code": 1, "description":"blabla"},
        {"apartment_id": 4, "problem_type_code": 2, "status_code": 3, "description":"blabla"},
    ]
    for problem in example_problems:
        session.add(Problem(**problem))
    session.commit()

# Populate tables with initial data
# populate_problem_types()
# populate_statuses()
# populate_apartments()
populate_problems()

print("Database and tables have been created and populated successfully.")
