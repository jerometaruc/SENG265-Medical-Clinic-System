from ast import main
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTableView, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from clinic.exception.illegal_access_exception import IllegalAccessException

class ListPatientsGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.logged_in = True
        self.user = self.controller.username

    def print_patients(self):
        self.setWindowTitle(self.user + "; List Patients")
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
            "PHN", "Name", "Address", "Phone Number", "Birthdate"
        ])

        try:
            patients = self.controller.list_patients()
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
                # Add an empty row with a message
                patient_model.appendRow([
                    QStandardItem("No patients registered in the clinic."),
                    QStandardItem(), QStandardItem(), QStandardItem(), QStandardItem()
                ])
        except IllegalAccessException:
            patient_model.appendRow([
                QStandardItem("MUST LOGIN FIRST."),
                QStandardItem(), QStandardItem(), QStandardItem(), QStandardItem()
            ])

        # Set model for the QTableView
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
