import time
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn import metrics

from business.bo_model import ModeloBase
from PyQt5.QtWidgets import QApplication

_HIPERPARAMETROS_DEFAULT = {'colsample_bytree': 1.0, 'learning_rate': 0.2, 'max_depth': 9, 'n_estimators': 200, 'subsample': 1.0}

class XgbBooster(ModeloBase):
    
    def get_feature_importance(self, xgb_model, X):    
        feature_importances = xgb_model.feature_importances_
        feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importances})
        feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
        features_formated = ""

        linhas = feature_importance_df.to_string(index=False).split('\n')[1:]

        for linha in linhas:
            linha = linha.strip() 
            if linha:
                features_formated += linha + "\n"
        
        return features_formated
   
    def processar(self, file, alvo, progress, **kwargs):
        
        hiperametros = kwargs.get('hiperametros', None)
        df = pd.read_csv(file, sep='|')
        #df.head()
        progress.set_progress(10, "Carregando dados...")
        df = pd.get_dummies(df, columns=["TP_SEXO", "DS_CID"], dtype='int')

        headers = list(df.columns)[2:]
        X = df[headers]
        y = df[alvo]  # internacao
        
        progress.set_progress(10, "Normalizando dados...")
        self.normalizar(X)
        
        progress.set_progress(10, "Dividindo dados em treino e teste...")
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=0)

        progress.set_progress(10,   "Aplicando over-sampling...")
        X_train, y_train = self.over_sampling(X_train, y_train)
        
        progress.set_progress(20, "Treinando modelo XGBoost...")
        best_params = hiperametros or _HIPERPARAMETROS_DEFAULT
        xgb_model = XGBClassifier(**best_params, importance_type='weight')
        xgb_model.fit(X_train, y_train)
        y_pred=xgb_model.predict(X_test)
                
        progress.set_progress(10,   "Gerando matriz de confusão...")
        self.matriz_confusao(y_test, y_pred)
                
        progress.set_progress(20,  "Gerando curva ROC...")
        self.curva_roc(y_test, y_pred)
        
        retorno = f'Accuracy: {metrics.accuracy_score(y_test, y_pred)} \n'

        recall = metrics.recall_score(y_test, y_pred)
        retorno += f'Sensitivity (Recall): {recall} \n'

        tn, fp, fn, tp = metrics.confusion_matrix(y_test, y_pred).ravel()
        specificity = tn / (tn+fp)

        retorno +=  f'Specificity: {specificity} \n'

        precision = tp / (tp + fp)
        retorno += f'Precision: {precision} \n'

        NPV = tn / (tn + fn)
        retorno += f'NPV: {NPV} \n'
        
        feature_importance_df = self.get_feature_importance(xgb_model, X)
        progress.set_progress(100, "Processamento concluído!")
        return (retorno, feature_importance_df,)
        
 
    
if __name__ == "__main__":
    file = '/home/caue/Documentos/pensi_projeto/datasaude-ml/Regressao/dados_treino_v8_inverse.csv'
    alvo = 'internacao'
    
    retorno = XgbBooster().processar(file, alvo)
    print(retorno)