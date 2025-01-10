
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys
import random

# Set up SQLAlchemy database
Base = declarative_base()
engine = create_engine("sqlite:///users.db")
Session = sessionmaker(bind=engine)
session = Session()

# User table definition
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    building_number = Column(String, nullable=False)  # Store building number

# Building table definition
class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True)
    building_number = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

Base.metadata.create_all(engine)

# Functions to manage users and buildings
def user_exists(username):
    return session.query(User).filter_by(username=username).first() is not None

def add_user(username, password, building_number, is_admin=False):
    if user_exists(username):
        return "Error: Username already exists."
    new_user = User(username=username, password=password, building_number=building_number, is_admin=is_admin)
    session.add(new_user)
    session.commit()
    return "User added successfully."

def add_building(building_number, description=None):
    if session.query(Building).filter_by(building_number=building_number).first():
        return "Error: Building already exists."
    new_building = Building(building_number=building_number, description=description)
    session.add(new_building)
    session.commit()
    return "Building added successfully."

# # Building Window for Admins
# class BuildingWindow(QMainWindow):
#     def __init__(self, username, building_number):
#         super().__init__()
#         self.setWindowTitle(f"Building {building_number} - Admin Interface")
#         self.resize(400, 400)
#         layout = QGridLayout()
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#         self.problems = [
#             "Leaking roof",
#             "Broken heater",
#             "Plumbing issue",
#             "Window repair",
#             "Elevator malfunction",
#             "Parking problem"
#         ]
#         self.red_windows = random.sample(range(1, 10), 3)
#         self.buttons = []
#         for i in range(1, 10):
#             button = QPushButton(str(i))
#             button.setStyleSheet("background-color: white;")
#             button.clicked.connect(lambda _, b=i: self.on_window_click(b))
#             self.buttons.append(button)
#             layout.addWidget(button, (i-1)//3, (i-1)%3)
#         for i in self.red_windows:
#             self.buttons[i-1].setStyleSheet("background-color: red; color: white;")
#         central_widget.setLayout(layout)

#     def on_window_click(self, window_num):
#         if window_num in self.red_windows:
#             self.show_problems_dialog()
#         else:
#             QMessageBox.information(self, "Window", f"Window {window_num} is empty.")

#     def show_problems_dialog(self):
#         dialog = QDialog(self)
#         dialog.setWindowTitle("Landlord Problems")
#         layout = QVBoxLayout()

#         self.checkboxes = []
#         for problem in self.problems:
#             checkbox = QCheckBox(problem)
#             self.checkboxes.append(checkbox)
#             layout.addWidget(checkbox)

#         button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
#         button_box.accepted.connect(dialog.accept)
#         layout.addWidget(button_box)

#         dialog.setLayout(layout)
#         dialog.exec()

# # Main Application Window
# class LoginWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Login")
#         self.resize(400, 350)
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout()
#         self.username_input = QLineEdit()
#         self.password_input = QLineEdit()
#         self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
#         self.building_number_input = QLineEdit()
#         self.login_button = QPushButton("Login")
#         self.login_button.clicked.connect(self.validate_login)
#         self.register_button = QPushButton("Register")
#         self.register_button.clicked.connect(self.show_register_dialog)
#         self.error_label = QLabel("")
#         self.error_label.setStyleSheet("color: red;")
#         layout.addWidget(QLabel("Username:"))
#         layout.addWidget(self.username_input)
#         layout.addWidget(QLabel("Password:"))
#         layout.addWidget(self.password_input)
#         layout.addWidget(QLabel("Building Number:"))
#         layout.addWidget(self.building_number_input)
#         layout.addWidget(self.login_button)
#         layout.addWidget(self.register_button)
#         layout.addWidget(self.error_label)
#         central_widget.setLayout(layout)

#     def validate_login(self):
#         username = self.username_input.text()
#         password = self.password_input.text()
#         building_number = self.building_number_input.text()
#         user = session.query(User).filter_by(username=username, password=password, building_number=building_number).first()
#         if user:
#             if user.is_admin:
#                 QMessageBox.information(self, "Welcome", f"Welcome, Admin {username}!")
#                 self.open_building_window(username, building_number)
#             else:
#                 QMessageBox.information(self, "Welcome", "Welcome, User! Have a great day.")
#         else:
#             self.error_label.setText("Invalid username, password, or building number.")

#     def show_register_dialog(self):
#         dialog = RegisterDialog()
#         dialog.exec()

#     def open_building_window(self, username, building_number):
#         self.building_window = BuildingWindow(username, building_number)
#         self.building_window.show()
#         self.close()

# # Registration Dialog
# class RegisterDialog(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Register")
#         self.resize(300, 240)
#         layout = QFormLayout()
#         self.username_input = QLineEdit()
#         self.password_input = QLineEdit()
#         self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
#         self.building_number_input = QLineEdit()
#         self.is_admin_checkbox = QCheckBox("Is Admin")
#         layout.addRow("Username:", self.username_input)
#         layout.addRow("Password:", self.password_input)
#         layout.addRow("Building Number:", self.building_number_input)
#         layout.addRow("", self.is_admin_checkbox)
#         button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
#         button_box.accepted.connect(self.register_user)
#         button_box.rejected.connect(self.reject)
#         layout.addWidget(button_box)
#         self.setLayout(layout)

#     def register_user(self):
#         username = self.username_input.text()
#         password = self.password_input.text()
#         building_number = self.building_number_input.text()
#         is_admin = self.is_admin_checkbox.isChecked()
#         if not username or not password or not building_number:
#             QMessageBox.warning(self, "Error", "All fields are required.")
#             return
#         result = add_user(username, password, building_number, is_admin)
#         if "Error" in result:
#             QMessageBox.warning(self, "Error", result)
#         else:
#             QMessageBox.information(self, "Success", result)
#             self.accept()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = LoginWindow()
#     window.show()
#     sys.exit(app.exec())
