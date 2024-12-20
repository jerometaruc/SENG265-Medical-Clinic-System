from ast import main
from clinic.gui.create_note_gui import CreateNoteGUI
from clinic.gui.list_patient_record_gui import ListNotesGUI
from clinic.gui.retrieve_notes_gui import RetrieveNotesGUI
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
from PyQt6.QtCore import Qt

class AppointmentMenuGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.logged_in = True
        self.create_note_gui = None
        self.list_patient_record_gui = None
        self.retrieve_notes_gui = None

    def appointment_menu(self):
        self.setWindowTitle("Medical Clinic System - Appointment Menu")
        self.setFixedSize(650, 350)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()

        # Patient info
        welcome_user = QLabel(self.controller.current_patient.name)
        welcome_user.setStyleSheet("font-size: 18px; font-weight: bold;")
        welcome_user.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Use Qt.AlignmentFlag

        patient_label = QLabel("PATIENT:")
        phn_label = QLabel("PHN: " + str(self.controller.current_patient.phn))
        name_label =  QLabel("Name: " + self.controller.current_patient.name)
        birthdate_label = QLabel("Birth date: " + self.controller.current_patient.birth_date)
        phone_label = QLabel("Phone: " + self.controller.current_patient.phone)
        email_label = QLabel("Email: " + self.controller.current_patient.email)
        address_label = QLabel("Address: " + self.controller.current_patient.address)

        patient_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        phn_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        name_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        birthdate_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        phone_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        email_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        address_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        patient_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        phn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        birthdate_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        phone_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        email_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        address_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Buttons
        button_layout_1 = QHBoxLayout()
        add_note = QPushButton("Add note to patient record")
        retrieve_notes_by_text = QPushButton("Retrieve notes from patient record by text")
        button_layout_1.addWidget(add_note)
        button_layout_1.addWidget(retrieve_notes_by_text)

        button_layout_2 = QHBoxLayout()
        list_notes = QPushButton("List full patient record")
        finish_button = QPushButton("Finish appointment")
        button_layout_2.addWidget(list_notes)
        button_layout_2.addWidget(finish_button)

        # Connect buttons to actions
        add_note.clicked.connect(self.create_note)
        retrieve_notes_by_text.clicked.connect(self.retrieve_notes)
        list_notes.clicked.connect(self.list_patient_record)
        finish_button.clicked.connect(self.finish_appt)

        # Set layout for central widget
        main_layout.addWidget(patient_label)
        main_layout.addWidget(phn_label)
        main_layout.addWidget(name_label)
        main_layout.addWidget(birthdate_label)
        main_layout.addWidget(phone_label)
        main_layout.addWidget(email_label)
        main_layout.addWidget(address_label)
        main_layout.addLayout(button_layout_1)
        main_layout.addLayout(button_layout_2)
        central_widget.setLayout(main_layout)

    def create_note(self):
        if not self.create_note_gui:
            self.create_note_gui = CreateNoteGUI(self.controller)
        self.create_note_gui.create_note()
        self.create_note_gui.show()

    def list_patient_record(self):
        if not self.list_patient_record_gui:
            self.list_patient_record_gui = ListNotesGUI(self.controller)
        self.list_patient_record_gui.print_notes()
        self.list_patient_record_gui.show()

    def retrieve_notes(self):
        if not self.retrieve_notes_gui:
            self.retrieve_notes_gui = RetrieveNotesGUI(self.controller)
        self.retrieve_notes_gui.print_existing_notes()
        self.retrieve_notes_gui.show()

    def finish_appt(self):
        self.controller.unset_current_patient()
        self.close()
    
if __name__ == '__main__':
    main()