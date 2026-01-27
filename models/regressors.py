from abc import ABC, abstractmethod
from typing import Iterator

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import BaseCrossValidator, GridSearchCV
from xgboost import XGBRegressor


class TimeseriesSplitter(BaseCrossValidator):
    def __init__(self, n_splits: int = 5):
        self.validation_folds = [[2013, 2014], [2015, 2016], [2017, 2018], [2019, 2020], [2021, 2022]]
        self.n_splits = n_splits

    def split(self, X: pd.DataFrame, y: pd.Series, groups: None = None) -> Iterator[tuple[np.ndarray, np.ndarray]]:
        for validation_years in self.validation_folds:
            train_indices = X[X["year"] < validation_years[0]].index
            val_indices = X[X["year"].isin(validation_years)].index
            yield train_indices, val_indices

    def get_n_splits(self, X=None, y=None, groups=None):
        """Returns the number of splitting iterations"""
        return self.n_splits


class Regressor(ABC):
    def __init__(self):
        self.regressor = None
        self.test_years = [2023, 2024]
        self.cv_splitter = TimeseriesSplitter()

    @abstractmethod
    def get_grid_params(self) -> dict:
        return {}

    def load_data(self) -> tuple[pd.DataFrame, pd.Series]:
        df = pd.read_csv("data/timeseries-sample.csv")
        df = df.drop(columns=[df.columns[0]])
        print(f"Successfully loaded data with shape {df.shape = }")
        df["in_beach_zone"] = df["in_beach_zone"].astype(int)

        X, y = df.drop(columns=["index"]), df["index"]
        return X, y

    def train_test_split(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        X, y = self.load_data()
        X_train, X_test = X[X["year"].isin(self.test_years) == False], X[X["year"].isin(self.test_years)]
        y_train, y_test = y[X["year"].isin(self.test_years) == False], y[X["year"].isin(self.test_years)]
        print(f"Successfully split data into train and test sets with shapes {X_train.shape = }, {X_test.shape = }")
        return X_train, X_test, y_train, y_test

    @staticmethod
    def evaluate_model(y_true: pd.Series, y_pred: np.ndarray) -> dict:
        return {
            'MSE': mean_squared_error(y_true, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
            'MAE': mean_absolute_error(y_true, y_pred),
            'R2': r2_score(y_true, y_pred)
        }

    def grid_search(self, X: pd.DataFrame, y: np.ndarray) -> GridSearchCV:
        gs = GridSearchCV(
            self.regressor,
            self.get_grid_params(),
            scoring="neg_mean_squared_error",
            cv=self.cv_splitter,
            n_jobs=-1,
            verbose=3,
        )

        gs.fit(X, y)
        return gs


class CatBoost(Regressor):
    def __init__(self):
        super().__init__()
        self.regressor = CatBoostRegressor(verbose=False, random_state=42, learning_rate=0.1, depth=3, n_estimators=200, l2_leaf_reg=3, max_bin=251)

    def get_grid_params(self) -> dict:
        return {
            # 'model_size_reg': [0.1, 0.15, 0.2, 0.25],
        }


class LightGBM(Regressor):
    def __init__(self):
        super().__init__()
        self.regressor = LGBMRegressor(random_state=42, verbose=-1, max_depth=3, n_estimators=200, learning_rate=0.125, max_bin=325)

    def get_grid_params(self) -> dict:
        return {
            # 'num_leaves': [5, 7, 9],
            # 'boosting_type': ['gbdt', 'goss'],
        }


class XGBoost(Regressor):
    def __init__(self):
        super().__init__()
        self.regressor = XGBRegressor(tree_method="hist", random_state=42, max_depth=3, learning_rate=0.08, n_estimators=250, min_child_weight=5)

    def get_grid_params(self) -> dict:
        return {
            # 'grow_policy': ['depthwise', 'lossguide'],
            # 'max_bin': [250, 290, 300, 310, 325, 350],
            # 'max_leaves': [5, 7, 9],
        }
