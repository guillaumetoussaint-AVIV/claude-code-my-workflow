import numpy as np
import pandas as pd
import statsmodels.api as sm
import sklearn
from scipy.stats import loguniform
from pandas import read_csv
import statistics
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from sklearn.linear_model import ElasticNet
from scipy.stats import randint
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import KFold
from matplotlib import pyplot
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from numpy import arange
from numpy import mean
from numpy import std
from sklearn.metrics import accuracy_score
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import StratifiedShuffleSplit,RepeatedStratifiedKFold
from sklearn.linear_model import LinearRegression
from mlxtend.feature_selection import SequentialFeatureSelector
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
#%%
Fusion_d01_d21 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/Fusion_d01_d21.csv",sep = ",")
Fusion_d22_d40 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/Fusion_d22_d40.csv",sep = ",")
Fusion_d41_d60 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/Fusion_d41_d60.csv",sep = ",")
Fusion_d61_d80 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/Fusion_d61_d80.csv",sep = ",")
Fusion_d81_d974 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/Fusion_d81_d974.csv",sep = ",")
Fusion_d971_d974 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/Fusion_d971_d974.csv",sep = ",")

#%%Centre val de Loire
Fusion = pd.concat([Fusion_d01_d21, Fusion_d22_d40, Fusion_d41_d60, Fusion_d61_d80, Fusion_d81_d974], axis = 0)
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:2]
Fusion['Dep'].value_counts()

Fusion = Fusion[(Fusion['Dep'] == "18")|(Fusion['Dep'] == "28")|(Fusion['Dep'] == "36")|
                (Fusion['Dep'] == "37")|(Fusion['Dep'] == "41")|(Fusion['Dep'] == "45")]
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['datemut'] >= '2012-01-01') & (Fusion['datemut'] < '2013-01-01')]
list(Fusion.columns)
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Fusion = pd.merge(Fusion, Aires_urbaines, how="left", on=['ffcodinsee'])
Fusion = Fusion.dropna()
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)


Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('243700754', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})
#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=2)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=5,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 50, 
                                      max_depth= 5, 
                                      max_bins= 50, 
                                      loss= 'absolute_error', 
                                      learning_rate= 0.3, 
                                      l2_regularization= 0.45)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight= 4, 
                     max_depth= 9,
                     reg_lambda= 0.7, 
                     gamma= 0.4, 
                     eta= 0.15, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))

#%%Prédiction
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R24.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
#Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)&
                            (Fusion_pred['npiece_ff']> 0)]
#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred,  
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 8.12€ du m²
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min: 5.48€ du m²
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 7,17€ du m²
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_24.csv', sep=',', encoding='utf-8')

#%%Île de France sans Paris
Fusion = pd.concat([Fusion_d01_d21, Fusion_d22_d40, Fusion_d41_d60, Fusion_d61_d80, Fusion_d81_d974], axis = 0)
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:2]
Fusion['Dep'].value_counts()
Fusion = Fusion[(Fusion['Dep'] == "77")|(Fusion['Dep'] == "78")|
                (Fusion['Dep'] == "91")|(Fusion['Dep'] == "92")|(Fusion['Dep'] == "93")|
                (Fusion['Dep'] == "94")|(Fusion['Dep'] == "95")]
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['datemut'] >= '2019-01-01') & (Fusion['datemut'] < '2020-01-01')]
list(Fusion.columns)
Fusion['ffcodinsee'].value_counts()
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)


Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})
#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=42)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 40, 
                                      max_depth= 4, 
                                      max_bins= 50, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.5, 
                                      l2_regularization= 0.5)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight= 5, 
                     max_depth= 9,
                     reg_lambda= 0.6, 
                     gamma = 0, 
                     eta = 0.1, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))

#%%
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R11.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)&
                            (Fusion_pred['npiece_ff']> 0)]
#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred,  
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 9.37€ du m²
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min: 6.35€ du m²
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 8.11 du m²
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_11.csv', sep=',', encoding='utf-8', index=False)

#%%Paris
Fusion = pd.concat([Fusion_d01_d21, Fusion_d22_d40, Fusion_d41_d60, Fusion_d61_d80, Fusion_d81_d974], axis = 0)
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:2]
Fusion['Dep'].value_counts()
Fusion = Fusion[(Fusion['Dep'] == "75")]
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['datemut'] >= '2019-01-01') & (Fusion['datemut'] < '2020-01-01')]
list(Fusion.columns)
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)

