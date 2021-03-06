from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

import pandas as pd
import numpy as np


class Model:
    """
    Every Model class needs to implement at least the `__init__`, `fit` and `predict` methods.
    """
    def __init__(self, log_C, kernel, shrinking):
        """
        The __init__ method gets called when initializing the model. The arguments that are named in the method are
        hyperparameters that influence the way the model is constructed and trained. These can be directly linked to
        the algorithm but also for the preprocessor which is considered to be part of the model. In this example support
        vector classifier Cubonacci can change the `log_C`, `kernel` and `shrinking` to optimize the model.
        :param log_C: Logarithm of C, the penalty classifier
        :param kernel: Kernel type
        :param shrinking: Whether to use the shrinking heuristic
        """
        self.log_C = log_C
        self.kernel = kernel
        self.shrinking = True if shrinking == "true" else False
        self.standard_scaler = None
        self.model = None
        self.pipeline = None

    def fit(self, X, y):
        """
        The method called to train the model. X has the same schema as the features from the DataLoader while y has the
        same schema as the target. Here we instantiate the model with the passed hyperparameters.
        :param X: Features
        :param y: Target
        """
        self.standard_scaler = StandardScaler()
        self.model = SVC(C=np.exp(self.log_C),
                         shrinking=self.shrinking,
                         kernel=self.kernel,
                         probability=True)
        self.pipeline = Pipeline([("StandardScaler", self.standard_scaler), ("SVC", self.model)])
        self.pipeline.fit(X=X, y=y.values.ravel())

    def predict(self, X):
        """
        After the model has been trained Cubonacci calls this method to predict on features `X`. This method returns
        the corresponding predictions. `X` is always wrapped as if it is multiple samples, even if it is just one.
        The return value for a single prediction can be custom again. Cubonacci runs predictions on a sample of 1000
        training rows to automatically infer the target.
        :param X: Features (always multiple samples)
        :return: Prediction object
        """
        discrete_prediction = self.pipeline.predict(X)
        predictions = self.pipeline.predict_proba(X)
        predictions = pd.DataFrame(predictions, columns=['PSetosa', 'PVersicolor', 'PVirginica'])
        predictions['Prediction'] = discrete_prediction
        return predictions
