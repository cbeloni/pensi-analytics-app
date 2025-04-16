from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 900)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Main layout
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # CSV selection layout
        self.csvLayout = QtWidgets.QHBoxLayout()
        self.textCsvPath = QtWidgets.QLineEdit(self.centralwidget)
        self.textCsvPath.setObjectName("textCsvPath")
        self.csvLayout.addWidget(self.textCsvPath)

        self.buttonCsv = QtWidgets.QPushButton(self.centralwidget)
        self.buttonCsv.setObjectName("buttonCsv")
        self.csvLayout.addWidget(self.buttonCsv)

        self.mainLayout.addLayout(self.csvLayout)

        # Target variable layout
        self.targetLayout = QtWidgets.QVBoxLayout()
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.targetLayout.addWidget(self.label_2)

        self.textVariavelAlvo = QtWidgets.QLineEdit(self.centralwidget)
        self.textVariavelAlvo.setObjectName("textVariavelAlvo")
        self.targetLayout.addWidget(self.textVariavelAlvo)

        self.mainLayout.addLayout(self.targetLayout)

        # Tab widget for results
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        # Tab 1: Resultado
        self.tabResultado = QtWidgets.QWidget()
        self.tabResultado.setObjectName("tabResultado")
        self.resultLayout = QtWidgets.QVBoxLayout(self.tabResultado)
        self.textResultado = QtWidgets.QPlainTextEdit(self.tabResultado)
        self.textResultado.setObjectName("textResultado")
        self.resultLayout.addWidget(self.textResultado)
        self.tabWidget.addTab(self.tabResultado, "Resultado")

        # Tab 2: Matriz de Confusão
        self.tabMatriz = QtWidgets.QWidget()
        self.tabMatriz.setObjectName("tabMatriz")
        self.matrizLayout = QtWidgets.QVBoxLayout(self.tabMatriz)
        self.labelImagem = QtWidgets.QLabel(self.tabMatriz)
        self.labelImagem.setObjectName("labelImagem")
        self.labelImagem.setAlignment(QtCore.Qt.AlignCenter)
        self.matrizLayout.addWidget(self.labelImagem)
        self.tabWidget.addTab(self.tabMatriz, "Matriz de Confusão")
               
        # Tab 3: Resultado
        self.tabFeature = QtWidgets.QWidget()
        self.tabFeature.setObjectName("tabFeatureImportance")
        self.featureLayout = QtWidgets.QVBoxLayout(self.tabFeature)
        self.textFeature = QtWidgets.QPlainTextEdit(self.tabFeature)
        self.textFeature.setObjectName("textFeatureImportance")
        self.featureLayout.addWidget(self.textFeature)
        self.tabWidget.addTab(self.tabFeature, "Feature Importance")

        self.mainLayout.addWidget(self.tabWidget)

        # Progress bar
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setTextVisible(False)  # Hide the percentage text
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)
        self.mainLayout.addWidget(self.progressBar)

        # Process button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.mainLayout.addWidget(self.pushButton, alignment=QtCore.Qt.AlignCenter)

        MainWindow.setCentralWidget(self.centralwidget)

        # Menu bar
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

        self.retranslateUi(MainWindow)
        self.actionSair.triggered.connect(MainWindow.close)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pensi Analytics APP"))
        self.buttonCsv.setText(_translate("MainWindow", "Selecionar CSV"))
        self.pushButton.setText(_translate("MainWindow", "Processar"))
        self.label_2.setText(_translate("MainWindow", "Defina a variável alvo"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabResultado), _translate("MainWindow", "Resultado"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMatriz), _translate("MainWindow", "Matriz de Confusão"))
        self.menuSair.setTitle(_translate("MainWindow", "Configurações"))
        self.actionSair.setText(_translate("MainWindow", "Sair"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
