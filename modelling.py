import pickle

import numpy as np
import joblib
import os
import warnings

warnings.simplefilter('ignore')


def process_features(features):
    """
    :param features: is the list or tuple of features/characteristics
    this is the order of features to be passed in the model
    1. nighttime phone usage / day (minutes)
    2. step count
    3. in bed awake duration (minutes)
    4. actual sleep duration (minutes)
    5. total phone usage / day (minutes)
    6. calories burnt (kcal)
    7. phone unlock count / day
    :return:
    ndarray of features to be used for making predictions
    """
    features = np.asarray(features)
    features = features.reshape(1, -1)
    return features


def load_model(filename):
    """
    :param filename: the full path to the model file saved as joblib
    :return:
    returns the model
    """
    # Load the model
    with open(filename, 'rb') as f:
        model = joblib.load(f)
        f.close()
    return model


def make_prediction(predictors):
    file_path = os.path.join(os.getcwd(), "files", "telemedecine_model_3.sav")
    model = load_model(file_path)
    predictions = model.predict(predictors)
    if predictions[0] == 0:
        return "Healthy"
    elif predictions[0] == 1:
        return "Medium Healthy"
    else:
        return "Unhealthy"


if __name__ == "__main__":


    input_data = (686, 3016, 58, 455, 730, 2151, 97)
    input_data = process_features(input_data)
    pred = make_prediction(input_data, model)
    print(f"Prediction: {pred}")
