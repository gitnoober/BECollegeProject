#Packages related to general operating system & warnings
import pickle
import json
import requests
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from termcolor import colored as cl # text customization #Packages related to data
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages 
from sklearn.model_selection import train_test_split, GridSearchCV 
from sklearn import metrics 
from sklearn.impute import MissingIndicator, SimpleImputer 
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, KBinsDiscretizer, FunctionTransformer, MinMaxScaler, MaxAbsScaler, LabelEncoder, OneHotEncoder, LabelBinarizer, OrdinalEncoder
from sklearn.linear_model import LogisticRegression, LinearRegression, ElasticNet, Lasso, Ridge 
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor 
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_graphviz 
from sklearn.ensemble import BaggingClassifier, BaggingRegressor, RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor, AdaBoostClassifier, AdaBoostRegressor
from sklearn.svm import LinearSVC, LinearSVR, SVC, SVR 
from xgboost import XGBClassifier 
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix
from process_file.models import MiscData
from process_file.serializers import MiscDataSerializer
class ProcessFileService:
    
    def process_file(self, file_url, n_rows):
        r = requests.get(file_url, allow_redirects=True)
        file = 'op.csv'
        with open(file, 'wb') as f:
            f.write(r.content)
        data = pd.read_csv(file, nrows=n_rows)
        total_transactions = len(data)
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
        
    def insert_to_db(self, props):
        parent_obj = MiscData.objects.create()
        parent_id = parent_obj.id
        for dic in props:
            MiscData.objects.create(parent_id=parent_id, props=props[dic])
        s_data = MiscDataSerializer(parent_obj).data
        # print(parent_id)
        return s_data
        
    
    def pass_through_model(data):
        pass