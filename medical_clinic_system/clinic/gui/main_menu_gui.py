from ast import main
from clinic.gui.search_patient_gui import SearchPatientGUI
from clinic.gui.retrieve_existing_gui import RetrieveExistingGUI
from clinic.gui.list_patients_gui import ListPatientsGUI
from clinic.gui.create_patient_gui import CreatePatientGUI
from clinic.gui.delete_update_by_phn_gui import DeleteUpdateByPhnGUI
from clinic.gui.start_appointment_gui import StartAppointmentGUI
from PyQt6.QtWidgets import (QApplication,QMainWindow,
    QWidget, QLabel, QLineEdit,  QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox,
)
from PyQt6.QtCore import Qt  # Import Qt for alignment flags

class MainMenuGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.logged_in = True
        self.user = self.controller.username
        self.search_patient_gui = None
        self.retrieve_existing_gui = None
        self.list_patients_gui = None
        self.start_appointment_gui = None
        self.create_patient_gui = None
        # self.update_patient_gui = None
        self.delete_update_by_phn_gui = None
        # self.user = self.controller.get_current_patient(self)

    def main_menu(self):
        self.setWindowTitle("Medical Clinic System - Main Menu")
        self.setFixedSize(400, 300)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()

        # Welcome label
        welcome_user = QLabel("Hello, " + self.user)
        welcome_user.setStyleSheet("font-size: 18px; font-weight: bold;")
        welcome_user.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Use Qt.AlignmentFlag

        # Buttons
        button_layout_1 = QHBoxLayout()
        search_patient_button = QPushButton("Search Patient")
        create_patient_button = QPushButton("Create New Patient")
        button_layout_1.addWidget(search_patient_button)
        button_layout_1.addWidget(create_patient_button)

        # Buttons
        button_layout_2 = QHBoxLayout()
        delete_update_patient_button = QPushButton("Delete / Update patient")
        # update_patient_button = QPushButton("Update existing patient")
        button_layout_2.addWidget(delete_update_patient_button)
        # button_layout_2.addWidget(update_patient_button)

        # Buttons
        button_layout_3 = QHBoxLayout()
        retrieve_patients_button = QPushButton("Retrieve Existing Patients")
        list_patients_button = QPushButton("List all patients")
        button_layout_3.addWidget(retrieve_patients_button)
        button_layout_3.addWidget(list_patients_button)

        # connect functionality to button
        list_patients_button.clicked.connect(self.list_patients)
        create_patient_button.clicked.connect(self.create_patient)
        delete_update_patient_button.clicked.connect(self.delete_update_by_phn_patient)
        search_patient_button.clicked.connect(self.search_patient)
        retrieve_patients_button.clicked.connect(self.retrieve_existing)

        # Buttons
        button_layout_4 = QHBoxLayout()
        start_appt_button = QPushButton("Start Appointment")
        logout_button = QPushButton("Logout")
        button_layout_4.addWidget(start_appt_button)
        button_layout_4.addWidget(logout_button)

        # Connect buttons to actions
        logout_button.clicked.connect(self.logout)
        start_appt_button.clicked.connect(self.open_appointment_menu)

        # Set layout for central widget
        main_layout.addWidget(welcome_user)
        main_layout.addLayout(button_layout_1)
        main_layout.addLayout(button_layout_2)
        main_layout.addLayout(button_layout_3)
        main_layout.addLayout(button_layout_4)
        central_widget.setLayout(main_layout)

    def list_patients(self):
        if not self.list_patients_gui:
            self.list_patients_gui = ListPatientsGUI(self.controller)
        self.list_patients_gui.print_patients()
        self.list_patients_gui.show()
        # self.hide()

    def create_patient(self):
        if not self.create_patient_gui:
            self.create_patient_gui = CreatePatientGUI(self.controller)
        self.create_patient_gui.create_patient()
        self.create_patient_gui.show()
        # self.hide()

    # def update_patient(self):
    #     if not self.update_patient_gui:
    #         self.update_patient_gui = UpdatePatientGUI(self.controller)
    #     self.update_patient_gui.update_patient()
    #     self.update_patient_gui.show()
    #     # self.hide()

    def delete_update_by_phn_patient(self):
        if not self.delete_update_by_phn_gui:
            self.delete_update_by_phn_gui = DeleteUpdateByPhnGUI(self.controller)
        self.delete_update_by_phn_gui.print_search()
        self.delete_update_by_phn_gui.show()
        # self.hide()

    def search_patient(self):
        if not self.search_patient_gui:
            self.search_patient_gui = SearchPatientGUI(self.controller)
        self.search_patient_gui.print_search()
        self.search_patient_gui.show()
        # self.hide()

    def retrieve_existing(self):
        if not self.retrieve_existing_gui:
            self.retrieve_existing_gui = RetrieveExistingGUI(self.controller)
        self.retrieve_existing_gui.print_existing_patients()
        self.retrieve_existing_gui.show()
        # self.hide()

    def logout(self):
        if self.controller.logout():
            self.close()

    def open_appointment_menu(self):
        if not self.start_appointment_gui:
            self.start_appointment_gui = StartAppointmentGUI(self.controller)
        self.start_appointment_gui.start_appointment()
        self.start_appointment_gui.show()
        # self.hide()

if __name__ == '__main__':
    main()
