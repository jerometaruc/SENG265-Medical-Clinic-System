from ast import main
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.gui.edit_note_gui import EditNoteGUI

class ListNotesGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.logged_in = True
        self.edit_note_gui = None

    def print_notes(self):
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
            # Fetch notes from the controller (via the current patient)
            notes = self.controller.list_notes()

            # Format and display notes in reverse order
            for note in notes:  # Reverse the list for displaying latest first
                note_code = f"Code: {note.code}"  # Access note code
                note_date = note.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")  # Format timestamp
                note_content = note.text
                note_text_edit.appendPlainText(f"{note_code}, from {note_date}\n{note_content}\n")

        except IllegalAccessException as e:
            QMessageBox.critical(self, "Error", str(e))
            self.close()

        # Buttons
        button_layout = QHBoxLayout()
        edit_button = QPushButton("Update/Delete note")
        button_layout.addWidget(edit_button)
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(cancel_button)

        # Connect buttons to actions
        edit_button.clicked.connect(self.edit)
        cancel_button.clicked.connect(self.close)

        # Add button layout to main layout
        main_layout.addLayout(button_layout)

        # Set the layout for the central widget
        central_widget.setLayout(main_layout)

    def edit(self):
        if not self.edit_note_gui:
            self.edit_note_gui = EditNoteGUI(self.controller)
        self.edit_note_gui.print_search()
        self.edit_note_gui.show()
        self.close()

if __name__ == '__main__':
    main()