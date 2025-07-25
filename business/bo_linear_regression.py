import pandas as pd

import statsmodels.api as sm 

from business.bo_model import ModeloBase
import numpy as np

class RegressaoLinear(ModeloBase):

    def get_feature_importance(self, model, X):    
        return "Não disponível para Regressão Logística"
   
    def processar(self, file, alvo, variaveis, progress, **kwargs):
        progress.set_progress(30, "Carregando dados...")
        df = pd.read_csv(file, sep='|')
        #df.head()
        # df = pd.get_dummies(df, columns=["TP_SEXO", "DS_CID"], dtype='int', drop_first=True)

        # headers = list(df.columns)[1:]
        X = df[variaveis]
        y = df[alvo]  # internacao
        
        progress.set_progress(30, "Normalizando dados...")
        # self.normalizar(X)
        X_sm = sm.add_constant(X) 
        logit_model_sm = sm.Logit(y, X_sm)
        result_sm = logit_model_sm.fit(disp=0) # disp=0 para não imprimir o output de convergência
        p_values = result_sm.pvalues
        p_values.rename('P-Value', inplace=True)
        retorno = ""
        retorno += "\nP-Values:\n"
        retorno += p_values.to_string()
        
        progress.set_progress(30, "Gerando métricas...")
        
        # Métricas Beta e Exp(Beta)
        betas = result_sm.params
        exp_betas = betas.apply(lambda x: round(np.exp(x), 4))

        retorno += "\n\nBetas (Coeficientes):\n"
        retorno += betas.to_string()

        retorno += "\n\nExp(Beta):\n"
        retorno += exp_betas.to_string()
        
        progress.set_progress(30, "Processamento concluído!")
        return retorno
        