from ast import main
from PyQt6.QtWidgets import (QApplication,QMainWindow,
    QWidget, QLabel, QLineEdit,  QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox,
)
from PyQt6.QtCore import Qt  # Import Qt for alignment flags
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException

class EditNoteGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.logged_in = True
        self.note = None
        self.code_input = None
        self.text_input = None

    def print_search(self):
        self.setWindowTitle("Search by Code")
        self.setFixedSize(400, 300)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()

        # Welcome label
        welcome_user = QLabel("Here you can Update or Delete a Cote. \n\n Search by Code")
        welcome_user.setStyleSheet("font-size: 18px; font-weight: bold;")
        welcome_user.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Use Qt.AlignmentFlag

        # Code input
        code_label = QLabel("Enter Code:")
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Enter the Code")

        # Buttons
        button_layout_1 = QHBoxLayout()
        update_note_button = QPushButton("Update Note")
        delete_note_button = QPushButton("Delete Note")
        cancel_button = QPushButton("Cancel")
        button_layout_1.addWidget(update_note_button)
        button_layout_1.addWidget(delete_note_button)
        button_layout_1.addWidget(cancel_button)

        # connect functionality to button
        update_note_button.clicked.connect(self.update_note)
        delete_note_button.clicked.connect(self.delete_note)
        cancel_button.clicked.connect(self.close)

        # Set layout for central widget
        main_layout.addWidget(welcome_user)
        main_layout.addWidget(code_label)
        main_layout.addWidget(self.code_input)
        main_layout.addLayout(button_layout_1)
        central_widget.setLayout(main_layout)

    def update_note(self):
        try:
            note_code_text = self.code_input.text().strip()
            if not note_code_text.isdigit():
                QMessageBox.warning(self, "Error", "Note code must be a valid number.")
                return
            code = int(note_code_text)
            # Search for the note using the controller
            self.note = self.controller.search_note(code)
            
            if self.note:
                self.update_note_window(code)
                # self.close()
            else:
                QMessageBox.warning(self, "Error", "No note found with the entered code.")
        except IllegalAccessException:
            QMessageBox.warning(self, "Login Required", "You must be logged in to perform this action.")
        except IllegalOperationException as e:
            QMessageBox.warning(self, "Error", f"An unknown error occurred: {str(e)}")

    def delete_note(self):
        try:
            note_code_text = self.code_input.text().strip()
            if not note_code_text.isdigit():
                QMessageBox.warning(self, "Error", "Note code must be a valid number.")
                return
            code = int(note_code_text)
            self.note = self.controller.search_note(code)
            if self.note:
                self.controller.delete_note(code)
                QMessageBox.information(self, "Success", "Note removed successfully.")
                self.close()
            else:
                QMessageBox.warning(self, "Error", "No note found with the entered code.")
        except IllegalAccessException:
            QMessageBox.warning(self, "Login", "You must be logged in to perform this action.")
        except IllegalOperationException:
            QMessageBox.warning(self, "Error", "An unknown error occurred.")

    def update_note_window(self, note_code):
        self.setWindowTitle("Update Note")
        self.setFixedSize(400, 300)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create layout
        main_layout = QVBoxLayout()

        # Title label
        title_label = QLabel("Update Note")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Input fields
        text_label = QLabel("New Text:")
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter new note text")
        self.text_input.setText(self.note.text)

        # Buttons
        button_layout = QHBoxLayout()
        update_button = QPushButton("Update")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(update_button)
        button_layout.addWidget(cancel_button)

        # Add widgets to layout
        main_layout.addWidget(title_label)
        main_layout.addWidget(text_label)
        main_layout.addWidget(self.text_input)
        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)

        # Store note code in a new attribute
        self.current_note_code = note_code
        
        # Connect buttons to actions
        update_button.clicked.connect(self.update_note_action)
        cancel_button.clicked.connect(self.close)

        # Set layout for central widget
        central_widget.setLayout(main_layout)

    def update_note_action(self):
        new_text = self.text_input.text().strip()
        if not new_text:
            QMessageBox.warning(self, "Input Error", "Note text must be filled out.")
            return
        code = self.current_note_code
        try:
            self.controller.update_note(code, new_text)
            QMessageBox.information(self, "Success", "Note updated successfully.")
            self.close()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Note code must be a valid number.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

if __name__ == '__main__':
    main()
