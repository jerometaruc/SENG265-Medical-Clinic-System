from ast import main
from PyQt6.QtWidgets import (QApplication,QMainWindow,
    QWidget, QLabel, QLineEdit,  QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox,
)
from PyQt6.QtCore import Qt  # Import Qt for alignment flags
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException

class DeleteUpdateByPhnGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.logged_in = True
        self.user = self.controller.username
        # self.update_patient_gui = None

        self.patient = None
        self.phn_input = None
        self.name_input = None
        self.birthdate_input = None
        self.email_input = None
        self.phone_input = None
        self.address_input = None

    def print_search(self):
        self.setWindowTitle("Search by PHN")
        self.setFixedSize(400, 300)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()

        # Welcome label
        welcome_user = QLabel("Here you can Update or Delete a Patient. \n\n Search by PHN")
        welcome_user.setStyleSheet("font-size: 18px; font-weight: bold;")
        welcome_user.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Use Qt.AlignmentFlag

        # PHN input
        phn_label = QLabel("Enter PHN:")
        self.phn_input = QLineEdit()
        self.phn_input.setPlaceholderText("Enter the PHN")

        # Buttons
        button_layout_1 = QHBoxLayout()
        update_patient_button = QPushButton("Update Patient")
        delete_patient_button = QPushButton("Delete Patient")
        cancel_button = QPushButton("Cancel")
        button_layout_1.addWidget(update_patient_button)
        button_layout_1.addWidget(delete_patient_button)
        button_layout_1.addWidget(cancel_button)

        # connect functionality to button
        update_patient_button.clicked.connect(self.update_patient)
        delete_patient_button.clicked.connect(self.delete_patient)
        cancel_button.clicked.connect(self.close)

        # Set layout for central widget
        main_layout.addWidget(welcome_user)
        main_layout.addWidget(phn_label)
        main_layout.addWidget(self.phn_input)
        main_layout.addLayout(button_layout_1)
        central_widget.setLayout(main_layout)

    def update_patient(self):
        try:
            phn_text = self.phn_input.text().strip()
            if not phn_text.isdigit():
                QMessageBox.warning(self, "Error", "PHN must be a valid number.")
                return

            phn = int(phn_text)
            self.patient = self.controller.search_patient(phn)
            if self.patient:
                self.update_patient_window()
            else:
                QMessageBox.warning(self, "Error", "No patient found with the entered PHN.")
        except IllegalAccessException:
            QMessageBox.warning(self, "Login Required", "You must be logged in to perform this action.")
        except IllegalOperationException as e:
            QMessageBox.warning(self, "Error", f"An unknown error occurred: {str(e)}")

    def delete_patient(self):
        try:
            phn = int(self.phn_input.text())
            self.patient = self.controller.search_patient(phn)
            if self.patient:
                # confirmation box
                self.controller.delete_patient(phn)
                QMessageBox.warning(self, "Success", "Patient Removed")
                self.close()
            else:
                QMessageBox.warning(self, "Error", "There is no patient registered with this PHN.")
        except IllegalAccessException:
            QMessageBox.warning(self, "Login", "You must be logged in")
        except IllegalOperationException:
            QMessageBox.warning(self, "Error", "Error occured: unknwon")

            # cannot delete current patient
            # if self.controller.current_patient:
            #     if self.controller.current_patient.phn == self.phn_input:
            #         QMessageBox.warning(self, "Error", "Cannot remove current Patient.")
            # else:
            #     QMessageBox.warning(self, "Error", "There is no patient registered with this PHN.")
    
    def update_patient_window(self):
        self.setWindowTitle("Update Patient")
        self.setFixedSize(400, 500)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create layout
        main_layout = QVBoxLayout()

        # Title label
        title_label = QLabel("Update Existing Patient")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Input fields
        name_label = QLabel("Full Name:")
        self.name_input = QLineEdit()
        self.name_input.setText(self.patient.name)

        phn_label = QLabel("PHN:")
        self.phn_input = QLineEdit()
        self.phn_input.setText(str(self.patient.phn))
        self.phn_input.setInputMask("0000000000")  # PHN must be 10 digits

        birthdate_label = QLabel("Birthdate:")
        self.birthdate_input = QLineEdit()
        self.birthdate_input.setText(self.patient.birth_date)
        self.birthdate_input.setInputMask("0000-00-00")  # Birthdate format yyyy/mm/dd

        address_label = QLabel("Address:")
        self.address_input = QLineEdit()
        self.address_input.setText(self.patient.address)

        phone_label = QLabel("Phone Number:")
        self.phone_input = QLineEdit()
        self.phone_input.setText(self.patient.phone)
        self.phone_input.setInputMask("000 000 0000")  # Phone number format (xxx)xxx-xxxx

        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setText(self.patient.email)

        # Buttons
        button_layout = QHBoxLayout()
        update_button = QPushButton("Update")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(update_button)
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
        update_button.clicked.connect(self.update_patient_action)
        cancel_button.clicked.connect(self.close)

        # Set layout for central widget
        central_widget.setLayout(main_layout)

    def update_patient_action(self):

        # Validate input data
        if not all([
            self.name_input.text().strip(),
            self.phn_input.text().strip(),
            self.birthdate_input.text().strip(),
            self.address_input.text().strip(),
            self.phone_input.text().strip(),
            self.email_input.text().strip()
        ]):
            QMessageBox.warning(self, "Input Error", "All fields must be filled out.")
            return
        
        try:
            # Collect input data
            self.controller.update_patient(
                original_phn=self.patient.phn,  # Original PHN of the patient
                phn=int(self.phn_input.text().strip()),  # Convert PHN to integer
                name=self.name_input.text().strip(),
                birth_date=self.birthdate_input.text().strip(),
                phone=self.phone_input.text().strip(),
                email=self.email_input.text().strip(),
                address=self.address_input.text().strip(),
            )
            QMessageBox.information(self, "Success", "Patient updated successfully.")
            self.close()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "PHN must be a valid number.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    
if __name__ == '__main__':
    main()
