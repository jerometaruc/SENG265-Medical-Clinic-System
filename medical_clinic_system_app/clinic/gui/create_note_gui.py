from ast import main
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

class CreateNoteGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.logged_in = True

    def create_note(self):
        self.setWindowTitle("Add note to patient record")
        self.setFixedSize(400, 200)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

         # Create layout
        main_layout = QVBoxLayout()

        # Title label
        title_label = QLabel("Add note to patient record:")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Input field
        note_label = QLabel("Add note:")
        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Add text here")

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        # Add widgets to layout
        main_layout.addWidget(title_label)
        main_layout.addWidget(note_label)
        main_layout.addWidget(self.note_input)
        main_layout.addLayout(button_layout)

        # Connect buttons to actions
        save_button.clicked.connect(self.save_note)
        cancel_button.clicked.connect(self.close)

        # Set layout for central widget
        central_widget.setLayout(main_layout)

    def save_note(self):
        note_text = self.note_input.text()
        if not note_text:
            QMessageBox.warning(self, "Input Error", "Note cannot be empty.")
            return
        try:
            self.controller.create_note(note_text)
            QMessageBox.information(self, "Success", "Note added to the system.")  # Corrected line
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create note: {e}")

if __name__ == '__main__':
    main()