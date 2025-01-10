import sys
import socket
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QCheckBox, QMessageBox, QDialog, QFormLayout, QDialogButtonBox, QWidget, QComboBox
)

# Function to send JSON data to the server
def send_to_server(data):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8080))
        client_socket.send(json.dumps(data).encode())  # Convert data to JSON and send
        response = client_socket.recv(1024).decode()  # Receive the server's response
        client_socket.close()
        return response
    except Exception as e:
        return f"Error connecting to server: {e}"

# Building Selection Window for Admins
class BuildingSelectionWindow(QMainWindow):
    def __init__(self, buildings):
        super().__init__()
        self.setWindowTitle("Building Selection - Admin Interface")
        self.resize(400, 200)

        layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.building_label = QLabel("Select a Building:")
        self.building_combobox = QComboBox()

        # Populate the combo box with building numbers and descriptions
        for building in buildings:
            self.building_combobox.addItem(f"{building['building_number']} - {building['description']}", building['id'])

        layout.addWidget(self.building_label)
        layout.addWidget(self.building_combobox)

        self.central_widget.setLayout(layout)

# Registration Dialog
class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.resize(300, 240)
        layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.building_number_combobox = QComboBox()
        self.is_admin_checkbox = QCheckBox("Is Admin")

        # Example building numbers and names for demonstration purposes
        buildings = [
            {"building_number": "B001", "name": "ORT Main Building"},
            {"building_number": "B002", "name": "ORT Secondary Building"},
            {"building_number": "B003", "name": "ORT Science Wing"}
        ]
        for building in buildings:
            self.building_number_combobox.addItem(f"{building['building_number']} - {building['name']}")

        layout.addRow("Username:", self.username_input)
        layout.addRow("Password:", self.password_input)
        layout.addRow("Building Number:", self.building_number_combobox)
        layout.addRow("", self.is_admin_checkbox)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.register_user)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        building_number = self.building_number_combobox.currentText()
        is_admin = self.is_admin_checkbox.isChecked()

        if not username or not password or not building_number:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        # Create JSON data to send to the server
        data = {
            "action": "register",
            "username": username,
            "password": password,
            "building_number": building_number,
            "is_admin": is_admin
        }

        # Send the JSON data to the server
        result = send_to_server(data)
        try:
            response = json.loads(result)
            if response.get("status") == "success":
                QMessageBox.information(self, "Success", "Registration successful!")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", response.get("message", "Unknown error"))
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", "Invalid response from server.")

# Main Application Window
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(400, 350)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.validate_login)
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.show_register_dialog)
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.error_label)
        central_widget.setLayout(layout)

    def validate_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and Password are required.")
            return

        # Create JSON data to send to the server
        data = {
            "action": "login",
            "username": username,
            "password": password
        }

        # Send the JSON data to the server
        result = send_to_server(data)

        try:
            response = json.loads(result)
            if response.get("role") == "ADMIN":
                QMessageBox.information(self, "Welcome", f"Welcome, Admin {username}!")
                buildings = response.get("buildings", [])
                self.open_building_selection_window(buildings)
            elif response.get("role") == "TENANT":
                QMessageBox.information(self, "Welcome", f"Welcome, Tenant {username}!")
            else:
                self.error_label.setText("Invalid username or password.")
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", "Invalid response from server.")

    def show_register_dialog(self):
        dialog = RegisterDialog()
        dialog.exec()

    def open_building_selection_window(self, buildings):
        self.building_selection_window = BuildingSelectionWindow(buildings)
        self.building_selection_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
