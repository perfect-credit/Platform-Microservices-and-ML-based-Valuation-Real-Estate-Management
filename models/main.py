import joblib

import pandas as pd
import matplotlib.pyplot as plt

from regressors import CatBoost, LightGBM, Regressor, XGBoost


def train():
    cat = CatBoost()

    X_train, X_test, y_train, y_test = cat.train_test_split()

    cat_gs = cat.grid_search(X_train, y_train)
    print(f"{cat_gs.best_params_ = }")
    y_pred = cat_gs.predict(X_test)
    cat_gs_metrics = Regressor.evaluate_model(y_test, y_pred)

    lgbm = LightGBM()
    lgbm_gs = lgbm.grid_search(X_train, y_train)
    print(f"{lgbm_gs.best_params_ = }")
    y_pred = lgbm_gs.predict(X_test)
    lgbm_gs_metrics = Regressor.evaluate_model(y_test, y_pred)

    xgb = XGBoost()
    xgb_gs = xgb.grid_search(X_train, y_train)
    print(f"{xgb_gs.best_params_ = }")
    y_pred = xgb_gs.predict(X_test)
    xgb_gs_metrics = Regressor.evaluate_model(y_test, y_pred)

    # create a dataframe with the metrics
    df = pd.DataFrame(
        [
            {"model": "CatBoost", **cat_gs_metrics},
            {"model": "LightGBM", **lgbm_gs_metrics},
            {"model": "XGBoost", **xgb_gs_metrics},
        ],
    )

    # plot the metrics
    df.plot(x="model", y=["MSE"], kind="bar", rot=0)
    df.plot(x="model", y=["RMSE"], kind="bar", rot=0)
    df.plot(x="model", y=["MAE"], kind="bar", rot=0)
    df.plot(x="model", y=["R2"], kind="bar", rot=0)
    plt.show()

    # save the best model: CatBoost in this case
    joblib.dump(cat_gs.best_estimator_, "saved/valuation.pkl")


def test():
    regressor = joblib.load("saved/valuation.pkl")
    cat = CatBoost()

    _, X_test, _, y_test = cat.train_test_split()

    y_pred = regressor.predict(X_test)
    cat_metrics = Regressor.evaluate_model(y_test, y_pred)

    print(f"{cat_metrics = }")


if __name__ == "__main__":
    train()
    test()
