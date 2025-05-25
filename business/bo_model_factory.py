from .bo_xgbooster import XgbBooster
from .bo_logistic_regression import RegressaoLogistica

modelos = {
    "XGBoost": XgbBooster,
    "Regressão Logística": RegressaoLogistica
}

def modelo_factory(model_type):
    try:
        return modelos[model_type]()
    except KeyError:
        raise ValueError(f"Tipo de modelo desconhecido: {model_type}")