Comm = pd.get_dummies(Fusion['ffcodinsee'])
Fusion['ffcodinsee'].value_counts()
Comm = Comm.drop('75115', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})
#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=42)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 40, 
                                      max_depth= 4, 
                                      max_bins= 50, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.5, 
                                      l2_regularization= 0.5)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight= 4,
                     max_depth= 6,
                     reg_lambda= 0.5,
                     gamma = 0.2,
                     eta = 0.25,
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))

#%%
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R11_75.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_pred['Dep'] = Fusion_pred['idcom'].astype(str).str[:2]
Fusion_pred['Dep'].value_counts()
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)&
                            (Fusion_pred['npiece_ff']> 0)]
#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred,  
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 9.84€ du m²
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min: 8.43€ du m²
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 9.21€ du m²
Fusion_1_Pred = Fusion_1_Pred.drop(columns=['Dep'])
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_Paris.csv', sep=',', encoding='utf-8', index=False)

#%%Bourgogne-Franche comté
Fusion = pd.concat([Fusion_d01_d21, Fusion_d22_d40, Fusion_d41_d60, Fusion_d61_d80, Fusion_d81_d974], axis = 0)
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:2]
Fusion['Dep'].value_counts()
Fusion = Fusion[(Fusion['Dep'] == "21")|(Fusion['Dep'] == "25")|(Fusion['Dep'] == "39")|
                (Fusion['Dep'] == "58")|(Fusion['Dep'] == "70")|(Fusion['Dep'] == "71")|
                (Fusion['Dep'] == "89")|(Fusion['Dep'] == "90")]
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['datemut'] >= '2019-01-01') & (Fusion['datemut'] < '2020-01-01')]
list(Fusion.columns)
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Fusion = pd.merge(Fusion, Aires_urbaines, how="left", on=['ffcodinsee'])
Fusion = Fusion.dropna()
#%%
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)


Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('242100410', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})
#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=42)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 20, 
                                      max_depth= 4, 
                                      max_bins= 30, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.4, 
                                      l2_regularization= 0)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight= 3, 
                     max_depth= 8,
                     reg_lambda= 0.55, 
                     gamma= 0.4, 
                     eta= 0.1, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R27.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)&
                            (Fusion_pred['npiece_ff']> 0)]
#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred, 
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 8.21 du m²
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min: 5.27€ du m²
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 7.04€ du m²
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_27.csv', sep=',', encoding='utf-8', index=False)

#%%Normandie
Fusion = pd.concat([Fusion_d01_d21, Fusion_d22_d40, Fusion_d41_d60, Fusion_d61_d80, Fusion_d81_d974], axis = 0)
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:2]
Fusion['Dep'].value_counts()
Fusion = Fusion[(Fusion['Dep'] == "14")|(Fusion['Dep'] == "27")|(Fusion['Dep'] == "50")|
                (Fusion['Dep'] == "61")|(Fusion['Dep'] == "76")]
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['datemut'] >= '2019-01-01') & (Fusion['datemut'] < '2020-01-01')]
list(Fusion.columns)
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Fusion = pd.merge(Fusion, Aires_urbaines, how="left", on=['ffcodinsee'])
Fusion = Fusion.dropna()
#%%
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)


Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('200023414', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})
#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=42)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 20, 
                                      max_depth= 4, 
                                      max_bins= 50, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.4, 
                                      l2_regularization= 0.15)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight= 2, 
                     max_depth= 8,
                     reg_lambda= 0.65, 
                     gamma=0.4,  
                     eta= 0.15, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))

#%%
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R28.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
#Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)&
                            (Fusion_pred['npiece_ff']> 0)]
#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred, 
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 8.57€ du m²
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min: 5.36€ du m²
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 7.29€ du m²
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_28.csv', sep=',', encoding='utf-8', index=False)

