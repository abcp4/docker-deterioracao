""" Módulo principal da API de predição
"""
import joblib
from fastapi import FastAPI
from pydantic import BaseModel, validator
from binning import binning
import numpy as np
import xgboost
import shap
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

@app.get("/predict")
def predict_data(age: int,
                sector: str,
                temperature: float,
                respiratory_frequency: float,
                systolic_blood_pressure: float,
                diastolic_blood_pressure: float,
                mean_arterial_pressure: float,
                oxygen_saturation: float
                ):
    """Informe os dados do paciente que deseja obter uma predição."""
    if(sector != 'Nenhum'):
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

    extra_features=binning(features)
    features.extend(list(extra_features.flatten()))
    
    features_np=np.asarray(features,dtype=np.float64)
    if(sector != 'Nenhum'):
        features_np=scaler.transform([features_np])
        y_pred = model.predict(features_np)
        return {"predict": y_pred[0],'features': features}
    else:
        print(features_np)
        features_np=np.delete(features_np, 1)
        print(features_np)
        features_np=nosection_scaler.transform([features_np])
        y_pred = nosection_model.predict(features_np)
        features=[features[0]]+features[2:]
        print(features)
        return {"predict": y_pred[0],'features': features}
    
    
