from abc import ABC, abstractmethod

class ModeloBase(ABC):
    @abstractmethod
    def processar(self, file, alvo, progress):
        pass
