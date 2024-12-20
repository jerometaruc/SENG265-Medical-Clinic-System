from ast import main
from PyQt6.QtWidgets import (QApplication,QMainWindow,
    QWidget, QLabel, QLineEdit,  QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox,
    QTableView
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt  # Import Qt for alignment flags
from clinic.exception.illegal_access_exception import IllegalAccessException

class RetrieveExistingGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.logged_in = True
        self.user = self.controller.username
        self.name_input = None

    def print_existing_patients(self):
        self.setWindowTitle("Retrieve by name")
        self.setFixedSize(400, 300)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()

        # Welcome label
        welcome_user = QLabel("Search Patients By Name")
        welcome_user.setStyleSheet("font-size: 18px; font-weight: bold;")
        welcome_user.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Use Qt.AlignmentFlag

        # PHN input
        name_label = QLabel("Enter Name to Search:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Patient Name")

        # Buttons
        button_layout_1 = QHBoxLayout()
        search_patient_button = QPushButton("Search Patient")
        button_layout_1.addWidget(search_patient_button)
        cancel_button = QPushButton("Cancel")
        button_layout_1.addWidget(cancel_button)
    
        # connect functionality to button
        search_patient_button.clicked.connect(self.retrieve_patients)
        cancel_button.clicked.connect(self.close)

        # Set layout for central widget
        main_layout.addWidget(welcome_user)
        main_layout.addWidget(name_label)
        main_layout.addWidget(self.name_input)
        main_layout.addLayout(button_layout_1)
        central_widget.setLayout(main_layout)

    def retrieve_patients(self):
        name = self.name_input.text().strip()
        patients = self.controller.retrieve_patients(name)
        self.setWindowTitle("Retrieve Patients")
        self.setFixedSize(600, 400)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create layout
        main_layout = QVBoxLayout()

        # Welcome label
        welcome_user = QLabel("Patient List:")
        welcome_user.setStyleSheet("font-size: 18px; font-weight: bold;")
        welcome_user.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Table View for Patient List
        patient_table = QTableView()
        patient_model = QStandardItemModel()
        patient_model.setHorizontalHeaderLabels([
            "PHN", "Name", "Address", "Phone Number", "Birthdate", "Email"
        ])

        if patients:
            for patient in patients:
                row_data = [
                    QStandardItem(str(patient.phn)),
                    QStandardItem(patient.name),
                    QStandardItem(patient.address),
                    QStandardItem(patient.phone),
                    QStandardItem(patient.birth_date),
                    QStandardItem(patient.email),
                ]
                patient_model.appendRow(row_data)
        else:
            patient_model.appendRow([
                QStandardItem("No patients found."),
                QStandardItem(), QStandardItem(), QStandardItem(), QStandardItem(), QStandardItem()
            ])

        # Set model for QTableView
        patient_table.setModel(patient_model)
        patient_table.resizeColumnsToContents()

        # Buttons
        button_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(cancel_button)

        # Connect buttons to actions
        cancel_button.clicked.connect(self.close)

        # Set layout for central widget
        main_layout.addWidget(welcome_user)
        main_layout.addWidget(patient_table)
        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)

if __name__ == '__main__':
    main()
