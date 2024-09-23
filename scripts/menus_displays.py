# Script: `./scripts/menu_displays.py`

# Imports
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wsl2g-AmdGpu-Agent")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # User Input
        self.user_input = QTextEdit()
        self.user_input.setPlaceholderText("Enter your message here...")
        left_layout.addWidget(QLabel("User Input"))
        left_layout.addWidget(self.user_input)

        # Submit Button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_submit)
        left_layout.addWidget(self.submit_button)

        # AI Chat Output
        self.chat_output = QTextEdit()
        self.chat_output.setReadOnly(True)
        right_layout.addWidget(QLabel("AI Chat Output"))
        right_layout.addWidget(self.chat_output)

        # Current Goal
        self.current_goal = QTextEdit()
        self.current_goal.setReadOnly(True)
        left_layout.addWidget(QLabel("Current Goal"))
        left_layout.addWidget(self.current_goal)

        # Task List
        self.task_list = QTextEdit()
        self.task_list.setReadOnly(True)
        right_layout.addWidget(QLabel("Task List"))
        right_layout.addWidget(self.task_list)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        central_widget.setLayout(main_layout)

    def on_submit(self):
        user_message = self.user_input.toPlainText()
        self.user_input.clear()
        # Process user message and update chat output
        # This will be implemented later when we integrate with the AI logic

def show_main_window():
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()

def show_model_menu(model_files):
    # This function can be updated to use a PyQt dialog instead of console input
    print("Multiple models found:")
    for i, model_file in enumerate(model_files):
        print(f"{i+1}. {model_file}")
    
    selection = int(input("Enter the number of the model you wish to use: ")) - 1
    if 0 <= selection < len(model_files):
        return model_files[selection]
    else:
        print("Invalid selection.")
        return show_model_menu(model_files)  # Recurse if invalid