#%%Hauts-de-France
Fusion = pd.concat([Fusion_d01_d21, Fusion_d22_d40, Fusion_d41_d60, Fusion_d61_d80, Fusion_d81_d974], axis = 0)
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:2]
Fusion['Dep'].value_counts()
Fusion = Fusion[(Fusion['Dep'] == "02")|(Fusion['Dep'] == "59")|(Fusion['Dep'] == "60")|
                (Fusion['Dep'] == "62")|(Fusion['Dep'] == "80")]
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['datemut'] >= '2019-01-01') & (Fusion['datemut'] < '2020-01-01')]
list(Fusion.columns)
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Fusion = pd.merge(Fusion, Aires_urbaines, how="left", on=['ffcodinsee'])
Fusion = Fusion.dropna()
#%%
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)


Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('200093201', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})
#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=42)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 30, 
                                      max_depth= 4, 
                                      max_bins= 50, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.4, 
                                      l2_regularization= 0.1)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight = 4, 
                     max_depth = 10,
                     reg_lambda = 0.25, 
                     gamma = 0.8,  
                     eta = 0.2, 
                     booster = 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))

#%%
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R32.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
#Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)&
                            (Fusion_pred['npiece_ff']> 0)]
#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred, 
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 8.89€ du m²
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min: 5.52€ du m²
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 7.28€ du m²
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_32.csv', sep=',', encoding='utf-8', index=False)

#%%Grand est
Fusion = pd.concat([Fusion_d01_d21, Fusion_d22_d40, Fusion_d41_d60, Fusion_d61_d80, Fusion_d81_d974], axis = 0)
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:2]
Fusion['Dep'].value_counts()
Fusion = Fusion[(Fusion['Dep'] == "08")|(Fusion['Dep'] == "10")|(Fusion['Dep'] == "51")|
                (Fusion['Dep'] == "52")|(Fusion['Dep'] == "54")|(Fusion['Dep'] == "55")|
                (Fusion['Dep'] == "88")]
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['datemut'] >= '2019-01-01') & (Fusion['datemut'] < '2020-01-01')]
list(Fusion.columns)
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Fusion = pd.merge(Fusion, Aires_urbaines, how="left", on=['ffcodinsee'])
Fusion = Fusion.dropna()
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)


Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('200067213', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})
#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=42)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 40, 
                                      max_depth= 4, 
                                      max_bins= 40, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.4, 
                                      l2_regularization= 0.65)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))#0.56
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight = 5, 
                     max_depth = 7,
                     reg_lambda = 0.5, 
                     gamma = 0.6,  
                     eta = 0.1, 
                     booster = 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))

#%%
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R44.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
#Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)]
Fusion_1_Pred['Dep'] = Fusion_1_Pred['idcom'].astype(str).str[:2]
Fusion_1_Pred = Fusion_1_Pred[(Fusion_1_Pred['Dep'] == "08")|(Fusion_1_Pred['Dep'] == "10")|(Fusion_1_Pred['Dep'] == "51")|
                (Fusion_1_Pred['Dep'] == "52")|(Fusion_1_Pred['Dep'] == "54")|(Fusion_1_Pred['Dep'] == "55")|
                (Fusion_1_Pred['Dep'] == "88")]
Fusion_1_Pred = Fusion_1_Pred.drop('Dep', axis=1)

#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred, 
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 8.03€ du m²
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min: 5.36€ du m²
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 7.03€ du m²
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_44.csv', sep=',', encoding='utf-8', index=False)

#%% Alsace Moselle
Alsace_Lorraine = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Prix communes Alsace Moselle.xlsx')

Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/R44.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
#Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)]
Fusion_1_Pred['Dep'] = Fusion_1_Pred['idcom'].astype(str).str[:2]
Fusion_1_Pred = Fusion_1_Pred[(Fusion_1_Pred['Dep'] == "57")|(Fusion_1_Pred['Dep'] == "67")|(Fusion_1_Pred['Dep'] == "68")]
Fusion_1_Pred = Fusion_1_Pred.drop('Dep', axis=1)



#%%Pays de la Loire
Fusion = pd.concat([Fusion_d01_d21, Fusion_d22_d40, Fusion_d41_d60, Fusion_d61_d80, Fusion_d81_d974], axis = 0)
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:2]
Fusion['Dep'].value_counts()
Fusion = Fusion[(Fusion['Dep'] == "44")|(Fusion['Dep'] == "49")|(Fusion['Dep'] == "53")|
                (Fusion['Dep'] == "72")|(Fusion['Dep'] == "85")]
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['datemut'] >= '2019-01-01') & (Fusion['datemut'] < '2020-01-01')]
list(Fusion.columns)
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Fusion = pd.merge(Fusion, Aires_urbaines, how="left", on=['ffcodinsee'])
Fusion = Fusion.dropna()
#%%
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)


Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('244400404', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})
#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=42)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 50, 
                                      max_depth= 4, 
                                      max_bins= 50, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.3, 
                                      l2_regularization= 0.75)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight = 4, 
                     max_depth = 7,
                     reg_lambda = 0.1, 
                     gamma = 0.4,  
                     eta = 0.1, 
                     booster = 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))

