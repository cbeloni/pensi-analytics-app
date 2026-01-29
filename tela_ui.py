from PyQt5 import QtCore, QtWidgets
from tela.temporal_ui import Ui_TemporalWindow
from tela.regressao_linear_ui import Ui_RegressaoLinearWindow
import yaml
import os
import logging

hiperparams = {}
try:
    yaml_path = os.getenv("HIPERPARAMS_YAML_PATH", os.path.join(os.path.dirname(__file__), "hiperparametros.yaml"))
    with open(yaml_path, "r", encoding="utf-8") as f:
        hiperparams = yaml.safe_load(f)
except FileNotFoundError:
    logging.error(f"Arquivo de hiperparâmetros não encontrado: {yaml_path}")
    
_HIPERPARAMS_XGB = str(hiperparams.get("xgboost", {}))
_HIPERPARAMS_LOGISTIC = str(hiperparams.get("logistic_regression", {}))

class Ui_MainWindow(Ui_TemporalWindow, Ui_RegressaoLinearWindow):
    
    def __init__(self):
        super().__init__()
        Ui_TemporalWindow.__init__(self)
        Ui_RegressaoLinearWindow.__init__(self)
        
    
    def setupUi(self, MainWindow):
        # Configurações iniciais da janela principal
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 900)
        # Centraliza a janela na tela
        qr = MainWindow.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        MainWindow.move(qr.topLeft())

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Widget de abas principal
        self.mainTabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.mainTabWidget.setObjectName("mainTabWidget")

        # ==== ABA: Classificação ====
        self.setupClassificacaoTab()

        # ==== ABA: Temporal ====
        self.setupTemporalTab()

        self.setupRegressaoLinearTab()

        # Adiciona as abas ao widget principal
        self.mainTabWidget.addTab(self.tabClassificacao, "Classificação")
        self.mainTabWidget.addTab(self.tabTemporal, "Temporal")
        self.mainTabWidget.addTab(self.tabLinearRegressao, "Regressão Linear")

        # Centraliza o widget de abas
        layout = QtWidgets.QVBoxLayout(self.centralwidget)
        layout.addWidget(self.mainTabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        # Menu superior e barra de status
        self.setupMenu(MainWindow)

        # Tradução de textos e conexão de ações
        self.retranslateUi(MainWindow)
        self.actionSair.triggered.connect(MainWindow.close)  # Fecha app ao clicar em "Sair"

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setupClassificacaoTab(self):
        """Configura a aba de Classificação"""
        self.tabClassificacao = QtWidgets.QWidget()
        self.tabClassificacao.setObjectName("tabClassificacao")
        self.classificacaoLayout = QtWidgets.QVBoxLayout(self.tabClassificacao)

        # Layout principal com QSplitter para separador móvel
        self.splitterClassificacao = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self.tabClassificacao)

        # ==== Widget à esquerda ====
        self.leftWidgetClassificacao = QtWidgets.QWidget()
        self.leftLayoutClassificacao = QtWidgets.QVBoxLayout(self.leftWidgetClassificacao)
        self.leftLayoutClassificacao.setContentsMargins(0, 0, 0, 0)

        # Lista de variáveis com seleção múltipla
        self.variaveisClassificacao = QtWidgets.QListWidget(self.leftWidgetClassificacao)
        self.variaveisClassificacao.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.leftLayoutClassificacao.addWidget(self.variaveisClassificacao)
        self.leftWidgetClassificacao.setMinimumWidth(160)

        # Botões "Habilitar" e "Desabilitar" lado a lado
        self.btnsLayoutClassificacao = QtWidgets.QHBoxLayout()
        self.btnHabilitarClassificacao = QtWidgets.QPushButton("Habilitar", self.leftWidgetClassificacao)
        self.btnDesabilitarClassificacao = QtWidgets.QPushButton("Desabilitar", self.leftWidgetClassificacao)
        self.btnsLayoutClassificacao.addWidget(self.btnHabilitarClassificacao)
        self.btnsLayoutClassificacao.addWidget(self.btnDesabilitarClassificacao)
        self.leftLayoutClassificacao.addLayout(self.btnsLayoutClassificacao)

        # Layout horizontal para botão e campo de texto (variável alvo)
        self.rightOfVariaveisWidgetClassificacao = QtWidgets.QWidget()
        self.rightOfVariaveisLayoutClassificacao = QtWidgets.QHBoxLayout(self.rightOfVariaveisWidgetClassificacao)
        self.rightOfVariaveisLayoutClassificacao.setContentsMargins(0, 0, 0, 0)

        self.btnAdicionarAlvoClassificacao = QtWidgets.QPushButton("Adicionar variável alvo", self.rightOfVariaveisWidgetClassificacao)
        self.rightOfVariaveisLayoutClassificacao.addWidget(self.btnAdicionarAlvoClassificacao)

        self.textVariavelAlvo = QtWidgets.QLineEdit(self.rightOfVariaveisWidgetClassificacao)
        self.textVariavelAlvo.setObjectName("textVariavelAlvo")
        self.textVariavelAlvo.setReadOnly(True)
        self.rightOfVariaveisLayoutClassificacao.addWidget(self.textVariavelAlvo)

        self.leftLayoutClassificacao.addWidget(self.rightOfVariaveisWidgetClassificacao)

        self.splitterClassificacao.addWidget(self.leftWidgetClassificacao)

        # ==== Widget à direita ====
        self.rightWidgetClassificacao = QtWidgets.QWidget()
        self.rightLayoutClassificacao = QtWidgets.QVBoxLayout(self.rightWidgetClassificacao)
        self.rightLayoutClassificacao.setContentsMargins(0, 0, 0, 0)

        # ==== Seleção de CSV ====
        self.csvLayout = QtWidgets.QHBoxLayout()
        self.textCsvPath = QtWidgets.QLineEdit(self.rightWidgetClassificacao)
        self.textCsvPath.setObjectName("textCsvPath")
        self.textCsvPath.setPlaceholderText("Selecione um arquivo CSV...")
        self.buttonCsv = QtWidgets.QPushButton("Selecionar CSV", self.rightWidgetClassificacao)
        self.buttonCsv.setObjectName("buttonCsv")
        self.buttonCsv.clicked.connect(self.select_csv_file_classificacao)  # Conecta o botão
        self.csvLayout.addWidget(self.textCsvPath)
        self.csvLayout.addWidget(self.buttonCsv)
        self.rightLayoutClassificacao.addLayout(self.csvLayout)

        # ==== Seleção do Modelo e Hiperparâmetros ====
        self.modelTargetLayout = QtWidgets.QHBoxLayout()

        # Seleção do Modelo
        self.labelModelo = QtWidgets.QLabel(self.rightWidgetClassificacao)
        self.labelModelo.setObjectName("labelModelo")
        self.comboBoxModelo = QtWidgets.QComboBox(self.rightWidgetClassificacao)
        self.comboBoxModelo.setObjectName("comboBoxModelo")
        self.comboBoxModelo.addItems(["XGBoost", "Regressão Logística"])
        self.comboBoxModelo.setFixedWidth(180)
        self.comboBoxModelo.currentTextChanged.connect(self.change_model_action)

        # Hiperparâmetros
        self.labelHiperparam = QtWidgets.QLabel(self.rightWidgetClassificacao)
        self.labelHiperparam.setObjectName("labelHiperparam")
        self.labelHiperparam.setText("Hiperparâmetros")
        self.textHiperparam = QtWidgets.QLineEdit(self.rightWidgetClassificacao)
        self.textHiperparam.setObjectName("textHiperparam")
        self.textHiperparam.setText(_HIPERPARAMS_XGB)
        self.textHiperparam.setFixedWidth(250)

        # Adiciona widgets ao layout horizontal
        self.modelTargetLayout.addWidget(self.labelModelo)
        self.modelTargetLayout.addWidget(self.comboBoxModelo)
        self.modelTargetLayout.addSpacing(30)
        self.modelTargetLayout.addWidget(self.labelHiperparam)
        self.modelTargetLayout.addWidget(self.textHiperparam)
        self.modelTargetLayout.addStretch()

        self.rightLayoutClassificacao.addLayout(self.modelTargetLayout)

        # ==== Botão de Processamento ====
        self.pushButton = QtWidgets.QPushButton("Processar", self.rightWidgetClassificacao)
        self.pushButton.setObjectName("pushButton")
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.pushButton)
        btn_layout.addStretch()
        self.rightLayoutClassificacao.addLayout(btn_layout)

        self.splitterClassificacao.addWidget(self.rightWidgetClassificacao)

        # Define tamanhos iguais para ambos os lados
        self.splitterClassificacao.setSizes([400, 600])

        self.classificacaoLayout.addWidget(self.splitterClassificacao)

        # ==== Separador ====
        self.separator = QtWidgets.QFrame(self.tabClassificacao)
        self.separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.classificacaoLayout.addWidget(self.separator)

        # ==== Sub-Abas de Resultados ====
        self.tabWidget = QtWidgets.QTabWidget(self.tabClassificacao)
        self.tabWidget.setObjectName("tabWidget")

        # Sub-aba: Resultado
        self.setupSubTabResultado()
        # Sub-aba: Matriz de Confusão
        self.setupSubTabMatriz()
        # Sub-aba: Feature Importance
        self.setupSubTabFeature()
        # Sub-aba: Curva ROC
        self.setupSubTabRoc()

        self.classificacaoLayout.addWidget(self.tabWidget)

        # Finaliza layout da aba
        self.tabClassificacao.setLayout(self.classificacaoLayout)

        # Conecta os botões
        self.btnAdicionarAlvoClassificacao.clicked.connect(self.adicionar_alvo_action)
        self.btnDesabilitarClassificacao.clicked.connect(self.desabilitar_variaveis_classificacao_action)
        self.btnHabilitarClassificacao.clicked.connect(self.habilitar_variaveis_classificacao_action)

    def setupSubTabResultado(self):
        self.tabResultado = QtWidgets.QWidget()
        self.tabResultado.setObjectName("tabResultado")
        self.resultLayout = QtWidgets.QVBoxLayout(self.tabResultado)
        self.textResultado = QtWidgets.QPlainTextEdit(self.tabResultado)
        self.textResultado.setObjectName("textResultado")
        self.resultLayout.addWidget(self.textResultado)
        self.tabWidget.addTab(self.tabResultado, "Resultado")

    def setupSubTabMatriz(self):
        self.tabMatriz = QtWidgets.QWidget()
        self.tabMatriz.setObjectName("tabMatriz")
        self.matrizLayout = QtWidgets.QVBoxLayout(self.tabMatriz)
        self.labelMatriz = QtWidgets.QLabel(self.tabMatriz)
        self.labelMatriz.setObjectName("labelMatriz")
        self.labelMatriz.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.matrizLayout.addWidget(self.labelMatriz)
        self.tabWidget.addTab(self.tabMatriz, "Matriz de Confusão")

    def setupSubTabFeature(self):
        self.tabFeature = QtWidgets.QWidget()
        self.tabFeature.setObjectName("tabFeatureImportance")
        self.featureLayout = QtWidgets.QVBoxLayout(self.tabFeature)
        self.textFeature = QtWidgets.QPlainTextEdit(self.tabFeature)
        self.textFeature.setObjectName("textFeatureImportance")
        self.featureLayout.addWidget(self.textFeature)
        self.tabWidget.addTab(self.tabFeature, "Feature Importance")

    def setupSubTabRoc(self):
        self.tabRoc = QtWidgets.QWidget()
        self.tabRoc.setObjectName("tabRoc")
        self.rocLayout = QtWidgets.QVBoxLayout(self.tabRoc)
        self.labelRoc = QtWidgets.QLabel(self.tabRoc)
        self.labelRoc.setObjectName("labelRoc")
        self.labelRoc.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.rocLayout.addWidget(self.labelRoc)
        self.tabWidget.addTab(self.tabRoc, "Curva ROC")

    def setupMenu(self, MainWindow):
        """Configura o menu superior e barra de status"""
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")

        self.menuSair = QtWidgets.QMenu(self.menubar)
        self.menuSair.setObjectName("menuSair")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionSair = QtWidgets.QAction(MainWindow)
        self.actionSair.setObjectName("actionSair")

        self.menuSair.addAction(self.actionSair)
        self.menubar.addAction(self.menuSair.menuAction())

    def retranslateUi(self, MainWindow):
        """Define textos dos widgets"""
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pensi Analytics APP"))
        self.buttonCsv.setText(_translate("MainWindow", "Abrir CSV"))
        self.pushButton.setText(_translate("MainWindow", "Processar"))
        # self.label_2.setText(_translate("MainWindow", "Defina a variável alvo"))
        self.labelModelo.setText(_translate("MainWindow", "Seleciona o Modelo"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabResultado), _translate("MainWindow", "Resultado"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMatriz), _translate("MainWindow", "Matriz de Confusão"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFeature), _translate("MainWindow", "Feature Importance"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabRoc), _translate("MainWindow", "Curva ROC"))

        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.tabClassificacao), _translate("MainWindow", "Classificação"))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.tabTemporal), _translate("MainWindow", "Temporal"))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.tabLinearRegressao), _translate("MainWindow", "Regressão Linear"))

        self.menuSair.setTitle(_translate("MainWindow", "Configurações"))
        self.actionSair.setText(_translate("MainWindow", "Sair"))
    
    def change_model_action(self, model_name):
        if model_name == "XGBoost":
            self.textHiperparam.setText(_HIPERPARAMS_XGB)
        elif model_name == "Regressão Logística":
            self.textHiperparam.setText(_HIPERPARAMS_LOGISTIC)

    def adicionar_alvo_action(self):
        selected_items = self.variaveisClassificacao.selectedItems()
        
        if hasattr(self, 'VAR_ALVO_CLASSIFICACAO') and self.VAR_ALVO_CLASSIFICACAO:
            self.variaveisClassificacao.addItem(self.VAR_ALVO_CLASSIFICACAO)
            self.VAR_ALVO_CLASSIFICACAO = ""
        
        if selected_items:
            self.VAR_ALVO_CLASSIFICACAO = selected_items[0].text()
            self.textVariavelAlvo.setText(self.VAR_ALVO_CLASSIFICACAO)
            self.variaveisClassificacao.takeItem(self.variaveisClassificacao.row(selected_items[0]))

    def desabilitar_variaveis_classificacao_action(self):
        selected_items = self.variaveisClassificacao.selectedItems()
        if selected_items:
            for item in selected_items:
                if " (disabled)" not in item.text():
                    item.setText(f"{item.text()} (disabled)")

    def habilitar_variaveis_classificacao_action(self):
        selected_items = self.variaveisClassificacao.selectedItems()
        if selected_items:
            for item in selected_items:
                item.setText(item.text().replace(" (disabled)", ""))

    def get_header_csv_classificacao(self, file_path):
        """Obtém o cabeçalho do CSV para exibir no campo de variáveis."""
        if not os.path.exists(file_path):
            return []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            header = file.readline().strip().split('|')
        return header

    def select_csv_file_classificacao(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None, "Selecionar arquivo CSV", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.textCsvPath.setText(file_path)
            # Limpa a lista antes de adicionar novas variáveis
            self.variaveisClassificacao.clear()
            variaveis_header = self.get_header_csv_classificacao(file_path)
            self.variaveisClassificacao.addItems(variaveis_header)

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
