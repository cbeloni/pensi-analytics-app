from datetime import datetime
import matplotlib.pyplot as plt

def plot_temporal_graph(dados, output_path='temporal_graph.png'):
    """
    Plota um gráfico temporal com valores históricos e de previsão.

    :param dados: Lista de dicionários com as chaves 'data', 'valor_historico' e 'valor_previsao'
    :param output_path: Caminho do arquivo de saída para salvar o gráfico
    """
    datas = [datetime.strptime(item['data'], '%Y-%m-%d') for item in dados]
    valores_historicos = [item['valor_historico'] for item in dados]
    valores_previsao = [item['valor_previsao'] for item in dados]

    plt.figure(figsize=(8, 6))
    plt.plot(datas, valores_historicos, marker='o', label='Valor Histórico')
    plt.plot(datas, valores_previsao, marker='o', label='Valor Previsão')
    plt.xlabel('Data')
    plt.ylabel('Valor')
    plt.title('Gráfico Regressão por Período')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
