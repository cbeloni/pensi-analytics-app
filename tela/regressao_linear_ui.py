from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap

from business.bo_temporal_graph import plot_temporal_graph
from business.bo_linear_regression import RegressaoLinear
import os

from utils.progress_modal import ProgressModal
from utils.modal_message_ui import MessageModal

class Ui_RegressaoLinearWindow(object):
    
    VARIAVEIS = []

    VAR_DEPENDENTE = ""
    
    def setupRegressaoLinearTab(self):
        """Configura a aba de Temporal"""
        self.tabLinearRegressao = QtWidgets.QWidget()
        self.tabLinearRegressao.setObjectName("tabLinearRegressao")
        self.RegressaoLinearLayout = QtWidgets.QVBoxLayout(self.tabLinearRegressao)

        # Layout principal com QSplitter para separador móvel
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self.tabLinearRegressao)

        # Espaço à esquerda com QListWidget para seleção de itens múltiplos
        self.leftWidget = QtWidgets.QWidget()
        self.leftLayout = QtWidgets.QVBoxLayout(self.leftWidget)
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.variaveis = QtWidgets.QListWidget(self.leftWidget)
        self.variaveis.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.variaveis.addItems(self.VARIAVEIS)
        self.leftLayout.addWidget(self.variaveis)
        self.leftWidget.setMinimumWidth(160)

        # Adiciona os botões "Habilitar" e "Desabilitar" lado a lado abaixo da lista de variáveis
        self.btnsLayout = QtWidgets.QHBoxLayout()
        self.btnHabilitar = QtWidgets.QPushButton("Habilitar", self.leftWidget)
        self.btnDesabilitar = QtWidgets.QPushButton("Desabilitar", self.leftWidget)
        self.btnsLayout.addWidget(self.btnHabilitar)
        self.btnsLayout.addWidget(self.btnDesabilitar)
        self.leftLayout.addLayout(self.btnsLayout)

        # Novo: layout horizontal para botão e campo de texto ao lado direito
        self.rightOfVariaveisWidget = QtWidgets.QWidget()
        self.rightOfVariaveisLayout = QtWidgets.QHBoxLayout(self.rightOfVariaveisWidget)
        self.rightOfVariaveisLayout.setContentsMargins(0, 0, 0, 0)

        self.btnAdicionarDependente = QtWidgets.QPushButton("Adicionar variável dependente", self.rightOfVariaveisWidget)
        self.rightOfVariaveisLayout.addWidget(self.btnAdicionarDependente)

        self.campoDependente = QtWidgets.QLineEdit(self.rightOfVariaveisWidget)
        self.campoDependente.setReadOnly(True)
        self.rightOfVariaveisLayout.addWidget(self.campoDependente)

        self.leftLayout.addWidget(self.rightOfVariaveisWidget)

        self.splitter.addWidget(self.leftWidget)

        # Widget central para os controles
        self.centralWidget = QtWidgets.QWidget()
        self.centralLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        # Layout horizontal para input e botão
        self.fileLayout = QtWidgets.QHBoxLayout()
        self.lineEditCsvLinear = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEditCsvLinear.setPlaceholderText("Selecione um arquivo CSV...")
        self.fileLayout.addWidget(self.lineEditCsvLinear)

        self.btnSelectCsvLinear = QtWidgets.QPushButton("Abrir CSV", self.centralWidget)
        self.btnSelectCsvLinear.clicked.connect(self.select_csv_file_linear)
        self.fileLayout.addWidget(self.btnSelectCsvLinear)

        self.centralLayout.addLayout(self.fileLayout)

        self.btnProcessarLinear = QtWidgets.QPushButton("Processar", self.centralWidget)
        self.btnProcessarLinear.clicked.connect(self.processar_linear)
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btnProcessarLinear)
        btn_layout.addStretch()
        self.centralLayout.addLayout(btn_layout)

        self.splitter.addWidget(self.centralWidget)

        # Define tamanhos iguais para ambos os lados
        self.splitter.setSizes([400, 600])

        self.RegressaoLinearLayout.addWidget(self.splitter)

        self.separator = QtWidgets.QFrame(self.tabLinearRegressao)
        self.separator.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.RegressaoLinearLayout.addWidget(self.separator)

        self.textResultadoLinear = QtWidgets.QPlainTextEdit(self.tabLinearRegressao)
        self.textResultadoLinear.setObjectName("textResultadoLinear")
        self.RegressaoLinearLayout.addWidget(self.textResultadoLinear)

        self.tabLinearRegressao.setLayout(self.RegressaoLinearLayout)

        self.btnAdicionarDependente.clicked.connect(self.adicionar_dependente_action)
        self.btnDesabilitar.clicked.connect(self.desabilitar_variaveis_action)
        self.btnHabilitar.clicked.connect(self.habilitar_variaveis_action)

    def desabilitar_variaveis_action(self):
        selected_items = self.variaveis.selectedItems()
        if selected_items:
            for item in selected_items:
                if " (disabled)" not in item.text():
                    item.setText(f"{item.text()} (disabled)")
    
    def habilitar_variaveis_action(self):
        selected_items = self.variaveis.selectedItems()
        if selected_items:
            for item in selected_items:
                item.setText(item.text().replace(" (disabled)", ""))

    def adicionar_dependente_action(self):
        selected_items = self.variaveis.selectedItems()
        
        if self.VAR_DEPENDENTE:
            self.variaveis.addItem(self.VAR_DEPENDENTE)
            self.VAR_DEPENDENTE = ""
        
        if selected_items:
            self.VAR_DEPENDENTE = selected_items[0].text()
            self.campoDependente.setText(self.VAR_DEPENDENTE)
            
            self.variaveis.takeItem(self.variaveis.row(selected_items[0]))
            
    def get_header_csv(self, file_path):
        """Obtém o cabeçalho do CSV para exibir no campo de variáveis."""
        if not os.path.exists(file_path):
            return []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            header = file.readline().strip().split('|')
        return header

    def select_csv_file_linear(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None, "Selecionar arquivo CSV", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.lineEditCsvLinear.setText(file_path)
            variaveis_header = self.get_header_csv(file_path)
            self.variaveis.addItems(variaveis_header)
            
    def processar_linear(self):
        if not self.campoDependente.text().strip():
            MessageModal("É necessário preencher o campo de variável dependente.").exec_()
            return
        
        progress = ProgressModal()
        progress.show()
        file_path = self.lineEditCsvLinear.text()
        linear_regression = RegressaoLinear()
        
        variaveis_lista = []
        for i in range(self.variaveis.count()):
            if "disabled" in self.variaveis.item(i).text():
                continue
            variaveis_lista.append(self.variaveis.item(i).text())
        
        dados=linear_regression.processar(file=file_path, alvo=self.campoDependente.text(), variaveis=variaveis_lista, progress=progress)
        self.textResultadoLinear.setPlainText(str(dados))
        progress.finalizar()
