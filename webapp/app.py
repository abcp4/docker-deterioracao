import joblib
import matplotlib.pyplot as plt
import pandas as pd
import requests
import shap
import streamlit as st
import streamlit.components.v1 as components
import os


def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)


# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

# st.title('App para predição de deterioração clínica do paciente')

st.header("App para predição de deterioração clínica do paciente")
st.markdown(
    """Essa demonstração faz uso do streamlit, xgboost e shap para
explicabilidade do modelo.
"""
)

modelo_name = st.selectbox(
    "Selecione o modelo", ["Modelo com setor", "Modelo sem setor"]
)  # select your dataset

# select your dataset params
st.sidebar.title("Coloque as informações do paciente")
setor = st.sidebar.selectbox(
    "Setor",
    [
        "UTIG",
        "1AP2",
        "4AP2",
        "UTIC",
        "UTIP",
        "3AP1",
        "3AP2",
        "4AP1",
        "1AP1",
        "2AP2",
        "UIP",
        "3AP3",
        "1AP2 - 126",
        "2AP1",
        "3AP3 - EPI",
        "SEMI-CO",
    ],
)  # data points

idade = st.sidebar.number_input("Idade", value=87, step=1)
temp = st.sidebar.number_input("Temperatura", value=36.0)
resp = st.sidebar.number_input("Frequência respiratória", value=18.0)
sisto = st.sidebar.number_input("Pressão Sistólica", value=128.0)
diasto = st.sidebar.number_input("Pressão Diastólica", value=75.0)
media = st.sidebar.number_input("Pressão Média", value=93.0)
o2 = st.sidebar.number_input("Saturação O2", value=91.0)
submit = st.sidebar.button("Fazer Predição")

# Carregar modelos do matplotlib
model = joblib.load("models/xgb_model.joblib")
nosection_model = joblib.load("models/nosection_xgb_model.joblib")

# Explainer
explainer = shap.TreeExplainer(model)
nosection_explainer = shap.TreeExplainer(nosection_model)
labels = ["Melhorado", "Obito"]
column_names = [
    "Idade",
    "Setor",
    "Temperatura",
    "Frequência respiratória",
    "Pressão Sistólica",
    "Pressão Diastólica",
    "Pressão Média",
    "Saturação O2",
    "Bin_Temperatura",
    "Bin_Respiração",
    "Bin_Sistólica",
    "Bin_Média",
    "Bin_o2",
]
column_names_nosector = [column_names[0]] + column_names[2:]

API_URL = os.getenv("API_URL")


if submit:
    query_params = {
        "age": idade,
        "temperature": temp,
        "respiratory_frequency": resp,
        "systolic_blood_pressure": sisto,
        "diastolic_blood_pressure": diasto,
        "mean_arterial_pressure": media,
        "oxygen_saturation": o2,
    }
    if modelo_name == "Modelo com setor":
        query_params["sector"] = setor
    r = requests.get(
        f"{API_URL}/predict",
        params=query_params,
    )

    data = r.json()
    y_pred = data["predict"]
    features = data["features"]
    if modelo_name != "Modelo sem setor":
        shap_values = explainer.shap_values(features)
        features = {
            column_names[k]: [features[k]] for k in range(len(features))
        }
        features = pd.DataFrame.from_dict(features)
    else:
        shap_values = nosection_explainer.shap_values(features)
        features = {
            column_names_nosector[k]: [features[k]]
            for k in range(len(features))
        }
        features = pd.DataFrame.from_dict(features)

    # st.write("Predição: ", labels[int(y_pred[0])])

    fig, ax = plt.subplots(nrows=1, ncols=1)

    p = shap.force_plot(explainer.expected_value, shap_values[0, :], features)
    # shap.summary_plot(shap_values, sample)
    # st.pyplot(fig)
    st.subheader(f"Predição: {labels[int(y_pred)]}")
    st_shap(p)
