import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

from business.bo_model import ModeloBase

class RegressaoLogistica(ModeloBase):

    def get_feature_importance(self, model, X):    
        return "Não disponível para Regressão Logística"
   
    def processar(self, file, alvo, progress):
        progress.set_progress(10, "Carregando dados...")
        df = pd.read_csv(file, sep='|')
        #df.head()
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
        
        progress.set_progress(20, "Treinando modelo Regressão logística...")
        xgb_model = LogisticRegression()
        xgb_model.fit(X_train, y_train)
        y_pred=xgb_model.predict(X_test)
        
        
        progress.set_progress(20,   "Gerando matriz de confusão...")
        self.matriz_confusao(y_test, y_pred)
                
        progress.set_progress(10,  "Gerando curva ROC...")
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