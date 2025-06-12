from PyQt5 import QtCore, QtWidgets
from tela.temporal_ui import Ui_TemporalWindow

class Ui_MainWindow(Ui_TemporalWindow):
    def __init__(self):
        super().__init__()
        Ui_TemporalWindow.__init__(self)
    
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

        # Adiciona as abas ao widget principal
        self.mainTabWidget.addTab(self.tabClassificacao, "Classificação")
        self.mainTabWidget.addTab(self.tabTemporal, "Temporal")

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

        # Layout principal da aba
        self.mainLayout = QtWidgets.QVBoxLayout()

        # ==== Seleção de CSV ====
        self.csvLayout = QtWidgets.QHBoxLayout()
        self.textCsvPath = QtWidgets.QLineEdit(self.tabClassificacao)
        self.textCsvPath.setObjectName("textCsvPath")
        self.textCsvPath.setPlaceholderText("Selecione um arquivo CSV...")
        self.buttonCsv = QtWidgets.QPushButton(self.tabClassificacao)
        self.buttonCsv.setObjectName("buttonCsv")
        self.csvLayout.addWidget(self.textCsvPath)
        self.csvLayout.addWidget(self.buttonCsv)
        self.mainLayout.addLayout(self.csvLayout)

        # ==== Seleção do Modelo e Variável Alvo (alinhados horizontalmente) ====
        self.modelTargetLayout = QtWidgets.QHBoxLayout()

        # Seleção do Modelo
        self.labelModelo = QtWidgets.QLabel(self.tabClassificacao)
        self.labelModelo.setObjectName("labelModelo")
        self.comboBoxModelo = QtWidgets.QComboBox(self.tabClassificacao)
        self.comboBoxModelo.setObjectName("comboBoxModelo")
        self.comboBoxModelo.addItems(["XGBoost", "Regressão Logística"])
        self.comboBoxModelo.setFixedWidth(180)

        # Variável Alvo
        self.label_2 = QtWidgets.QLabel(self.tabClassificacao)
        self.label_2.setObjectName("label_2")
        self.textVariavelAlvo = QtWidgets.QLineEdit(self.tabClassificacao)
        self.textVariavelAlvo.setObjectName("textVariavelAlvo")
        self.textVariavelAlvo.setFixedWidth(250)

        # Adiciona widgets ao layout horizontal
        self.modelTargetLayout.addWidget(self.labelModelo)
        self.modelTargetLayout.addWidget(self.comboBoxModelo)
        self.modelTargetLayout.addSpacing(30)
        self.modelTargetLayout.addWidget(self.label_2)
        self.modelTargetLayout.addWidget(self.textVariavelAlvo)
        self.modelTargetLayout.addStretch()

        self.mainLayout.addLayout(self.modelTargetLayout)
        
        # ==== Botão de Processamento ====
        self.pushButton = QtWidgets.QPushButton(self.tabClassificacao)
        self.pushButton.setObjectName("pushButton")
        self.mainLayout.addWidget(self.pushButton, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)


        # ==== Separador ====
        self.separator = QtWidgets.QFrame(self.tabClassificacao)
        self.separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.mainLayout.addWidget(self.separator)
        
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

        self.mainLayout.addWidget(self.tabWidget)

        # Finaliza layout da aba
        self.classificacaoLayout.addLayout(self.mainLayout)
        self.tabClassificacao.setLayout(self.classificacaoLayout)

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
        self.label_2.setText(_translate("MainWindow", "Defina a variável alvo"))
        self.labelModelo.setText(_translate("MainWindow", "Seleciona o Modelo"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabResultado), _translate("MainWindow", "Resultado"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMatriz), _translate("MainWindow", "Matriz de Confusão"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFeature), _translate("MainWindow", "Feature Importance"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabRoc), _translate("MainWindow", "Curva ROC"))

        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.tabClassificacao), _translate("MainWindow", "Classificação"))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.tabTemporal), _translate("MainWindow", "Temporal"))

        self.menuSair.setTitle(_translate("MainWindow", "Configurações"))
        self.actionSair.setText(_translate("MainWindow", "Sair"))

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
