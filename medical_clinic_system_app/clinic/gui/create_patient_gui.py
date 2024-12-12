from ast import main
from clinic.exception.illegal_access_exception import IllegalAccessException
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)

from PyQt6.QtCore import Qt  # Import Qt for alignment flags

class CreatePatientGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.logged_in = True
        self.user = self.controller.username

    def create_patient(self):
        self.setWindowTitle(self.user + "; Create Patient")
        self.setFixedSize(400, 500)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create layout
        main_layout = QVBoxLayout()

        # Title label
        title_label = QLabel("Create New Patient")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Input fields
        name_label = QLabel("Full Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")

        phn_label = QLabel("PHN:")
        self.phn_input = QLineEdit()
        self.phn_input.setPlaceholderText("Personal Health Number (PHN)")
        self.phn_input.setInputMask("0000000000")  # PHN must be 10 digits

        birthdate_label = QLabel("Birthdate:")
        self.birthdate_input = QLineEdit()
        self.birthdate_input.setPlaceholderText("Birthdate (yyyy-mm-dd)")
        self.birthdate_input.setInputMask("0000-00-00")  # Birthdate format yyyy/mm/dd

        address_label = QLabel("Address:")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Address")

        phone_label = QLabel("Phone Number:")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone Number")
        self.phone_input.setInputMask("000 000 0000")  # Phone number format (xxx)xxx-xxxx

        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        # Add widgets to layout
        main_layout.addWidget(title_label)
        main_layout.addWidget(name_label)
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(phn_label)
        main_layout.addWidget(self.phn_input)
        main_layout.addWidget(birthdate_label)
        main_layout.addWidget(self.birthdate_input)
        main_layout.addWidget(address_label)
        main_layout.addWidget(self.address_input)
        main_layout.addWidget(phone_label)
        main_layout.addWidget(self.phone_input)
        main_layout.addWidget(email_label)
        main_layout.addWidget(self.email_input)
        main_layout.addLayout(button_layout)

        # Connect buttons to actions
        save_button.clicked.connect(self.save_patient)
        cancel_button.clicked.connect(self.close)

        # Set layout for central widget
        central_widget.setLayout(main_layout)

    def save_patient(self):
        # Collect input data
        name = self.name_input.text()
        phn = int(self.phn_input.text())
        birth_date = self.birthdate_input.text()
        address = self.address_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        # Validate input data
        if not all([name, phn, birth_date, address, phone, email]):
            QMessageBox.warning(self, "Input Error", "All fields must be filled out.")
            return

        # Send data to controller
        try:
            self.controller.create_patient(phn, name, birth_date, phone, email, address)
            QMessageBox.information(self, "Success", "Patient created successfully.")
            self.close()
        except Exception as e:  # Replace with specific exceptions if needed
            QMessageBox.critical(self, "Error", f"Failed to create patient: {e}")

if __name__ == '__main__':
    main()
