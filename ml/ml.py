import os
import json
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import train_test_split, GridSearchCV

path = os.path.join(os.path.dirname( __file__ ), 'data_from_base.json')
data = json.loads(path)

def make_prediction(data):
    ds = pd.json_normalize(data['data'])
    ml_model = 1
    return ds

print(make_prediction(data))