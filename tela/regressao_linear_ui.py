from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap

from business.bo_temporal_graph import plot_temporal_graph
from business.bo_linear_regression import RegressaoLinear
import os

from utils.progress_modal import ProgressModal

class Ui_RegressaoLinearWindow(object):
    
    def setupRegressaoLinearTab(self):
        """Configura a aba de Temporal"""
        self.tabLinearRegressao = QtWidgets.QWidget()
        self.tabLinearRegressao.setObjectName("tabLinearRegressao")
        self.RegressaoLinearLayout = QtWidgets.QVBoxLayout(self.tabLinearRegressao)

        # Layout horizontal para input e botão
        self.fileLayout = QtWidgets.QHBoxLayout()
        self.lineEditCsvLinear = QtWidgets.QLineEdit(self.tabLinearRegressao)
        self.lineEditCsvLinear.setPlaceholderText("Selecione um arquivo CSV...")
        self.fileLayout.addWidget(self.lineEditCsvLinear)

        self.btnSelectCsvLinear = QtWidgets.QPushButton("Abrir CSV", self.tabLinearRegressao)
        self.btnSelectCsvLinear.clicked.connect(self.select_csv_file_linear)
        self.fileLayout.addWidget(self.btnSelectCsvLinear)

        self.RegressaoLinearLayout.addLayout(self.fileLayout)
        
        # Botão "Processar"
        self.btnProcessarLinear = QtWidgets.QPushButton("Processar", self.tabLinearRegressao)
        self.btnProcessarLinear.clicked.connect(self.processar_linear)
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btnProcessarLinear)
        btn_layout.addStretch()
        self.RegressaoLinearLayout.addLayout(btn_layout)
        
        # Separador visual (linha horizontal)
        self.separator = QtWidgets.QFrame(self.tabLinearRegressao)
        self.separator.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.RegressaoLinearLayout.addWidget(self.separator)
        
        # Campo de resultado
        self.textResultadoLinear = QtWidgets.QPlainTextEdit(self.tabLinearRegressao)
        self.textResultadoLinear.setObjectName("textResultadoLinear")
        self.RegressaoLinearLayout.addWidget(self.textResultadoLinear)

        self.tabLinearRegressao.setLayout(self.RegressaoLinearLayout)

    def select_csv_file_linear(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None, "Selecionar arquivo CSV", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.lineEditCsvLinear.setText(file_path)
            
    def processar_linear(self):
        progress = ProgressModal()
        progress.show()
        file_path = self.lineEditCsvLinear.text()
        linear_regression = RegressaoLinear()
        
        dados=linear_regression.processar(file=file_path, alvo="internacao", progress=progress)
        self.textResultadoLinear.setPlainText(str(dados))
        progress.finalizar()
