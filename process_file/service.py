# Packages related to general operating system & warnings
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import requests
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from pandas import Series, DataFrame
from sklearn import metrics
from sklearn import preprocessing
from sklearn.ensemble import BaggingClassifier, BaggingRegressor, RandomForestClassifier, RandomForestRegressor, \
    GradientBoostingClassifier, GradientBoostingRegressor, AdaBoostClassifier, AdaBoostRegressor
from sklearn.impute import MissingIndicator, SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegression, LinearRegression, ElasticNet, Lasso, Ridge
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, KBinsDiscretizer, FunctionTransformer, \
    MinMaxScaler, MaxAbsScaler, LabelEncoder, OneHotEncoder, LabelBinarizer, OrdinalEncoder
from sklearn.svm import LinearSVC, LinearSVR, SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_graphviz
from termcolor import colored as cl  # text customization #Packages related to data
from xgboost import XGBClassifier

from process_file.models import MiscData
from process_file.serializers import MiscDataSerializer

"""
sc = StandardScaler()
amount = data['amt'].values
data['amt'] = sc.fit_transform(amount.reshape(-1, 1))

merch_lat = data['merch_lat'].values
data['merch_lat'] = sc.fit_transform(merch_lat.reshape(-1, 1))

merch_long = data['merch_long'].values
data['merch_long'] = sc.fit_transform(merch_long.reshape(-1, 1))

data.drop_duplicates(inplace=True)

X = data[['amt', 'merch_lat', 'merch_long']]
Y = data['is_fraud'].values

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=1)
xgb = XGBClassifier(max_depth = 4)
xgb.fit(X_train, y_train)
xgb_yhat = xgb.predict(X_test)
ress = len(xgb_yhat)
data['is_fraud'] = list(xgb_yhat) + [0] * (total_transactions - ress)
# print(len(xgb_yhat), "ppppppp", total_transactions)
# print(xgb_yhat)

# print(data)
data.set_index("trans_num", drop=True, inplace=True)
dictionary = data.to_dict(orient="index")
s_data = self.insert_to_db(dictionary)
return s_data
"""


class ProcessFileService:

    def process_file(self, file_url, n_rows):
        r = requests.get(file_url, allow_redirects=True)
        file = 'op.xlsx'
        with open(file, 'wb') as f:
            f.write(r.content)
        data = pd.read_excel(file)
        total_transactions = len(data)
        print(total_transactions, "total transactions")

        # filling default values
        data['lat'].fillna(0, inplace=True)
        data['long'].fillna(0, inplace=True)
        data['city_pop'].fillna(0, inplace=True)
        data['trans_num'].fillna(0, inplace=True)
        data['merch_lat'].fillna(0, inplace=True)
        data['merch_long'].fillna(0, inplace=True)
        data['is_fraud'].fillna(0, inplace=True)

        # feature attributes
        # X = data[[
        #     'cc_num',
        #     'amt',
        #     'lat',
        #     'long',
        #     'merch_lat',
        #     'merch_long'
        # ]]
        X = data.drop(['is_fraud'], axis=1)
        X = data.drop(['trans_date_trans_time'], axis=1)
        X = data.drop(['unix_time'], axis=1)


        Y = data['is_fraud']  # target variable
        # splitting the data
        X_train, X_test, y_train, y_test = train_test_split(X, Y, random_state=0)
        X_train_2 = X_train[[
            'cc_num',
            'amt',
            'lat',
            'long',
            'merch_lat',
            'merch_long',
        ]]

        X_test_2 = X_test[[
            'cc_num',
            'amt',
            'lat',
            'long',
            'merch_lat',
            'merch_long',
        ]]

        # model initialization
        knn = KNeighborsClassifier(n_neighbors=10)
        # training
        knn.fit(X_train_2, y_train)
        # predicting values
        y_pred = knn.predict(X_test_2)
        print(len(y_pred), "yeh hai length")

        X_test['is_fraud'] = list(y_pred)
        X_test['dob'] = X_test['dob'].dt.strftime('%Y-%m-%d %H:%M:%S')
        X_test.set_index("trans_num", drop=True, inplace=True)
        dictionary = X_test.to_dict(orient="index")
        s_data = self.insert_to_db(dictionary)
        return s_data

    def insert_to_db(self, props):
        parent_obj = MiscData.objects.create()
        parent_id = parent_obj.id
        for dic in props:
            print(props[dic])
            MiscData.objects.create(parent_id=parent_id, props=props[dic])
        s_data = MiscDataSerializer(parent_obj).data
        return s_data

    def pass_through_model(data):
        pass
