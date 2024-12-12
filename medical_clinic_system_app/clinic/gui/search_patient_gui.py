from ast import main
from PyQt6.QtWidgets import (QApplication,QMainWindow,
    QWidget, QLabel, QLineEdit,  QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox,
)
from PyQt6.QtCore import Qt  # Import Qt for alignment flags

class SearchPatientGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.logged_in = True
        self.user = self.controller.username
        self.update_patient_gui = None
        self.phn_input = None
        # self.user = self.controller.get_current_patient(self)

    def print_search(self):
        self.setWindowTitle("Search by PHN")
        self.setFixedSize(400, 300)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()

        # Welcome label
        welcome_user = QLabel("Search Patient by PHN")
        welcome_user.setStyleSheet("font-size: 18px; font-weight: bold;")
        welcome_user.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Use Qt.AlignmentFlag

        # PHN input
        phn_label = QLabel("Enter PHN:")
        self.phn_input = QLineEdit()
        self.phn_input.setPlaceholderText("Enter the PHN")
        self.phn_input.setInputMask("0000000000")  # PHN must be 10 digits

        # Buttons
        button_layout_1 = QHBoxLayout()
        search_patient_button = QPushButton("Search Patient")
        button_layout_1.addWidget(search_patient_button)
        cancel_button = QPushButton("Cancel")
        button_layout_1.addWidget(cancel_button)
    
        # connect functionality to button
        search_patient_button.clicked.connect(self.search_patient)
        cancel_button.clicked.connect(self.close)

        # Set layout for central widget
        main_layout.addWidget(welcome_user)
        main_layout.addWidget(phn_label)
        main_layout.addWidget(self.phn_input)
        main_layout.addLayout(button_layout_1)
        central_widget.setLayout(main_layout)

    def search_patient(self):
        # if phn exists, then open update GUI
        try:
            phn = int(self.phn_input.text())
            patient = self.controller.search_patient(phn)
            if patient:
                self.setWindowTitle("Search Results")

                # Central widget
                central_widget = QWidget(self)
                self.setCentralWidget(central_widget)

                # Main layout
                main_layout = QVBoxLayout()

                # client info
                client_name = QLabel("Full Name: " + patient.name)
                client_phn = QLabel("PHN: " + str(patient.phn))
                client_birth = QLabel("BirthDay: " + str(patient.birth_date))
                client_address = QLabel("Address: " + patient.address)
                client_phone = QLabel("Phone: " + str(patient.phone))
                client_email = QLabel("Email: " + patient.email)

                # Buttons
                button_layout_1 = QHBoxLayout()
                cancel_button = QPushButton("Cancel")
                button_layout_1.addWidget(cancel_button)
                cancel_button.clicked.connect(self.close)

                # Set layout for central widget
                main_layout.addWidget(client_name)
                main_layout.addWidget(client_phn)
                main_layout.addWidget(client_birth)
                main_layout.addWidget(client_address)
                main_layout.addWidget(client_phone)
                main_layout.addWidget(client_email)
                main_layout.addLayout(button_layout_1)
                central_widget.setLayout(main_layout)

            else:
                QMessageBox.warning(self, "Error", "There is no patient registered with this PHN.")   

        except ValueError:
            QMessageBox.warning(self, "Input Error", "PHN must be a valid number.")

if __name__ == '__main__':
    main()
