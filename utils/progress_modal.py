import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QVBoxLayout, QProgressBar, QLabel
from PyQt5.QtCore import Qt
import time

class ProgressModal(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aguarde")
        self.setModal(True)
        self.setFixedSize(400, 150)

        layout = QVBoxLayout()

        self.label = QLabel("Processando...")
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

        self.progress = QProgressBar(self)
        self.progress.setMaximum(100)
        layout.addWidget(self.progress)

        self.setLayout(layout)
        self.step = 0

    def set_progress(self, value, message=None):
        self.step = min(self.step + value, 100)
        self.progress.setValue(self.step)
        
        if message:
            self.label.setText(message)
        
        # if self.step >= 100:
        #     # self.label.setText("Concluído!")
        #     self.accept()
        QApplication.processEvents()
    
    def finalizar(self):
        self.accept()
        QApplication.processEvents()


class MainWindowExample(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Principal")
        self.setFixedSize(200, 100)

        self.button = QPushButton("Iniciar Processo", self)
        self.button.clicked.connect(self.open_modal)
        self.button.move(50, 30)

    def open_modal(self):
        modal = ProgressModal()
        modal.show()
        
        # Simula um processo com progresso manual
        modal.set_progress(20, "Carregando dados...")
        
        time.sleep(1)
        
        modal.set_progress(30, "Processando informações...")
        
        time.sleep(1)
        
        modal.set_progress(25, "Salvando resultados...")
        
        time.sleep(1)
        
        modal.set_progress(25, "Finalizando...")
        
        modal.finalizar()
        
        # modal.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowExample()
    window.show()
    sys.exit(app.exec_())