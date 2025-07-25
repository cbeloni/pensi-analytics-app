from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

class WorkerSignals(QObject):
    finished = pyqtSignal(object, object)
    error = pyqtSignal(str)

class Worker(QRunnable):
    def __init__(self, model, csv_path, variavel_alvo, progress):
        super().__init__()
        self.model = model
        self.csv_path = csv_path
        self.variavel_alvo = variavel_alvo
        self.progress = progress
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            resultado, feature_importance = self.model.processar(self.csv_path, self.variavel_alvo, self.progress)
            self.signals.finished.emit(resultado, feature_importance)
        except Exception as e:
            self.signals.error.emit(str(e))