import numpy as np
import pandas as pd
import xgboost as xgb
from imblearn.under_sampling import AllKNN

# Salvar
from joblib import dump
from sklearn import preprocessing
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from binning import binning
from optim_xgb import otimizar_xgb

data = pd.read_csv("laura1.csv", sep="\t")

processed_data = data.interpolate("polynomial", order=7)

# Retirar o ultimo NAN
processed_data = processed_data.dropna()

"""
Engenharia de Features
"""


le = preprocessing.LabelEncoder()
le.fit(processed_data["setor"].values)
processed_data["setor"] = le.transform(processed_data["setor"].values)


features = binning(processed_data)
features = np.reshape(features, (5, 5000))
processed_data["feature1"] = features[0][:]
processed_data["feature2"] = features[1][:]
processed_data["feature3"] = features[2][:]
processed_data["feature4"] = features[3][:]
processed_data["feature5"] = features[4][:]


"""
Treinamento do modelo
"""


def str2num(d):
    n = np.zeros(len(d))
    for i in range(len(d)):
        if d[i] == "Melhorado":
            n[i] = 0
        else:
            n[i] = 1
    return n


y = processed_data["alta.motivo"].values
X = processed_data.drop(["alta.motivo"], axis=1)

y = str2num(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=41
)

X_valid, X_test, y_valid, y_test = train_test_split(
    X_test, y_test, test_size=0.5, random_state=41
)

X_train_df = X_train.copy()
X_valid_df = X_valid.copy()
X_test_df = X_test.copy()


ss = StandardScaler()
ss.fit(X_train)
X_train = ss.transform(X_train)
X_valid = ss.transform(X_valid)

imb = AllKNN()
imb.fit(X_train, y_train)
X_train, y_train = imb.fit_resample(X_train, y_train)


best_param = otimizar_xgb(X_train, y_train, X_valid, y_valid)
print(best_param)

xgb_model = xgb.XGBClassifier(
    max_depth=best_param["max_depth"],
    min_child_weight=best_param["min_child_weight"],
    eta=best_param["learning_rate"],
    n_estimators=1000,
    subsample=best_param["subsample"],
    colsample_bytree=best_param["colsample_bytree"],
    reg_alpha=best_param["reg_alpha"],
    reg_lambda=best_param["reg_lambda"],
    gamma=best_param["gamma"],
    objective="binary:logistic",
)

xgb_model.fit(
    X_train,
    y_train,
    eval_set=[(X_valid, y_valid)],
    eval_metric="error",
    early_stopping_rounds=80,
    verbose=False,
)

y_pred = xgb_model.predict(X_valid)
print(classification_report(y_valid, y_pred))
auc = roc_auc_score(y_valid, y_pred)
print("AUC: " + str(auc))


dump(ss, "scaler.joblib")
dump(xgb_model, "xgb_model.joblib")
dump(le, "le.joblib")
