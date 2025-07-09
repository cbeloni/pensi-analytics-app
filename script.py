from business.bo_logistic_regression import RegressaoLogistica

class Progress:
    def __init__(self):
        self.value = 0

    def set_progress(self, value, message=None):
        self.value = value
        print(f"message: {message}%")

if __name__ == "__main__":
    file = '/Users/cauebeloni/Documents/Projeto Pensi/pensi-analytics-app/dados_treino_linear.csv'
    alvo = 'internacao'
    
    retorno = RegressaoLogistica().processar(file, alvo, Progress())
    print(retorno)