#%%
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R52.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
#Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)&
                            (Fusion_pred['npiece_ff']> 0)]
#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred, 
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 8.76 du m²
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min: 5.62 du m²
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 7.45€ du m²
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_52.csv', sep=',', encoding='utf-8', index=False)

#%%Bretagne
Fusion = pd.concat([Fusion_d01_d21, Fusion_d22_d40, Fusion_d41_d60, Fusion_d61_d80, Fusion_d81_d974], axis = 0)
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:2]
Fusion['Dep'].value_counts()
Fusion = Fusion[(Fusion['Dep'] == "22")|(Fusion['Dep'] == "29")|(Fusion['Dep'] == "35")|
                (Fusion['Dep'] == "56")]
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['datemut'] >= '2019-01-01') & (Fusion['datemut'] < '2020-01-01')]
list(Fusion.columns)
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Fusion = pd.merge(Fusion, Aires_urbaines, how="left", on=['ffcodinsee'])
Fusion = Fusion.dropna()
#%%
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)


Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('243500139', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=42)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 30, 
                                      max_depth= 4, 
                                      max_bins= 50, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.4, 
                                      l2_regularization= 0.1)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight = 3, 
                     max_depth = 9,
                     reg_lambda = 0.25, 
                     gamma = 0.6,  
                     eta = 0.15, 
                     booster = 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))

#%%
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R53.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
#Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)&
                            (Fusion_pred['npiece_ff'] > 0)]
#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred, 
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 8.39€ du m²
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min: 5.62 du m²
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 6.95€ du m²
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_53.csv', sep=',', encoding='utf-8', index=False)
#%%
#%%Nouvelle Aquitaine
Fusion = pd.concat([Fusion_d01_d21, Fusion_d22_d40, Fusion_d41_d60, Fusion_d61_d80, Fusion_d81_d974], axis = 0)
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:2]
Fusion['Dep'].value_counts()
Fusion = Fusion[(Fusion['Dep'] == "16")|(Fusion['Dep'] == "17")|(Fusion['Dep'] == "19")|
                (Fusion['Dep'] == "23")|(Fusion['Dep'] == "24")|(Fusion['Dep'] == "33")|
                (Fusion['Dep'] == "40")|(Fusion['Dep'] == "47")|(Fusion['Dep'] == "64")|
                (Fusion['Dep'] == "79")|(Fusion['Dep'] == "86")|(Fusion['Dep'] == "87")]
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['datemut'] >= '2019-01-01') & (Fusion['datemut'] < '2020-01-01')]
list(Fusion.columns)
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Fusion = pd.merge(Fusion, Aires_urbaines, how="left", on=['ffcodinsee'])
Fusion = Fusion.dropna()
#%%
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('243300316', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})
#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=42)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 40, 
                                      max_depth= 6, 
                                      max_bins= 50, 
                                      loss= 'absolute_error', 
                                      learning_rate= 0.3, 
                                      l2_regularization= 0.15)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight = 5, 
                     max_depth = 10,
                     reg_lambda = 0.75, 
                     gamma = 1.2,  
                     eta = 0.1, 
                     booster = 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))

#%%
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R75.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)]
#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred,  
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 9.25€
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min: 5.63€
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 7.41€
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_75.csv', sep=',', encoding='utf-8', index=False)

