import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import joblib
import os


class DataPreprocessor:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='median')
        self.feature_columns = None
        self.is_fitted = False

    def fit(self, X):
        self.feature_columns = X.columns.tolist()
        categorical_cols = ['food_type', 'storage_type']
        numerical_cols = ['temperature', 'humidity', 'days_stored']

        for col in categorical_cols:
            if col in X.columns:
                le = LabelEncoder()
                X[col] = X[col].astype(str)
                le.fit(X[col])
                self.label_encoders[col] = le
                X[col] = le.transform(X[col])

        X[numerical_cols] = self.imputer.fit_transform(X[numerical_cols])
        self.scaler.fit(X[numerical_cols])
        self.is_fitted = True
        return self

    def transform(self, X):
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transform")

        X = X.copy()
        categorical_cols = ['food_type', 'storage_type']
        numerical_cols = ['temperature', 'humidity', 'days_stored']

        for col in categorical_cols:
            if col in X.columns and col in self.label_encoders:
                X[col] = X[col].astype(str)
                le = self.label_encoders[col]
                unseen_mask = ~X[col].isin(le.classes_)
                if unseen_mask.any():
                    X.loc[unseen_mask, col] = le.classes_[0]
                X[col] = le.transform(X[col])

        X[numerical_cols] = self.imputer.transform(X[numerical_cols])
        X[numerical_cols] = self.scaler.transform(X[numerical_cols])

        return X

    def fit_transform(self, X):
        return self.fit(X).transform(X)

    def save(self, filepath):
        joblib.dump({
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'imputer': self.imputer,
            'feature_columns': self.feature_columns,
            'is_fitted': self.is_fitted
        }, filepath)

    def load(self, filepath):
        data = joblib.load(filepath)
        self.label_encoders = data['label_encoders']
        self.scaler = data['scaler']
        self.imputer = data['imputer']
        self.feature_columns = data['feature_columns']
        self.is_fitted = data['is_fitted']
        return self


def load_data(filepath):
    df = pd.read_csv(filepath)
    X = df.drop('remaining_shelf_life', axis=1)
    y = df['remaining_shelf_life']
    return X, y
