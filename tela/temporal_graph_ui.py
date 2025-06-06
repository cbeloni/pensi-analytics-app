import sys
import random
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import pandas as pd

class InteractiveChartApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gráfico de Linha Interativo")
        self.setGeometry(100, 100, 1000, 600)

        # Widget central
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Criando o widget do gráfico
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        # Configurando o eixo X para datas
        self.date_axis = pg.DateAxisItem(orientation='bottom')
        self.plot_widget.setAxisItems({'bottom': self.date_axis})

        # Adicionando título e legendas aos eixos
        self.plot_widget.setTitle("Valores Diários", color="k", size="15pt")
        styles = {"color": "k", "font-size": "12pt"}
        self.plot_widget.setLabel("left", "Valores", **styles)
        self.plot_widget.setLabel("bottom", "Data em dias", **styles)

        # Habilitando interatividade
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setMouseEnabled(x=True, y=True) # Habilita zoom/pan
        self.plot_widget.setLimits(yMin=0, yMax=110) # Limita o eixo Y

        # Adicionando legenda
        self.plot_widget.addLegend(offset=(-30, 30))

        # Gerando os dados
        self.plot_data()

    def plot_data(self, data_list=None):
        """
        Plota os dados no gráfico.
        Parâmetro:
            data_list: lista de dicts, cada dict deve conter:
                - 'data': string ou datetime (data)
                - 'valor_historico': valor numérico
                - 'valor_previsao': valor numérico
            Se data_list for None, gera dados aleatórios para demonstração.
        """
        # Ordena por data
        df = pd.DataFrame(data_list)
        df['data'] = pd.to_datetime(df['data'])
        df = df.sort_values('data')
        timestamps = df['data'].map(lambda d: d.timestamp()).tolist()
        data_linha1 = df['valor_historico'].tolist()
        data_linha2 = df['valor_previsao'].tolist()

        # Limpa o gráfico antes de plotar novamente
        self.plot_widget.clear()

        # Plotando as linhas
        pen1 = pg.mkPen(color=(255, 0, 0), width=2) # Vermelho
        pen2 = pg.mkPen(color=(0, 0, 255), width=2) # Azul

        self.linha1 = self.plot_widget.plot(timestamps, data_linha1, name="Histórico", pen=pen1)
        self.linha2 = self.plot_widget.plot(timestamps, data_linha2, name="Previsão", pen=pen2)

        # Adicionando marcadores (símbolos) aos pontos
        self.linha1.setSymbol('o')
        self.linha1.setSymbolSize(5)
        self.linha2.setSymbol('s')
        self.linha2.setSymbolSize(5)

        # Configurando limites iniciais do eixo X para mostrar todo o período
        if timestamps:
            self.plot_widget.setXRange(timestamps[0], timestamps[-1])

        # Adicionando linha de cruzamento (crosshair)
        vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('k', style=QtCore.Qt.DashLine))
        hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('k', style=QtCore.Qt.DashLine))
        self.plot_widget.addItem(vLine, ignoreBounds=True)
        self.plot_widget.addItem(hLine, ignoreBounds=True)

        self.proxy = pg.SignalProxy(self.plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

    def mouseMoved(self, event):
        pos = event[0]  # Posição do mouse na cena
        if self.plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = self.plot_widget.plotItem.vb.mapSceneToView(pos)
            x_val = mouse_point.x()
            y_val = mouse_point.y()

            # Atualiza as linhas de cruzamento
            vLine = self.plot_widget.items()[2] # Assumindo que vLine é o terceiro item adicionado
            hLine = self.plot_widget.items()[3] # Assumindo que hLine é o quarto item adicionado
            vLine.setPos(x_val)
            hLine.setPos(y_val)

            # Exibe as coordenadas na barra de status ou em um QLabel (opcional)
            try:
                date_str = pd.to_datetime(x_val, unit='s').strftime('%d/%m/%Y')
                self.statusBar().showMessage(f"Data: {date_str}, Valor: {y_val:.2f}")
            except (OverflowError, ValueError):
                self.statusBar().showMessage("Movendo...")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = InteractiveChartApp()
    main_window.show()
    sys.exit(app.exec_())