#%% Occitanie
Fusion = pd.concat([Fusion_d01_d21, Fusion_d22_d40, Fusion_d41_d60, Fusion_d61_d80, Fusion_d81_d974], axis = 0)
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:2]
Fusion['Dep'].value_counts()
Fusion = Fusion[(Fusion['Dep'] == "09")|(Fusion['Dep'] == "11")|(Fusion['Dep'] == "12")|
                (Fusion['Dep'] == "30")|(Fusion['Dep'] == "31")|(Fusion['Dep'] == "32")|
                (Fusion['Dep'] == "34")|(Fusion['Dep'] == "46")|(Fusion['Dep'] == "48")|
                (Fusion['Dep'] == "65")|(Fusion['Dep'] == "66")|(Fusion['Dep'] == "81")
                |(Fusion['Dep'] == "82")]
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['datemut'] >= '2019-01-01') & (Fusion['datemut'] < '2020-01-01')]
list(Fusion.columns)
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Fusion = pd.merge(Fusion, Aires_urbaines, how="left", on=['ffcodinsee'])
Fusion = Fusion.dropna()
#%%
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('243100518', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})
#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=2)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=2)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 40, 
                                      max_depth= 6, 
                                      max_bins= 50, 
                                      loss= 'absolute_error', 
                                      learning_rate= 0.3, 
                                      l2_regularization= 0.15)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight = 4, 
                     max_depth = 10,
                     reg_lambda = 0.6, 
                     gamma = 0,  
                     eta = 0.1, 
                     booster = 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))

#%%
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R76.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)]
#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred,  
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 8.61€ m²
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min:  5.37€ m²
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 7.39€ m²
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_76.csv', sep=',', encoding='utf-8', index=False)

#%% Auvergne Rhône-Alpes
Fusion = pd.concat([Fusion_d01_d21, Fusion_d22_d40, Fusion_d41_d60, Fusion_d61_d80, Fusion_d81_d974], axis = 0)
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:2]
Fusion['Dep'].value_counts()
Fusion = Fusion[(Fusion['Dep'] == "01")|(Fusion['Dep'] == "03")|(Fusion['Dep'] == "07")|
                (Fusion['Dep'] == "15")|(Fusion['Dep'] == "26")|(Fusion['Dep'] == "38")|
                (Fusion['Dep'] == "42")|(Fusion['Dep'] == "43")|(Fusion['Dep'] == "63")|
                (Fusion['Dep'] == "69")|(Fusion['Dep'] == "73")|(Fusion['Dep'] == "74")]
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['datemut'] >= '2019-01-01') & (Fusion['datemut'] < '2020-01-01')]
list(Fusion.columns)
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Fusion = pd.merge(Fusion, Aires_urbaines, how="left", on=['ffcodinsee'])
Fusion = Fusion.dropna()
#%%
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('200046977', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})
#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=2)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=4)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 20, 
                                      max_depth= 4, 
                                      max_bins= 50, 
                                      loss= 'absolute_error', 
                                      learning_rate= 0.5, 
                                      l2_regularization= 0.2)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight = 3, 
                     max_depth = 10,
                     reg_lambda = 0.3, 
                     gamma = 0.6,  
                     eta = 0.15, 
                     booster = 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))

#%%
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R84.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
#Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)&
                            (Fusion_pred['npiece_ff'] > 0)]
#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred,  
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 9.66€ du m²
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min: 5.05 du m²
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 7.64€ du m²
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_84.csv', sep=',', encoding='utf-8', index=False)

#%% PACA
Fusion = pd.concat([Fusion_d01_d21, Fusion_d22_d40, Fusion_d41_d60, Fusion_d61_d80, Fusion_d81_d974], axis = 0)
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:2]
Fusion['Dep'].value_counts()
Fusion = Fusion[(Fusion['Dep'] == "04")|(Fusion['Dep'] == "05")|(Fusion['Dep'] == "06")|
                (Fusion['Dep'] == "13")|(Fusion['Dep'] == "83")|(Fusion['Dep'] == "84")]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['datemut'] >= '2019-01-01') & (Fusion['datemut'] < '2020-01-01')]
list(Fusion.columns)
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Fusion = pd.merge(Fusion, Aires_urbaines, how="left", on=['ffcodinsee'])
Fusion = Fusion.dropna()
#%%
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('200054807', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})
#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=2)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=4)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 20, 
                                      max_depth= 4, 
                                      max_bins= 50, 
                                      loss= 'absolute_error', 
                                      learning_rate= 0.5, 
                                      l2_regularization= 0.2)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight = 5, 
                     max_depth = 9,
                     reg_lambda = 0.4, 
                     gamma = 0,  
                     eta = 0.1, 
                     booster = 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))

#%%
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R93.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)&
                            (Fusion_pred['npiece_ff'] > 0)]
#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred,  
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 9.93€ du m²
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min: 6.26 du m²
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 7.89€ du m²
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_93.csv', sep=',', encoding='utf-8', index=False)

