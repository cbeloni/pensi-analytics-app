from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap

from business.bo_temporal_graph import plot_temporal_graph
from business.bo_temporal_regression import treinar_modelo
import os

class Ui_TemporalWindow(object):
    def setupTemporalTab(self):
        """Configura a aba de Temporal"""
        self.tabTemporal = QtWidgets.QWidget()
        self.tabTemporal.setObjectName("tabTemporal")
        self.temporalLayout = QtWidgets.QVBoxLayout(self.tabTemporal)

        # Layout horizontal para input e botão
        self.fileLayout = QtWidgets.QHBoxLayout()
        self.lineEditCsv = QtWidgets.QLineEdit(self.tabTemporal)
        self.lineEditCsv.setPlaceholderText("Selecione um arquivo CSV...")
        self.fileLayout.addWidget(self.lineEditCsv)

        self.btnSelectCsv = QtWidgets.QPushButton("Abrir CSV", self.tabTemporal)
        self.btnSelectCsv.clicked.connect(self.select_csv_file)
        self.fileLayout.addWidget(self.btnSelectCsv)

        self.temporalLayout.addLayout(self.fileLayout)
        
        # Layout horizontal para "Dias Previsão" e "Dias Sazonalidade"
        self.forecastSeasonalityLayout = QtWidgets.QHBoxLayout()
        self.forecastSeasonalityLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        # Campo para inserir o valor "Dias Previsão"
        self.labelForecastDays = QtWidgets.QLabel("Dias Previsão:", self.tabTemporal)
        self.spinBoxForecastDays = QtWidgets.QSpinBox(self.tabTemporal)
        self.spinBoxForecastDays.setMinimum(1)
        self.spinBoxForecastDays.setMaximum(365)
        self.spinBoxForecastDays.setValue(90)
        self.spinBoxForecastDays.setFixedWidth(120) 
        self.forecastSeasonalityLayout.addWidget(self.labelForecastDays)
        self.forecastSeasonalityLayout.addWidget(self.spinBoxForecastDays)

        # Espaço entre os campos
        self.forecastSeasonalityLayout.addSpacing(20)

        # Campo para inserir o valor "Dias Sazonalidade"
        self.labelSeasonalityDays = QtWidgets.QLabel("Dias Sazonalidade:", self.tabTemporal)
        self.spinBoxSeasonalityDays = QtWidgets.QSpinBox(self.tabTemporal)
        self.spinBoxSeasonalityDays.setMinimum(1)
        self.spinBoxSeasonalityDays.setMaximum(365)
        self.spinBoxSeasonalityDays.setValue(160)
        self.spinBoxSeasonalityDays.setFixedWidth(120) 
        self.forecastSeasonalityLayout.addWidget(self.labelSeasonalityDays)
        self.forecastSeasonalityLayout.addWidget(self.spinBoxSeasonalityDays)

        self.temporalLayout.addLayout(self.forecastSeasonalityLayout)
        
        # Botão "Processar"
        self.btnProcessar = QtWidgets.QPushButton("Processar", self.tabTemporal)
        self.btnProcessar.clicked.connect(self.processar)
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btnProcessar)
        btn_layout.addStretch()
        self.temporalLayout.addLayout(btn_layout)
        
        # Separador visual (linha horizontal)
        self.separator = QtWidgets.QFrame(self.tabTemporal)
        self.separator.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.temporalLayout.addWidget(self.separator)
        
        # Campo de imagem
        self.imageLabel = QtWidgets.QLabel(self.tabTemporal)
        self.imageLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.imageLabel.setStyleSheet("background-color: white;")
        self.imageLabel.setText("Nenhuma gráfico disponível.\nProcessar para gerar.")

        self.temporalLayout.addWidget(self.imageLabel)

        self.tabTemporal.setLayout(self.temporalLayout)

    def select_csv_file(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None, "Selecionar arquivo CSV", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.lineEditCsv.setText(file_path)
            
    def processar(self):
        file_path = self.lineEditCsv.text()
        qtd_dias_previsao = self.spinBoxForecastDays.value()
        qtd_dias_sazonalidade = self.spinBoxSeasonalityDays.value()
        
        dados=treinar_modelo(file_path, qtd_dias_previsao, qtd_dias_sazonalidade)
        plot_temporal_graph(dados, output_path='temporal_graph.png')
        pixmap = QPixmap("temporal_graph.png")
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setScaledContents(True)