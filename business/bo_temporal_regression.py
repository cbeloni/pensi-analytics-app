import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from utils.progress_modal import ProgressModal

def load_df(file_path: str):
    df = pd.read_csv(file_path, sep='|')
    return df

def treinar_modelo(variavel: str, dependente: str, file_path: str, qtd_dias_previsao: int, qtd_dias_sazonalidade: int): 
    progress = ProgressModal()
    progress.show()
    progress.set_progress(25, "Carregando dados...")
    df = load_df(file_path)
    # print(df.head().to_dict(orient='records'))
    df[variavel] = pd.to_datetime(df[variavel])
    df.set_index(variavel, inplace=True)
    ts = df[dependente]
    
    progress.set_progress(25, "Treinando modelo de previsão...")
    model = ExponentialSmoothing(ts, trend='add', seasonal='add', seasonal_periods=qtd_dias_sazonalidade).fit()
    forecast = model.forecast(steps=qtd_dias_previsao)
    forecast_df = pd.DataFrame({
        'data': forecast.index.strftime('%Y-%m-%d'),
        'valor_previsao': forecast.values
    })
    result = []
    progress.set_progress(25, "Gerando resultados...")
    for idx, row in df.iterrows():
        try:
            data = idx.strftime('%Y-%m-%d')
            valor_historico = int(row[dependente])
            paciente_historico = { "data": data, "valor_historico": valor_historico, "valor_previsao": None }
            result.append(paciente_historico)
        except:
            continue
    
    for forecast_dt in forecast_df.iterrows():
        try:
            data = forecast_dt[1]['data']
            valor_previsao = int(forecast_dt[1]['valor_previsao'])
            paciente_previsao = { "data": data, "valor_historico": None, "valor_previsao": valor_previsao }
            result.append(paciente_previsao)
        except:
            continue
    
    progress.set_progress(25, "Processamento concluído!")
    progress.finalizar()
    return result