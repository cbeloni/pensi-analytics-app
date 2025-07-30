from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap

from business.bo_temporal_graph import plot_temporal_graph
from business.bo_temporal_regression import treinar_modelo
import os

class Ui_TemporalWindow(object):
    
    VARIAVEIS = []
    VAR_DEPENDENTE = ""
    
    def setupTemporalTab(self):
        """Configura a aba de Temporal"""
        self.tabTemporal = QtWidgets.QWidget()
        self.tabTemporal.setObjectName("tabTemporal")
        self.temporalLayout = QtWidgets.QVBoxLayout(self.tabTemporal)

        # Layout principal com QSplitter para separador móvel
        self.splitterTemporal = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self.tabTemporal)

        # ==== Widget à esquerda ====
        self.leftWidgetTemporal = QtWidgets.QWidget()
        self.leftLayoutTemporal = QtWidgets.QVBoxLayout(self.leftWidgetTemporal)
        self.leftLayoutTemporal.setContentsMargins(0, 0, 0, 0)

        # Lista de variáveis com seleção múltipla
        self.variaveisTemporal = QtWidgets.QListWidget(self.leftWidgetTemporal)
        self.variaveisTemporal.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.variaveisTemporal.addItems(self.VARIAVEIS)
        self.leftLayoutTemporal.addWidget(self.variaveisTemporal)
        self.leftWidgetTemporal.setMinimumWidth(160)

        # Botões "Habilitar" e "Desabilitar" lado a lado
        self.btnsLayoutTemporal = QtWidgets.QHBoxLayout()
        self.btnHabilitarTemporal = QtWidgets.QPushButton("Habilitar", self.leftWidgetTemporal)
        self.btnDesabilitarTemporal = QtWidgets.QPushButton("Desabilitar", self.leftWidgetTemporal)
        self.btnsLayoutTemporal.addWidget(self.btnHabilitarTemporal)
        self.btnsLayoutTemporal.addWidget(self.btnDesabilitarTemporal)
        self.leftLayoutTemporal.addLayout(self.btnsLayoutTemporal)

        # Layout horizontal para botão e campo de texto (variável dependente)
        self.rightOfVariaveisWidgetTemporal = QtWidgets.QWidget()
        self.rightOfVariaveisLayoutTemporal = QtWidgets.QHBoxLayout(self.rightOfVariaveisWidgetTemporal)
        self.rightOfVariaveisLayoutTemporal.setContentsMargins(0, 0, 0, 0)

        self.btnAdicionarDependenteTemporal = QtWidgets.QPushButton("Adicionar variável dependente", self.rightOfVariaveisWidgetTemporal)
        self.rightOfVariaveisLayoutTemporal.addWidget(self.btnAdicionarDependenteTemporal)

        self.textVariavelDependenteTemporal = QtWidgets.QLineEdit(self.rightOfVariaveisWidgetTemporal)
        self.textVariavelDependenteTemporal.setObjectName("textVariavelDependenteTemporal")
        self.textVariavelDependenteTemporal.setReadOnly(True)
        self.rightOfVariaveisLayoutTemporal.addWidget(self.textVariavelDependenteTemporal)

        self.leftLayoutTemporal.addWidget(self.rightOfVariaveisWidgetTemporal)
        self.splitterTemporal.addWidget(self.leftWidgetTemporal)

        # ==== Widget à direita ====
        self.rightWidgetTemporal = QtWidgets.QWidget()
        self.rightLayoutTemporal = QtWidgets.QVBoxLayout(self.rightWidgetTemporal)
        self.rightLayoutTemporal.setContentsMargins(0, 0, 0, 0)

        # ==== Seleção de CSV ====
        self.fileLayout = QtWidgets.QHBoxLayout()
        self.lineEditCsv = QtWidgets.QLineEdit(self.rightWidgetTemporal)
        self.lineEditCsv.setPlaceholderText("Selecione um arquivo CSV...")
        self.fileLayout.addWidget(self.lineEditCsv)

        self.btnSelectCsv = QtWidgets.QPushButton("Abrir CSV", self.rightWidgetTemporal)
        self.btnSelectCsv.clicked.connect(self.select_csv_file)
        self.fileLayout.addWidget(self.btnSelectCsv)
        self.rightLayoutTemporal.addLayout(self.fileLayout)
        
        # Layout horizontal para "Dias Previsão" e "Dias Sazonalidade"
        self.forecastSeasonalityLayout = QtWidgets.QHBoxLayout()
        self.forecastSeasonalityLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        # Campo para inserir o valor "Dias Previsão"
        self.labelForecastDays = QtWidgets.QLabel("Dias Previsão:", self.rightWidgetTemporal)
        self.spinBoxForecastDays = QtWidgets.QSpinBox(self.rightWidgetTemporal)
        self.spinBoxForecastDays.setMinimum(1)
        self.spinBoxForecastDays.setMaximum(365)
        self.spinBoxForecastDays.setValue(90)
        self.spinBoxForecastDays.setFixedWidth(120) 
        self.forecastSeasonalityLayout.addWidget(self.labelForecastDays)
        self.forecastSeasonalityLayout.addWidget(self.spinBoxForecastDays)

        # Espaço entre os campos
        self.forecastSeasonalityLayout.addSpacing(20)

        # Campo para inserir o valor "Dias Sazonalidade"
        self.labelSeasonalityDays = QtWidgets.QLabel("Dias Sazonalidade:", self.rightWidgetTemporal)
        self.spinBoxSeasonalityDays = QtWidgets.QSpinBox(self.rightWidgetTemporal)
        self.spinBoxSeasonalityDays.setMinimum(1)
        self.spinBoxSeasonalityDays.setMaximum(365)
        self.spinBoxSeasonalityDays.setValue(160)
        self.spinBoxSeasonalityDays.setFixedWidth(120) 
        self.forecastSeasonalityLayout.addWidget(self.labelSeasonalityDays)
        self.forecastSeasonalityLayout.addWidget(self.spinBoxSeasonalityDays)
        self.forecastSeasonalityLayout.addStretch()

        self.rightLayoutTemporal.addLayout(self.forecastSeasonalityLayout)
        
        # Botão "Processar"
        self.btnProcessar = QtWidgets.QPushButton("Processar", self.rightWidgetTemporal)
        self.btnProcessar.clicked.connect(self.processar)
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btnProcessar)
        btn_layout.addStretch()
        self.rightLayoutTemporal.addLayout(btn_layout)

        self.splitterTemporal.addWidget(self.rightWidgetTemporal)
        
        # Define tamanhos iguais para ambos os lados
        self.splitterTemporal.setSizes([400, 600])
        
        self.temporalLayout.addWidget(self.splitterTemporal)
        
        # Separador visual (linha horizontal)
        self.separator = QtWidgets.QFrame(self.tabTemporal)
        self.separator.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.temporalLayout.addWidget(self.separator)
        
        # Campo de imagem
        self.imageLabel = QtWidgets.QLabel(self.tabTemporal)
        self.imageLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.imageLabel.setText("Nenhuma gráfico disponível.\nProcessar para gerar.")
        self.temporalLayout.addWidget(self.imageLabel)

        self.tabTemporal.setLayout(self.temporalLayout)

        # Conecta os botões
        self.btnAdicionarDependenteTemporal.clicked.connect(self.adicionar_dependente_temporal_action)
        self.btnDesabilitarTemporal.clicked.connect(self.desabilitar_variaveis_temporal_action)
        self.btnHabilitarTemporal.clicked.connect(self.habilitar_variaveis_temporal_action)

    def adicionar_dependente_temporal_action(self):
        selected_items = self.variaveisTemporal.selectedItems()
        
        if self.VAR_DEPENDENTE:
            self.variaveisTemporal.addItem(self.VAR_DEPENDENTE)
            self.VAR_DEPENDENTE = ""
        
        if selected_items:
            self.VAR_DEPENDENTE = selected_items[0].text()
            self.textVariavelDependenteTemporal.setText(self.VAR_DEPENDENTE)
            self.variaveisTemporal.takeItem(self.variaveisTemporal.row(selected_items[0]))

    def desabilitar_variaveis_temporal_action(self):
        selected_items = self.variaveisTemporal.selectedItems()
        if selected_items:
            for item in selected_items:
                if " (disabled)" not in item.text():
                    item.setText(f"{item.text()} (disabled)")

    def habilitar_variaveis_temporal_action(self):
        selected_items = self.variaveisTemporal.selectedItems()
        if selected_items:
            for item in selected_items:
                item.setText(item.text().replace(" (disabled)", ""))

    def get_header_csv_temporal(self, file_path):
        """Obtém o cabeçalho do CSV para exibir no campo de variáveis."""
        if not os.path.exists(file_path):
            return []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            header = file.readline().strip().split('|')
        return header

    def select_csv_file(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None, "Selecionar arquivo CSV", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.lineEditCsv.setText(file_path)
            # Limpa a lista antes de adicionar novas variáveis
            self.variaveisTemporal.clear()
            variaveis_header = self.get_header_csv_temporal(file_path)
            self.variaveisTemporal.addItems(variaveis_header)
            
    def processar(self):
        file_path = self.lineEditCsv.text()
        qtd_dias_previsao = self.spinBoxForecastDays.value()
        qtd_dias_sazonalidade = self.spinBoxSeasonalityDays.value()
        variaveisTemporal = [self.variaveisTemporal.item(i) for i in range(self.variaveisTemporal.count())]
        dados=treinar_modelo(variavel=variaveisTemporal[0].text(), dependente=self.VAR_DEPENDENTE, file_path=file_path, qtd_dias_previsao=qtd_dias_previsao, qtd_dias_sazonalidade=qtd_dias_sazonalidade)
        plot_temporal_graph(dados, output_path='temporal_graph.png')
        pixmap = QPixmap("temporal_graph.png")
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setScaledContents(True)