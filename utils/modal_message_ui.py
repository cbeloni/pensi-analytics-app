from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QApplication, QPushButton
import sys

class MessageModal(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mensagem")
        self.setModal(True)
        self.resize(300, 120)

        layout = QVBoxLayout()
        self.label = QLabel(message)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

# Exemplo de uso:
if __name__ == "__main__":
    app = QApplication(sys.argv)
    modal = MessageModal("Esta é uma mensagem de exemplo.")
    modal.exec_()