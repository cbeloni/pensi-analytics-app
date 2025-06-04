from PyQt5 import QtCore, QtWidgets

class Ui_TemporalWindow(object):
    def setupTemporalTab(self):
        """Configura a aba de Temporal"""
        self.tabTemporal = QtWidgets.QWidget()
        self.tabTemporal.setObjectName("tabTemporal")
        self.temporalLayout = QtWidgets.QVBoxLayout(self.tabTemporal)
        self.labelTemporal = QtWidgets.QLabel("Conteúdo da Aba Temporal", self.tabTemporal)
        self.labelTemporal.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.temporalLayout.addWidget(self.labelTemporal)
        self.tabTemporal.setLayout(self.temporalLayout)