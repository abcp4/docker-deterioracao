import xgboost as xgb
from sklearn.metrics import accuracy_score

from hyperopt import STATUS_OK, fmin, hp, tpe


def otimizar_xgb(X_train, y_train, X_val, y_val):
    "Hyperparameter optimization"
    train = xgb.DMatrix(X_train, label=y_train)
    val = xgb.DMatrix(X_val, label=y_val)
    X_val_D = xgb.DMatrix(X_val)

    def objective(params):
        xgb_model = xgb.train(
            params,
            dtrain=train,
            num_boost_round=1000,
            evals=[(val, "eval")],
            verbose_eval=False,
            early_stopping_rounds=80,
        )
        y_vd_pred = xgb_model.predict(
            X_val_D, ntree_limit=xgb_model.best_ntree_limit
        )
        y_val_class = [0 if i <= 0.5 else 1 for i in y_vd_pred]

        acc = accuracy_score(y_val, y_val_class)
        loss = 1 - acc

        return {"loss": loss, "params": params, "status": STATUS_OK}

    max_depths = [3, 4, 5]
    min_child_weights = [1, 5, 10]
    learning_rates = [0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.15, 0.2]
    subsamples = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    colsample_bytrees = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    reg_alphas = [0.0, 0.005, 0.01, 0.05, 0.1]
    reg_lambdas = [0.8, 1, 1.5, 2, 4]
    gammas = [0.5, 1, 1.5, 2, 5]

    space = {
        "max_depth": hp.choice("max_depth", max_depths),
        "min_child_weight": hp.choice("min_child_weight", min_child_weights),
        "learning_rate": hp.choice("learning_rate", learning_rates),
        "subsample": hp.choice("subsample", subsamples),
        "colsample_bytree": hp.choice("colsample_bytree", colsample_bytrees),
        "reg_alpha": hp.choice("reg_alpha", reg_alphas),
        "reg_lambda": hp.choice("reg_lambda", reg_lambdas),
        "gamma": hp.choice("gamma", gammas),
    }

    best = fmin(fn=objective, space=space, algo=tpe.suggest, max_evals=100)

    best_param = {
        "max_depth": max_depths[(best["max_depth"])],
        "min_child_weight": min_child_weights[(best["min_child_weight"])],
        "learning_rate": learning_rates[(best["learning_rate"])],
        "subsample": subsamples[(best["subsample"])],
        "colsample_bytree": colsample_bytrees[(best["colsample_bytree"])],
        "reg_alpha": reg_alphas[(best["reg_alpha"])],
        "reg_lambda": reg_lambdas[(best["reg_lambda"])],
        "gamma": gammas[(best["gamma"])],
    }

    return best_param
