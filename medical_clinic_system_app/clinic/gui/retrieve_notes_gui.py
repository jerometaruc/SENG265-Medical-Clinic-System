from ast import main
from PyQt6.QtWidgets import (QApplication,QMainWindow,
    QWidget, QLabel, QLineEdit,  QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox,
    QPlainTextEdit
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt  # Import Qt for alignment flags
from clinic.exception.illegal_access_exception import IllegalAccessException

class RetrieveNotesGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.logged_in = True
        self.user = self.controller.username
        self.text_input = None

    def print_existing_notes(self):
        self.setWindowTitle("Retrieve Notes from Patient by Text")
        self.setFixedSize(400, 300)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()

        # Welcome label
        welcome_user = QLabel("Search Notes by Text")
        welcome_user.setStyleSheet("font-size: 18px; font-weight: bold;")
        welcome_user.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Use Qt.AlignmentFlag

        # PHN input
        text_label = QLabel("Enter Text to Search:")
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Note Text")

        # Buttons
        button_layout_1 = QHBoxLayout()
        search_notes_button = QPushButton("Search Notes")
        button_layout_1.addWidget(search_notes_button)
        cancel_button = QPushButton("Cancel")
        button_layout_1.addWidget(cancel_button)
    
        # connect functionality to button
        search_notes_button.clicked.connect(self.retrieve_notes)
        cancel_button.clicked.connect(self.close)

        # Set layout for central widget
        main_layout.addWidget(welcome_user)
        main_layout.addWidget(text_label)
        main_layout.addWidget(self.text_input)
        main_layout.addLayout(button_layout_1)
        central_widget.setLayout(main_layout)

    def retrieve_notes(self):
        text = self.text_input.text().strip()
        if not text:
            QMessageBox.warning(self, "Input Error", "Please enter text to search.")
            return
        self.setWindowTitle("List full patient record")
        self.setFixedSize(600, 400)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create layout
        main_layout = QVBoxLayout()

        # Welcome label
        welcome_user = QLabel("Patient record:")
        welcome_user.setStyleSheet("font-size: 18px; font-weight: bold;")
        welcome_user.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set model for the QPlainTextEdit
        note_text_edit = QPlainTextEdit()
        note_text_edit.setReadOnly(True)

         # Add widgets to layout
        main_layout.addWidget(welcome_user)
        main_layout.addWidget(note_text_edit)
        
        try:
            notes = self.controller.retrieve_notes(text)
            if not notes:
                QMessageBox.information(self, "No Results", "No notes match the given text.")
                self.close()
                return False
            # Clear existing notes and populate with new ones
            note_text_edit.clear()
            for note in notes:
                note_code = f"Code: {note.code}"
                note_date = note.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                note_content = note.text
                note_text_edit.appendPlainText(f"{note_code}, from {note_date}\n{note_content}\n")
        except IllegalAccessException as e:
            QMessageBox.critical(self, "Error", str(e))
            self.close()

        # Buttons
        button_layout = QHBoxLayout()
        exit_button = QPushButton("Exit")
        button_layout.addWidget(exit_button)

        # Connect buttons to actions
        exit_button.clicked.connect(self.close)

        # Add button layout to main layout
        main_layout.addLayout(button_layout)

        # Set the layout for the central widget
        central_widget.setLayout(main_layout)

if __name__ == '__main__':
    main()