#%% Corse
Fusion = pd.concat([Fusion_d01_d21, Fusion_d22_d40, Fusion_d41_d60, Fusion_d61_d80, Fusion_d81_d974], axis = 0)
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:2]
Fusion['Dep'].value_counts()
Fusion = Fusion[(Fusion['Dep'] == "2A")|(Fusion['Dep'] == "2B")]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['datemut'] >= '2019-01-01') & (Fusion['datemut'] < '2020-01-01')]
list(Fusion.columns)
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Fusion = pd.merge(Fusion, Aires_urbaines, how="left", on=['ffcodinsee'])
Fusion = Fusion.dropna()
#%%
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('242010056', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})
#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=2)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=2)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 20, 
                                      max_depth= 4, 
                                      max_bins= 50, 
                                      loss= 'absolute_error', 
                                      learning_rate= 0.5, 
                                      l2_regularization= 0.2)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight = 2, 
                     max_depth = 3,
                     reg_lambda = 0.65, 
                     gamma = 2.2,  
                     eta = 0.15, 
                     booster = 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))

#%%
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R94.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)&
                            (Fusion_pred['npiece_ff'] > 0)]
#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred,  
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 9 620.08€ du m²
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min: 250.61 du m²
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 3 103.63€ du m²
Fusion_1_Pred = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price_sq_m'] > 0)]
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_94.csv', sep=',', encoding='utf-8', index=False)

#%% Guadeloupe
Fusion = Fusion_d971_d974
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:3]
Fusion['Dep'].value_counts()
Fusion = Fusion[(Fusion['Dep'] == "971")]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['datemut'] >= '2019-01-01') & (Fusion['datemut'] < '2020-01-01')]
#%%
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})
#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=2)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=2)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 20, 
                                      max_depth= 4, 
                                      max_bins= 50, 
                                      loss= 'absolute_error', 
                                      learning_rate= 0.5, 
                                      l2_regularization= 0.2)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight = 3, 
                     max_depth = 6,
                     reg_lambda = 0.2, 
                     gamma = 1.2,  
                     eta = 0.1, 
                     booster = 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))

#%%
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R01.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)&
                            (Fusion_pred['npiece_ff'] > 0)]
#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred,  
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 8.15
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min: 5.25
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 7.47
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_01.csv', sep=',', encoding='utf-8', index=False)

#%% Martinique
Fusion = Fusion_d971_d974
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:3]
Fusion['Dep'].value_counts()
Fusion = Fusion[(Fusion['Dep'] == "972")]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['datemut'] >= '2019-01-01') & (Fusion['datemut'] < '2020-01-01')]
list(Fusion.columns)
#%%
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})
#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=2)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=2)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 20, 
                                      max_depth= 4, 
                                      max_bins= 50, 
                                      loss= 'absolute_error', 
                                      learning_rate= 0.5, 
                                      l2_regularization= 0.2)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight = 1, 
                     max_depth = 4,
                     reg_lambda = 0.7, 
                     gamma = 0.6,  
                     eta = 0.2, 
                     booster = 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))

#%%
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R02.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)&
                            (Fusion_pred['npiece_ff'] > 0)]
#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred,  
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 8.19
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min: 4.93
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 7.50
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_02.csv', sep=',', encoding='utf-8', index=False)

