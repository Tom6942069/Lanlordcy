import socket
import threading
import json
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database Setup
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    building_number = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True)
    building_number = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    id_manager = Column(Integer, ForeignKey('users.id'), nullable=False)
    manager = relationship('User', backref='managed_buildings')

engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_user(username, password, building_number, is_admin):
    if session.query(User).filter_by(username=username).first():
        return "Error: Username already exists."
    new_user = User(username=username, password=password, building_number=building_number, is_admin=is_admin)
    session.add(new_user)
    session.commit()
    return "User registered successfully."

def user_exists(username, password):
    user = session.query(User).filter_by(username=username, password=password).first()
    if user:
        if user.is_admin:
            # Fetch list of buildings managed by the admin
            buildings = session.query(Building).filter_by(id_manager=user.id).all()
            building_list = [{"id": b.id, "building_number": b.building_number, "description": b.description} for b in buildings]
            return {"role": "ADMIN", "buildings": building_list}
        return {"role": "TENANT"}
    return {"role": "INVALID"}

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # Parse the received JSON data
            try:
                request = json.loads(data)
            except json.JSONDecodeError:
                client_socket.send(json.dumps({"error": "Invalid JSON format"}).encode())
                continue

            action = request.get("action")

            if action == "register":
                username = request.get("username")
                password = request.get("password")
                building_number = request.get("building_number")
                is_admin = request.get("is_admin", False)

                if not all([username, password, building_number]):
                    client_socket.send(json.dumps({"error": "Missing fields in registration data"}).encode())
                    continue

                response = add_user(username, password, building_number, is_admin)
                client_socket.send(json.dumps({"message": response}).encode())

            elif action == "login":
                username = request.get("username")
                password = request.get("password")

                if not all([username, password]):
                    client_socket.send(json.dumps({"error": "Missing username or password"}).encode())
                    continue

                response = user_exists(username, password)
                client_socket.send(json.dumps(response).encode())

            else:
                client_socket.send(json.dumps({"error": "Unknown action"}).encode())

        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)
    print("Server is running on port 8080")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    server()
