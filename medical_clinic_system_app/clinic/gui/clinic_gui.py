import sys
from clinic.controller import Controller
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.gui.main_menu_gui import MainMenuGUI
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


class ClinicGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.username_input = None
        self.password_input = None
        self.controller = Controller(autosave=True)
        self.main_menu_gui = None
        self.print_login()

    def print_login(self):
        self.setWindowTitle("Medical Clinic System - Login")
        self.setFixedSize(400, 200)

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create layout
        main_layout = QVBoxLayout()

        # Login label
        login_label = QLabel("Login")
        login_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(login_label)

        # Username input
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        main_layout.addWidget(username_label)
        main_layout.addWidget(self.username_input)

        # Password input
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        main_layout.addWidget(password_label)
        main_layout.addWidget(self.password_input)

        # Buttons
        button_layout = QHBoxLayout()
        login_button = QPushButton("Login")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(login_button)
        button_layout.addWidget(cancel_button)

        # Connect buttons to actions
        login_button.clicked.connect(self.handle_login)
        cancel_button.clicked.connect(self.close)

        main_layout.addLayout(button_layout)

        # Set layout for the central widget
        central_widget.setLayout(main_layout)

    def handle_login(self):
        if self.login():
            # self.show_main_menu(self)  # lazy loading
            if not self.main_menu_gui:
                self.main_menu_gui = MainMenuGUI(self.controller)
            self.main_menu_gui.main_menu()
            self.reset_values()
            self.main_menu_gui.show()
            # self.hide()
        else: 
            self.reset_values()

    # lazy loading style
    # def show_main_menu(self):
    #     from clinic.gui.main_menu_gui import MainMenuGUI
    #     self.main_menu_gui = MainMenuGUI(self.controller) 
    #     self.main_menu_gui.show()

    def login(self):
        try:
            # Get input values
            username = self.username_input.text()
            password = self.password_input.text()
            self.controller.login(username, password)
        except InvalidLoginException:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
            return False
        except DuplicateLoginException:
            QMessageBox.warning(self, "Login Failed", "Duplicate login detected.")
            return False
        return True
    
    def reset_values(self):
        self.username_input.clear()
        self.password_input.clear()


def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
