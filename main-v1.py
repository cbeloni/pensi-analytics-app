import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("CSV Selector and Text Input")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # CSV File Selector
        self.csv_label = QLabel("Select a CSV file:")
        layout.addWidget(self.csv_label)

        self.csv_button = QPushButton("Browse")
        self.csv_button.clicked.connect(self.select_csv_file)
        layout.addWidget(self.csv_button)

        # Text Input
        self.text_label = QLabel("Defina a variável alvo:")
        layout.addWidget(self.text_label)

        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)

        self.setLayout(layout)

    def select_csv_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            self.csv_label.setText(f"Selected File: {file_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())