#%% La réunion
Fusion = Fusion_d971_d974
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:3]
Fusion['Dep'].value_counts()
Fusion = Fusion[(Fusion['Dep'] == "974")]
Fusion = Fusion[(Fusion['ffnbpprinc'] > 0)]
Fusion = Fusion[(Fusion['libnatmut'] == 'Vente')]
Fusion = Fusion[(Fusion['datemut'] >= '2019-01-01') & (Fusion['datemut'] < '2020-01-01')]
list(Fusion.columns)
#%%
#%%
y = np.log(Fusion['valeurfonc']/Fusion['ffshab'])

Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Floor = pd.concat([Floor, Floor_mais], axis = 1)
list(Floor.columns)
Floor['RDC'] = Floor['RDC']*Floor['Appartement']
Floor['1-3'] = Floor['1-3']*Floor['Appartement']
Floor['4-6'] = Floor['4-6']*Floor['Appartement']
Floor['7+'] = Floor['7+']*Floor['Appartement']
Floor = Floor.drop('Appartement', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Longitude = Fusion['Longitude']
Latitude = Fusion['Latitude']

Parking = pd.cut(Fusion['ffnbpgarag'], bins=[-1,2,10000], labels=['0', '1'])
Parking = pd.get_dummies(Parking)
Parking = Parking.drop('0', axis=1)#Problème de variable: peu déclarée

Cave = pd.cut(Fusion['ffnbpaut'], bins=[0,1,10000], labels=['0', '1'])
Cave = pd.get_dummies(Cave)
Cave = Cave.drop('0', axis=1)
Cave = Cave.rename(columns={'1': 'Cave'})

Floor_mais = pd.get_dummies(Fusion['ffctyploc'])
Floor_mais = Floor_mais.drop(1, axis = 1)
Floor_mais = Floor_mais.rename(columns={2: 'Appartement'})
Etage_Max = pd.concat([Fusion['ffnbetage'],Floor_mais], axis = 1)
Etage_Max = Etage_Max['ffnbetage']*Etage_Max['Appartement']
Etage_Max = pd.DataFrame(Etage_Max)
Etage_Max = Etage_Max.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion['ffnbpprinc'] == 1) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 2) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] >= 4) & (Fusion['ffctyploc'] == 2)
    , (Fusion['ffnbpprinc'] <= 2) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 3) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] == 4) & (Fusion['ffctyploc'] == 1)
    , (Fusion['ffnbpprinc'] >= 5) & (Fusion['ffctyploc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")

Nb_piece = pd.get_dummies(Fusion["Nb_piece_App_Mais"])
Fusion['Nb_piece_App_Mais'].value_counts()
Nb_piece = Nb_piece.drop('4P_Mais', axis=1)

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})
#%%Modelling
#%%Linear regression
X_OLS = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Comm], axis = 1)
X_OLS.columns = X_OLS.columns.astype(str)
X_train_OLS, X_test_OLS, y_train, y_test = train_test_split(X_OLS, y, test_size=0.20, random_state=2)
OLS = LinearRegression()
OLS.fit(X_train_OLS, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test_OLS))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test_OLS))/y_test),0.75)*100,2)
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_test, OLS.predict(X_test_OLS))),2)
round(r2_score(y_test,OLS.predict(X_test_OLS)),3)
#%%
X = pd.concat([Floor, Const_Year,
               Cave, Etage_Max, Nb_piece, 
               Terrasse, Longitude, Latitude], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=2)

HGB = HistGradientBoostingRegressor()
param_grid = [{'loss': ['squared_error'],
              'learning_rate': arange(0, 0.9, 0.1),
              'l2_regularization': arange(0, 0.8, 0.05),
              'max_depth': arange(1, 5, 1),
              'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
              'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['absolute_error'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]},
              {'loss': ['quantile'],
                            'learning_rate': arange(0, 0.9, 0.1),
                            'l2_regularization': arange(0, 0.8, 0.05),
                            'max_depth': arange(1, 8, 1),
                            'max_leaf_nodes': [5, 10, 20, 30, 40, 50],
                            'max_bins': [5, 10, 20, 30, 40, 50]}]
grid = RandomizedSearchCV(HGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes= 20, 
                                      max_depth= 4, 
                                      max_bins= 50, 
                                      loss= 'absolute_error', 
                                      learning_rate= 0.5, 
                                      l2_regularization= 0.2)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))
#%%XGBoost
from xgboost import XGBRegressor
XGB = XGBRegressor()
param_grid = [{'booster': ['gbtree'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)},
              {'booster': ['gblinear'],
              'eta': arange(0, 0.8, 0.05),
              'gamma': arange(0, 4, 0.2),
              'max_depth': arange(1, 11, 1),
              'min_child_weight': arange(1, 6, 1),
              'lambda': arange(0, 0.8, 0.05)}]
grid = RandomizedSearchCV(XGB, param_grid, verbose = 1, cv=3,
                          n_iter = 500)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight = 4, 
                     max_depth = 9,
                     reg_lambda = 0.25, 
                     gamma = 0.8,  
                     eta = 0.1, 
                     booster = 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_test, model.predict(X_test))),2)
print('R² is: '+str(round(r2_score(y_test,model.predict(X_test)),2)))

