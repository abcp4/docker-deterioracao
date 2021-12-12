""" Módulo principal da API de predição
"""
from enum import Enum
from typing import Optional

import joblib
import numpy as np
from binning import binning
from fastapi import FastAPI

description = """
# Desafio Machine Learning Engineer. 🚀

API para predição do motivo de alta de pacientes, com base em:

- idade
- setor
- temperatura
- frequência respiratória
- pressão arterial sistólica
- pressão arterial diastólica
- pressão arterial média
- saturação da oxigenação

O motivo de alta assumido é:
- Óbito
- Melhorado

"""

app = FastAPI(
    title="PredictAPI",
    description=description,
    version="0.0.1",
    contact={
        "name": "Ivan Pereira",
        "email": "navi1921@gmail.com",
    },
)


model = joblib.load("models/xgb_model.joblib")
label_encoder = joblib.load("models/le.joblib")
scaler = joblib.load("models/scaler.joblib")

nosection_model = joblib.load("models/nosection_xgb_model.joblib")
nosection_scaler = joblib.load("models/nosection_scaler.joblib")


class SectorName(str, Enum):
    sector_UTIG = "UTIG"
    sector_1AP2 = "1AP2"
    sector_4AP2 = "4AP2"
    sector_UTIC = "UTIC"
    sector_UTIP = "UTIP"
    sector_3AP1 = "3AP1"
    sector_3AP2 = "3AP2"
    sector_4AP1 = "4AP1"
    sector_1AP1 = "1AP1"
    sector_2AP2 = "2AP2"
    sector_UIP = "UIP"
    sector_3AP3 = "3AP3"
    sector_1AP2_126 = "1AP2 - 126"
    sector_2AP1 = "2AP1"
    sector_3AP3_EPI = "3AP3 - EPI"
    sector_SEMI_CO = "SEMI-CO"


@app.get("/predict")
def predict_data(
    age: int,
    temperature: float,
    respiratory_frequency: float,
    systolic_blood_pressure: float,
    diastolic_blood_pressure: float,
    mean_arterial_pressure: float,
    oxygen_saturation: float,
    sector: Optional[SectorName] = None,
):
    """Informe os dados do paciente que deseja obter uma predição."""
    if sector is not None:
        sector = sector.value
        sector_encoded = label_encoder.transform([sector])
        features = [
            age,
            sector_encoded.item(),
            temperature,
            respiratory_frequency,
            systolic_blood_pressure,
            diastolic_blood_pressure,
            mean_arterial_pressure,
            oxygen_saturation,
        ]
    else:
        features = [
            age,
            0,
            temperature,
            respiratory_frequency,
            systolic_blood_pressure,
            diastolic_blood_pressure,
            mean_arterial_pressure,
            oxygen_saturation,
        ]

    extra_features = binning(features)
    features.extend(list(extra_features.flatten()))

    features_np = np.asarray(features, dtype=np.float64)
    if sector is not None:
        features_np = scaler.transform([features_np])
        y_pred = model.predict(features_np)
        return {"predict": y_pred[0], "features": features}
    else:
        print(features_np)
        features_np = np.delete(features_np, 1)
        print(features_np)
        features_np = nosection_scaler.transform([features_np])
        y_pred = nosection_model.predict(features_np)
        features = [features[0]] + features[2:]
        print(features)
        return {"predict": y_pred[0], "features": features}
