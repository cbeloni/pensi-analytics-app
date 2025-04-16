from PyQt5 import QtWidgets
from tela_ui import Ui_MainWindow
from business.bo_xgbooster import processar
from PyQt5.QtGui import QPixmap

from utils.progress import Progress


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_connections()

    def setup_connections(self):
        self.ui.pushButton.clicked.connect(self.processar)
        self.ui.buttonCsv.clicked.connect(self.select_csv_file)

    def processar(self):
        print("Botão 'Processar' foi clicado!")
        
        self.progress = Progress(self.ui.progressBar)
        self.progress.set_progress(0)
        self.ui.pushButton.setEnabled(False)
        
        variavel_alvo = self.ui.textVariavelAlvo.text()
        csv_path = self.ui.textCsvPath.text()
        resultado = ""
        feature_importance = ""
        try:
            resultado, feature_importance = processar(csv_path, variavel_alvo, self.progress)        
        except Exception as e:
            resultado = f"Erro: {e}"
        
        self.ui.textResultado.setPlainText(resultado)
        self.ui.textFeature.setPlainText(feature_importance)
        
        pixmap = QPixmap("confusion_matriz.png")
        self.ui.labelMatriz.setPixmap(pixmap)
        self.ui.labelMatriz.setScaledContents(True)
        
        pixmap = QPixmap("curva_roc.png")
        self.ui.labelRoc.setPixmap(pixmap)
        self.ui.labelRoc.setScaledContents(True)
        
        self.ui.pushButton.setEnabled(True)
        
            
    def select_csv_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            self.ui.textCsvPath.setText(f"{file_path}")

if __name__ == "__main__":
    import sys    
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
