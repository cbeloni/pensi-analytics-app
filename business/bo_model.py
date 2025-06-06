from abc import ABC, abstractmethod
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score

class ModeloBase(ABC):
    
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
        plt.figure(figsize=(8, 6))
        sn.heatmap(confusion_matrix, annot=True, annot_kws={"size": 10}, fmt='d')
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.savefig('confusion_matriz.png') 
        plt.close()
        
    def curva_roc(self, y_test, y_pred):  
        fpr, tpr, thresholds = roc_curve(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred)
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve: %0.2f' % roc_auc)
        plt.savefig('curva_roc.png') 
        plt.close()
    
    @abstractmethod
    def processar(self, file, alvo, progress):
        pass
