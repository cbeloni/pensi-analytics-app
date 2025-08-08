import sys
from PyQt5 import QtWidgets
from tela_ui import Ui_MainWindow
from business.bo_model_factory import modelo_factory
from PyQt5.QtGui import QPixmap

from utils.progress_modal import ProgressModal
import ast
from utils.modal_message_ui import MessageModal

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_connections()

    def setup_connections(self):
        try:
            self.ui.pushButton.clicked.connect(self.processar)
        except Exception as e:
            MessageModal(f"Erro ao processar modelo: {e}").exec_()
        # self.ui.buttonCsv.clicked.connect(self.select_csv_file)

    def processar(self):
        print("Botão 'Processar' foi clicado!")
        
        progress = ProgressModal()
        progress.show()
        self.ui.pushButton.setEnabled(False)
        
        variavel_alvo = self.ui.textVariavelAlvo.text()
        csv_path = self.ui.textCsvPath.text()
        hiperametros_text = self.ui.textHiperparam.text()
        hiperametros = ast.literal_eval(hiperametros_text) if hiperametros_text else {}
        try:
            model = modelo_factory(self.ui.comboBoxModelo.currentText())
            resultado, feature_importance = model.processar(csv_path, variavel_alvo, progress, hiperametros=hiperametros)        
        except Exception as e:
            error_message = str(e)[:500]
            MessageModal(f"Erro ao processar modelo: {error_message}").exec_()
            self.ui.pushButton.setEnabled(True)
            progress.finalizar()
            return

        progress.finalizar()
        self.ui.textResultado.setPlainText(resultado)
        self.ui.textFeature.setPlainText(feature_importance)
        
        pixmap = QPixmap("confusion_matriz.png")
        self.ui.labelMatriz.setPixmap(pixmap)
        self.ui.labelMatriz.setScaledContents(True)
        
        pixmap = QPixmap("curva_roc.png")
        self.ui.labelRoc.setPixmap(pixmap)
        self.ui.labelRoc.setScaledContents(True)
        
        self.ui.pushButton.setEnabled(True)
        
            
    # def select_csv_file(self):
    #     options = QtWidgets.QFileDialog.Options()
    #     file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
    #     if file_path:
    #         self.ui.textCsvPath.setText(f"{file_path}")

if __name__ == "__main__":
    import sys    
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
