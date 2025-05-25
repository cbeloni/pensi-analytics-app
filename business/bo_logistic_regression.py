import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score

from business.bo_model import ModeloBase

class RegressaoLogistica(ModeloBase):

    def over_sampling(self, X_train, y_train):    
        from imblearn.over_sampling import SMOTE
        smote = SMOTE()
        X_train, y_train = smote.fit_resample(X_train, y_train)
        return X_train, y_train

    def normalizar(self, X):
        from sklearn.preprocessing import MinMaxScaler
        
        scaler = MinMaxScaler()
        colunas_normalizar = ['MP10', 'O3', 'TEMP', 'UR']
        # colunas_normalizar = ['MP10', 'O3', 'TEMP', 'UR']
        X.loc[:, colunas_normalizar] = scaler.fit_transform(X.loc[:, colunas_normalizar])
        
    def matriz_confusao(self, y_test, y_pred):
        confusion_matrix = pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicted'])
        plt.figure(figsize=(10, 7))
        sn.heatmap(confusion_matrix, annot=True, annot_kws={"size": 10}, fmt='d')
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.savefig('confusion_matriz.png') 
        plt.close()
        
    def curva_roc(self, y_test, y_pred):  
        fpr, tpr, thresholds = roc_curve(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred)
        plt.figure(figsize=(10, 7))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.savefig('curva_roc.png') 
        plt.close()

    def get_feature_importance(self, model, X):    
        return "Não disponível para Regressão Logística"
   
    def processar(self, file, alvo, progress):
        df = pd.read_csv(file, sep='|')
        #df.head()
        progress.set_progress(10)
        df = pd.get_dummies(df, columns=["TP_SEXO", "DS_CID"], dtype='int')

        headers = list(df.columns)[2:]
        X = df[headers]
        y = df[alvo]  # internacao
        
        self.normalizar(X)
        progress.set_progress(20)
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=0)

        progress.set_progress(30)
        X_train, y_train = self.over_sampling(X_train, y_train)
        
        progress.set_progress(50)
        xgb_model= LogisticRegression(max_iter=5000)
        xgb_model.fit(X_train, y_train)
        y_pred=xgb_model.predict(X_test)
        
        progress.set_progress(70)
        
        self.matriz_confusao(y_test, y_pred)
        
        
        progress.set_progress(80)
        self.curva_roc(y_test, y_pred)
        
        progress.set_progress(90)
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
        progress.set_progress(100)
        return (retorno, feature_importance_df,)
        
 
    
if __name__ == "__main__":
    file = '/home/caue/Documentos/pensi_projeto/datasaude-ml/Regressao/dados_treino_v8_inverse.csv'
    alvo = 'internacao'
    
    retorno = RegressaoLogistica().processar(file, alvo)
    print(retorno)