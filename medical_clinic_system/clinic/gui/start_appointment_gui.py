from ast import main
from clinic.controller import Controller
from clinic.gui.appointment_menu_gui import AppointmentMenuGUI
from clinic.exception.invalid_login_exception import InvalidLoginException
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)
from clinic.exception.illegal_operation_exception import IllegalOperationException

class StartAppointmentGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.logged_in = True
        self.phn_input = None
        self.appointment_menu_gui = None
        self.controller = controller

    def start_appointment(self):
        self.setWindowTitle("Start Appointment")
        self.setFixedSize(400, 200)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create layout
        main_layout = QVBoxLayout()

        # Main label
        start_label = QLabel("Start Appointment")
        start_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(start_label)

        # PHN input
        phn_label = QLabel("Personal Health Number (PHN):")
        self.phn_input = QLineEdit()
        self.phn_input.setPlaceholderText("Enter your Personal Health Number (PHN):")
        self.phn_input.setInputMask("0000000000")  # PHN must be 10 digits
        main_layout.addWidget(phn_label)
        main_layout.addWidget(self.phn_input)

        # Buttons
        button_layout = QHBoxLayout()
        enter_button = QPushButton("Enter")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(enter_button)
        button_layout.addWidget(cancel_button)

        # Connect buttons to actions
        enter_button.clicked.connect(self.handle_phn)
        cancel_button.clicked.connect(self.close)

        main_layout.addLayout(button_layout)

        # Set layout for the central widget
        central_widget.setLayout(main_layout)

    def handle_phn(self):
        if self.phn():
            if not self.appointment_menu_gui:
                self.appointment_menu_gui = AppointmentMenuGUI(self.controller)
            self.appointment_menu_gui.appointment_menu()
            self.reset_phn()
            self.appointment_menu_gui.show()
            self.close()
        else: 
            self.reset_phn()

    def phn(self):
        try:
            phn = int(self.phn_input.text())
            self.controller.set_current_patient(phn)
            return True
        except ValueError:
            QMessageBox.warning(self, "Error", "PHN must be a valid numeric value.")
            return False
        except IllegalOperationException:
            QMessageBox.warning(self, "Error", "Illegal Operation: Cannot set the current patient to an inexistent patient.")
            return False
        except InvalidLoginException:
            QMessageBox.warning(self, "Error", "Invalid PHN.")
            return False

    def reset_phn(self):
        self.phn_input.clear()

if __name__ == '__main__':
    main()