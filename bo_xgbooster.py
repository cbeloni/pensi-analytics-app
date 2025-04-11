import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn import metrics
import seaborn as sn
import matplotlib.pyplot as plt

def processar(file, alvo):
    df = pd.read_csv(file, sep='|')
    #df.head()

    df = pd.get_dummies(df, columns=["TP_SEXO", "DS_CID"], dtype='int')

    headers = list(df.columns)[2:]
    X = df[headers]
    y = df[alvo]  # internacao
    
    normalizar(X)
    
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=0)

    X_train, y_train = over_sampling(X_train, y_train)
        
    best_params = {'colsample_bytree': 1.0, 'learning_rate': 0.2, 'max_depth': 9, 'n_estimators': 200, 'subsample': 1.0}     
    xgb_model = XGBClassifier(**best_params, importance_type='weight')
    xgb_model.fit(X_train, y_train)
    y_pred=xgb_model.predict(X_test)
    
    matriz_confusao(y_test, y_pred)
    
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
    
    feature_importance_df = get_feature_importance(xgb_model, X)
    
    return (retorno, feature_importance_df,)
    
def over_sampling(X_train, y_train):    
    from imblearn.over_sampling import SMOTE
    smote = SMOTE()
    X_train, y_train = smote.fit_resample(X_train, y_train)
    return X_train, y_train

def normalizar(X):
    from sklearn.preprocessing import MinMaxScaler
    
    scaler = MinMaxScaler()
    colunas_normalizar = ['MP10', 'O3', 'TEMP', 'UR']
    # colunas_normalizar = ['MP10', 'O3', 'TEMP', 'UR']
    X.loc[:, colunas_normalizar] = scaler.fit_transform(X.loc[:, colunas_normalizar])
    
def matriz_confusao(y_test, y_pred):
    confusion_matrix = pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicted'])
    plt.figure(figsize=(10, 7))
    sn.heatmap(confusion_matrix, annot=True, annot_kws={"size": 10}, fmt='d')
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.savefig('confusion_matriz.png') 
    plt.close()

def get_feature_importance(xgb_model, X):    
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
    
    
if __name__ == "__main__":
    file = '/home/caue/Documentos/pensi_projeto/datasaude-ml/Regressao/dados_treino_v8_inverse.csv'
    alvo = 'internacao'
    retorno = processar(file, alvo)
    print(retorno)