#%%
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R04.csv",sep = ",")
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)&
                            (Fusion_pred['stoth'] <= 1000)&
                            (Fusion_pred['jannath'] > 0)&
                            (Fusion_pred['npiece_ff'] > 0)]
#
Floor_pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_pred = pd.get_dummies(Floor_pred)
Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Floor_pred = pd.concat([Floor_pred, Floor_pred_mais], axis = 1)
list(Floor_pred.columns)
Floor_pred['RDC'] = Floor_pred['RDC']*Floor_pred['Appartement']
Floor_pred['1-3'] = Floor_pred['1-3']*Floor_pred['Appartement']
Floor_pred['4-6'] = Floor_pred['4-6']*Floor_pred['Appartement']
Floor_pred['7+'] = Floor_pred['7+']*Floor_pred['Appartement']
Floor_pred = Floor_pred.drop('Appartement', axis=1)

Const_Year_pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1949,1981,1990,2001,2010,10000], labels=['Avant 1949', '1949-1980', '1981-1990','1991-2000','2000-2010','Après 2010'])
Const_Year_pred = pd.get_dummies(Const_Year_pred)
list(Const_Year_pred.columns)
Const_Year_pred = Const_Year_pred.drop('Avant 1949', axis=1)

Longitude_pred = Fusion_1_Pred['Longitude']
Latitude_pred = Fusion_1_Pred['Latitude']

Parking_pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,2,10000], labels=['0', '1'])
Parking_pred = pd.get_dummies(Parking_pred)
Parking_pred = Parking_pred.drop('0', axis=1)#Problème de variable: peu déclarée

Cave_pred = pd.cut(Fusion_1_Pred['nbannexe'], bins=[0,1,10000], labels=['0', '1'])
Cave_pred = pd.get_dummies(Cave_pred)
Cave_pred = Cave_pred.drop('0', axis=1)
Cave_pred = Cave_pred.rename(columns={'1': 'Cave'})

Floor_pred_mais = pd.get_dummies(Fusion_1_Pred['dteloc'])
Floor_pred_mais = Floor_pred_mais.drop(1, axis = 1)
Floor_pred_mais = Floor_pred_mais.rename(columns={2: 'Appartement'})
Etage_Max_pred = pd.concat([Fusion_1_Pred['nbetagemax'],Floor_pred_mais], axis = 1)
Etage_Max_pred = Fusion_1_Pred['nbetagemax']*Etage_Max_pred['Appartement']
Etage_Max_pred = pd.DataFrame(Etage_Max_pred)
Etage_Max_pred = Etage_Max_pred.rename(columns={0: 'Etage_Max'})

conditions = [
      (Fusion_1_Pred['npiece_ff'] == 1) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 2) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] >= 4) & (Fusion_1_Pred['dteloc'] == 2)
    , (Fusion_1_Pred['npiece_ff'] <= 2) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 3) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] == 4) & (Fusion_1_Pred['dteloc'] == 1)
    , (Fusion_1_Pred['npiece_ff'] >= 5) & (Fusion_1_Pred['dteloc'] == 1)
]

choices  = [
      "1P_APP"
    , "2P_APP"
    , "3P_APP"
    , "4P+_APP"
    ,"1_2P_Mais"
    , "3P_Mais"
    , "4P_Mais"
    , "5P+_Mais"
]
Fusion_1_Pred["Nb_piece_App_Mais"] = np.select(conditions, choices, "ERROR")
Nb_piece_pred = pd.get_dummies(Fusion_1_Pred["Nb_piece_App_Mais"])
Fusion_1_Pred['Nb_piece_App_Mais'].value_counts()
Nb_piece_pred = Nb_piece_pred.drop('4P_Mais', axis=1)

Terrasse_pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_pred = pd.get_dummies(Terrasse_pred)
Terrasse_pred = Terrasse_pred.drop('0', axis=1)
Terrasse_pred = Terrasse_pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_pred, Const_Year_pred,
               Cave_pred, Etage_Max_pred, Nb_piece_pred, 
               Terrasse_pred,  
               Longitude_pred, Latitude_pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)
list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price_sq_m'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price_sq_m'])#Max: 8.62
np.min(Fusion_1_Pred['Predicted_price_sq_m'])#Min: 6.30
mean(Fusion_1_Pred['Predicted_price_sq_m'])#Moyenne : 7.51
Fusion_1_Pred.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_04.csv', sep=',', encoding='utf-8', index=False)
