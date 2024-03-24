from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pandas as pd

class ScalerDf(BaseEstimator, TransformerMixin):

    def __init__(self, method):
        self.method = method

    def transform(self, X):
        X = pd.DataFrame(
            self.scaler.transform(X),
            columns=X.columns,
            index=X.index
        )
        return X

    def fit(self, X, y=None):
        if self.method == 'minmax':
            self.scaler = MinMaxScaler()
        elif self.method == 'standard':
            self.scaler = StandardScaler()
        elif self.method == 'none':
            return self
        else:
            raise ValueError("Invalid scaling method. Supported methods are 'minmax', 'standard', and 'none'.")

        self.scaler.fit(X)
        return self