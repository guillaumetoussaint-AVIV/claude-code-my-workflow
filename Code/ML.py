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
#%%2022
#%%Appartements
Fusion_11 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/11_Fusion.csv",sep = ",")
Fusion_24 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/24_Fusion.csv",sep = ",")
Fusion_27 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/27_Fusion.csv",sep = ",")
Fusion_28 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/28_Fusion.csv",sep = ",")
Fusion_32 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/32_Fusion.csv",sep = ",")
Fusion_44 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/44_Fusion.csv",sep = ",")
Fusion_52 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/52_Fusion.csv",sep = ",")
Fusion_53 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/53_Fusion.csv",sep = ",")
Fusion_75 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/75_Fusion.csv",sep = ",")
Fusion_76 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/76_Fusion.csv",sep = ",")
Fusion_84 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/84_Fusion.csv",sep = ",")
Fusion_93 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/93_Fusion.csv",sep = ",")
Fusion_94 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/94_Fusion.csv",sep = ",")
Fusion = pd.concat([Fusion_11, Fusion_24, Fusion_27, Fusion_28, Fusion_32,
                    Fusion_44, Fusion_52, Fusion_53, Fusion_75, Fusion_76,
                    Fusion_84, Fusion_93, Fusion_94], axis=0).reset_index()
del(Fusion_11, Fusion_24, Fusion_27, Fusion_28, Fusion_32,
                    Fusion_44, Fusion_52, Fusion_53, Fusion_75, Fusion_76,
                    Fusion_84, Fusion_93, Fusion_94)
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
#Fusion = Fusion[(Fusion['ffctyploc'] == 1)]
Fusion = Fusion[(Fusion['datemut'] >= '2022-01-01') & (Fusion['datemut'] < '2023-01-01')]
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
list(Fusion.columns)
Fusion['Dep'] = Fusion['ffcodinsee'].astype(str).str[:2]
Fusion['Dep'].value_counts()
#Clusters = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Indices socio-démo_Cluster.xlsx')
#Fusion = pd.merge(Fusion, Clusters, how="left", on=['Dep'])
#list(Fusion.columns)
#Fusion = Fusion.reset_index(drop=True)
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Fusion = pd.merge(Fusion, Aires_urbaines, how="left", on=['ffcodinsee'])
Fusion = Fusion.reset_index(drop=True)
Fusion['LIB_DENS'].value_counts()
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Fusion = pd.merge(Fusion, Aires_urbaines, how="left", on=['ffcodinsee'])
#%%Grands centres urbains
Fusion_1 = Fusion[(Fusion['DENS'] == 1)]
#Par région et par densité ?
#%%
y = Fusion_1['valeurfonc']
Floor = pd.cut(Fusion_1['ffetage'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion_1['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion_1['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Comm_1 = pd.get_dummies(Fusion_1['EPCI'])
Comm_1.columns = Comm_1.columns.astype(str)
list(Comm_1.columns)
Comm_1 = Comm_1.drop('200068120', axis=1)

Comm = pd.get_dummies(Fusion_1['ffcodinsee'])
Comm.columns = Comm.columns.astype(str)
list(Comm.columns)
Comm = Comm.drop('59426', axis=1)

#Year = pd.get_dummies(Fusion_1['dateannee'])
#Year.columns = Year.columns.astype(str)
#Year = Year.drop('2012', axis=1)

Maison = pd.get_dummies(Fusion_1['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion_1['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion_1['ffshab']*Fusion_1['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion_1['ffsdep']

Garage = pd.cut(Fusion_1['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion_1['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
list(X_train.columns)
list(X_test.columns)
#%%Linear regression
#Hyperparamètres
from sklearn.linear_model import LinearRegression
OLS = LinearRegression()
OLS.fit(X_train, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test))/y_test),0.75)*100,2)
#SR
import random
sample_mean_y1 = []
sample_mean_y2 = []
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(OLS.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))

#%%Gradient boosting
X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm_1], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
list(X_train.columns)
list(X_test.columns)
#
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
grid = RandomizedSearchCV(HGB, param_grid, verbose = 3, cv=3,
                          n_iter = 100)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(loss = 'squared_error',
                     l2_regularization = 0.15,
                     max_depth = 4,
                     learning_rate = 0.8,
                     max_leaf_nodes = 50,
                     max_bins = 30)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
#SR
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(model.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
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
grid = RandomizedSearchCV(XGB, param_grid, verbose = 3, cv=3,
                          n_iter = 100)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight= 5, 
                     max_depth= 6,
                     reg_lambda= 0.05, 
                     gamma= 1.6, 
                     eta= 0.35, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
#SR
import random
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(model.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
#%%RF
RF = RandomForestRegressor()
param_grid = [{'criterion': ['absolute_error'],
              'max_depth': arange(1, 20, 1),
              'n_estimators': arange(20, 400, 10)},
              {'criterion': ['squared_error'],
              'max_depth': arange(1, 20, 1),
              'n_estimators': arange(20, 400, 10)}]
grid = RandomizedSearchCV(RF, param_grid, verbose = 3, cv=3,
                          n_iter = 100)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = RandomForestRegressor(criterion= , 
                     max_depth= ,
                     n_estimators= 0.)
# fit model
model.fit(X_train, y_train)
np.sqrt(mean_squared_error(y_train, model.predict(X_train)))
np.sqrt(mean_squared_error(y_test, model.predict(X_test)))
np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100
np.median(abs((y_test-model.predict(X_test))/y_test))*100
mean(abs((y_test-model.predict(X_test))/y_test))*100#27%
np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(model.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(np.mean(sample_mean_y2)/np.mean(sample_mean_y1))
#%%Prediction
Fusion_11 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R11.csv",sep = ",")
Fusion_24 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R24.csv",sep = ",")
Fusion_27 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R27.csv",sep = ",")
Fusion_28 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R28.csv",sep = ",")
Fusion_32 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R32.csv",sep = ",")
Fusion_44 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R44.csv",sep = ",")
Fusion_52 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R52.csv",sep = ",")
Fusion_53 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R53.csv",sep = ",")
Fusion_75 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R75.csv",sep = ",")
Fusion_76 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R76.csv",sep = ",")
Fusion_84 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R84.csv",sep = ",")
Fusion_93 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R93.csv",sep = ",")
Fusion_Pred_Sans_Corse = pd.concat([Fusion_11, Fusion_24, Fusion_27, Fusion_28, Fusion_32,
                    Fusion_44, Fusion_52, Fusion_53, Fusion_75, Fusion_76,
                    Fusion_84, Fusion_93], axis=0).reset_index()
Fusion_Pred_Sans_Corse['idcom'] = Fusion_Pred_Sans_Corse['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_Pred_Sans_Corse['idcom'].value_counts()
type(Fusion_Pred_Sans_Corse['idcom'])

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_Pred_Sans_Corse = pd.merge(Fusion_Pred_Sans_Corse, Aires_urbaines, how="left", on=['idcom'])
Fusion_Pred_Sans_Corse['DENS'].value_counts()

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_Pred_Sans_Corse = pd.merge(Fusion_Pred_Sans_Corse, Aires_urbaines, how="left", on=['idcom'])

Fusion_94 = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R94.csv",sep = ",")
type(Fusion_94['idcom'])
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_94 = pd.merge(Fusion_94, Aires_urbaines, how="left", on=['idcom'])
Fusion_94['LIB_DENS'].value_counts()

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_94 = pd.merge(Fusion_94, Aires_urbaines, how="left", on=['idcom'])

Fusion_Pred = pd.concat([Fusion_Pred_Sans_Corse, Fusion_94], axis=0).reset_index()
Fusion_Pred = Fusion_Pred[(Fusion_Pred['loghlls'] != 'OUI') & (Fusion_Pred['loghlls'] != 'OUI PROBABLE')]
list(Fusion_Pred.columns)
Fusion_Pred.drop(['ccodep', 'nbpiscine', 'nbannexe',
                      'loghlls'], axis=1, inplace=True)
#Fusion_Pred_1.shape[0]/Fusion_Pred.shape[0]
#Fusion_Pred.shape[0]-Fusion_Pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_Pred['Dep'] = Fusion_Pred['idcom'].astype(str).str[:2]
Fusion_Pred['Dep'].value_counts()
Fusion_Pred = Fusion_Pred[(Fusion_Pred['Dep'] != '57') 
                          & (Fusion_Pred['Dep'] != '67')
                          & (Fusion_Pred['Dep'] != '68')]

#%%
Fusion_1_Pred = Fusion_Pred[(Fusion_Pred['DENS'] == 1)]
list(Fusion_1_Pred.columns)
#%%
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Comm_1_Pred.columns = Comm_1_Pred.columns.astype(str)
list(Comm_1_Pred.columns)
Comm_1_Pred = Comm_1_Pred.drop('200068120', axis=1)

Maison_Pred = pd.get_dummies(Fusion_1_Pred['dteloc'])
Maison_Pred.columns = Maison_Pred.columns.astype(str)
Maison_Pred = Maison_Pred.drop('2', axis=1)

Surface_Pred = pd.DataFrame(Fusion_1_Pred['stoth'])
Surface_Pred = Surface_Pred.rename(columns={'stoth': 'Surface'})

Surface_sq_Pred = pd.DataFrame(Fusion_1_Pred['stoth']*Fusion_1_Pred['stoth'])
Surface_sq_Pred = Surface_sq_Pred.rename(columns={'stoth': 'Surface_sq'})

Surf_dep_Pred = pd.DataFrame(Fusion_1_Pred['stotd'])
Surf_dep_Pred = Surf_dep_Pred.rename(columns={'stotd': 'ffsdep'})

Garage_Pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,0,20], labels=['0', '1'])
Garage_Pred = pd.get_dummies(Garage_Pred)
Garage_Pred = Garage_Pred.drop('0', axis=1)
Garage_Pred = Garage_Pred.rename(columns={'1': 'Garage'})

Terrasse_Pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_Pred = pd.get_dummies(Terrasse_Pred)
Terrasse_Pred = Terrasse_Pred.drop('0', axis=1)
Terrasse_Pred = Terrasse_Pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_Pred, Terrasse_Pred, Const_Year_Pred,
                    Room_count_Pred, Surface_Pred,
                    Surface_sq_Pred,
               Surf_dep_Pred, Garage_Pred, Maison_Pred, Comm_1_Pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)

list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.max(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>0)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_Dens_1.csv', sep=',', encoding='utf-8')

#%% Paris
Fusion_1 = Fusion[(Fusion['DENS'] == 0)]
#Par région et par densité ?
#%%
y = Fusion_1['valeurfonc']
Floor = pd.cut(Fusion_1['ffetage'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion_1['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion_1['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Comm = pd.get_dummies(Fusion_1['ffcodinsee'])
Comm.columns = Comm.columns.astype(str)
list(Comm.columns)
Comm = Comm.drop('75115', axis=1)

#Year = pd.get_dummies(Fusion_1['dateannee'])
#Year.columns = Year.columns.astype(str)
#Year = Year.drop('2012', axis=1)

Maison = pd.get_dummies(Fusion_1['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion_1['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion_1['ffshab']*Fusion_1['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion_1['ffsdep']

Garage = pd.cut(Fusion_1['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion_1['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
list(X_train.columns)
list(X_test.columns)
#%%Linear regression
#Hyperparamètres
from sklearn.linear_model import LinearRegression
OLS = LinearRegression()
OLS.fit(X_train, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test))/y_test),0.75)*100,2)
#SR
import random
sample_mean_y1 = []
sample_mean_y2 = []
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(OLS.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))

#%%Gradient boosting
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
grid = RandomizedSearchCV(HGB, param_grid, verbose = 3, cv=3,
                          n_iter = 100)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(loss = 'squared_error',
                     l2_regularization = 0.7,
                     max_depth = 2,
                     learning_rate = 0.3,
                     max_leaf_nodes = 5,
                     max_bins = 50)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
#SR
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(model.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
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
grid = RandomizedSearchCV(XGB, param_grid, verbose = 3, cv=3,
                          n_iter = 100)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight= 2, 
                     max_depth= 4,
                     reg_lambda= 0.6, 
                     gamma= 0.8, 
                     eta= 0.1, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
#SR
import random
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(model.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
#%%
Fusion_1_Pred = Fusion_Pred[(Fusion_Pred['DENS'] == 0)]
list(Fusion_1_Pred.columns)
#%%
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_Pred = pd.get_dummies(Fusion_1_Pred['idcom'])
Comm_Pred.columns = Comm_Pred.columns.astype(str)
list(Comm_Pred.columns)
Comm_Pred = Comm_Pred.drop('75115', axis=1)

Maison_Pred = pd.get_dummies(Fusion_1_Pred['dteloc'])
Maison_Pred.columns = Maison_Pred.columns.astype(str)
Maison_Pred = Maison_Pred.drop('2', axis=1)

Surface_Pred = pd.DataFrame(Fusion_1_Pred['stoth'])
Surface_Pred = Surface_Pred.rename(columns={'stoth': 'Surface'})

Surface_sq_Pred = pd.DataFrame(Fusion_1_Pred['stoth']*Fusion_1_Pred['stoth'])
Surface_sq_Pred = Surface_sq_Pred.rename(columns={'stoth': 'Surface_sq'})

Surf_dep_Pred = pd.DataFrame(Fusion_1_Pred['stotd'])
Surf_dep_Pred = Surf_dep_Pred.rename(columns={'stotd': 'ffsdep'})

Garage_Pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,0,20], labels=['0', '1'])
Garage_Pred = pd.get_dummies(Garage_Pred)
Garage_Pred = Garage_Pred.drop('0', axis=1)
Garage_Pred = Garage_Pred.rename(columns={'1': 'Garage'})

Terrasse_Pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_Pred = pd.get_dummies(Terrasse_Pred)
Terrasse_Pred = Terrasse_Pred.drop('0', axis=1)
Terrasse_Pred = Terrasse_Pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_Pred, Terrasse_Pred, Const_Year_Pred,
                    Room_count_Pred, Surface_Pred,
                    Surface_sq_Pred,
               Surf_dep_Pred, Garage_Pred, Maison_Pred, Comm_Pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)

list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.min(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>0)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_Dens_0.csv', sep=',', encoding='utf-8')

#%% Centres urbains intermédiaires
Fusion_1 = Fusion[(Fusion['DENS'] == 2)]
#Par région et par densité ?
#%%
y = Fusion_1['valeurfonc']
Floor = pd.cut(Fusion_1['ffetage'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion_1['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion_1['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Comm_1 = pd.get_dummies(Fusion_1['EPCI'])
Comm_1.columns = Comm_1.columns.astype(str)
list(Comm_1.columns)
Comm_1 = Comm_1.drop('', axis=1)

Comm = pd.get_dummies(Fusion_1['ffcodinsee'])
Comm.columns = Comm.columns.astype(str)
list(Comm.columns)
Comm = Comm.drop('42095', axis=1)

#Year = pd.get_dummies(Fusion_1['dateannee'])
#Year.columns = Year.columns.astype(str)
#Year = Year.drop('2012', axis=1)

Maison = pd.get_dummies(Fusion_1['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion_1['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion_1['ffshab']*Fusion_1['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion_1['ffsdep']

Garage = pd.cut(Fusion_1['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion_1['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
list(X_train.columns)
list(X_test.columns)
#%%Linear regression
#Hyperparamètres
from sklearn.linear_model import LinearRegression
OLS = LinearRegression()
OLS.fit(X_train, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test))/y_test),0.75)*100,2)
#SR
import random
sample_mean_y1 = []
sample_mean_y2 = []
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(OLS.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))

#%%Gradient boosting
X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm_1], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
list(X_train.columns)
list(X_test.columns)
#
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
grid = RandomizedSearchCV(HGB, param_grid, verbose = 3, cv=3,
                          n_iter = 100)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(loss = 'squared_error',
                     l2_regularization = 0.0,
                     max_depth = 4,
                     learning_rate = 0.8,
                     max_leaf_nodes = 50,
                     max_bins = 50)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
#SR
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(model.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
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
grid = RandomizedSearchCV(XGB, param_grid, verbose = 3, cv=3,
                          n_iter = 100)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight= 3, 
                     max_depth= 5,
                     reg_lambda= 0.4, 
                     gamma= 2.4, 
                     eta= 0.25, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
#SR
import random
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(model.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
#%%Prédiction
Fusion_1_Pred = Fusion_Pred[(Fusion_Pred['DENS'] == 2)]
#%%
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Comm_1_Pred.columns = Comm_1_Pred.columns.astype(str)
list(Comm_1_Pred.columns)
Comm_1_Pred = Comm_1_Pred.drop('', axis=1)

Maison_Pred = pd.get_dummies(Fusion_1_Pred['dteloc'])
Maison_Pred.columns = Maison_Pred.columns.astype(str)
Maison_Pred = Maison_Pred.drop('2', axis=1)

Surface_Pred = pd.DataFrame(Fusion_1_Pred['stoth'])
Surface_Pred = Surface_Pred.rename(columns={'stoth': 'Surface'})

Surface_sq_Pred = pd.DataFrame(Fusion_1_Pred['stoth']*Fusion_1_Pred['stoth'])
Surface_sq_Pred = Surface_sq_Pred.rename(columns={'stoth': 'Surface_sq'})

Surf_dep_Pred = pd.DataFrame(Fusion_1_Pred['stotd'])
Surf_dep_Pred = Surf_dep_Pred.rename(columns={'stotd': 'ffsdep'})

Garage_Pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,0,20], labels=['0', '1'])
Garage_Pred = pd.get_dummies(Garage_Pred)
Garage_Pred = Garage_Pred.drop('0', axis=1)
Garage_Pred = Garage_Pred.rename(columns={'1': 'Garage'})

Terrasse_Pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_Pred = pd.get_dummies(Terrasse_Pred)
Terrasse_Pred = Terrasse_Pred.drop('0', axis=1)
Terrasse_Pred = Terrasse_Pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_Pred, Terrasse_Pred, Const_Year_Pred,
                    Room_count_Pred, Surface_Pred,
                    Surface_sq_Pred,
               Surf_dep_Pred, Garage_Pred, Maison_Pred, Comm_1_Pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)

list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.min(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>0)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_Dens_2.csv', sep=',', encoding='utf-8')

#%%Petites villes
Fusion_1 = Fusion[(Fusion['DENS'] == 3)]
Fusion_1['LIB_DENS'].value_counts()
#Par région et par densité ?
#%%
y = Fusion_1['valeurfonc']
Floor = pd.cut(Fusion_1['ffetage'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion_1['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion_1['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Comm_1 = pd.get_dummies(Fusion_1['EPCI'])
Comm_1.columns = Comm_1.columns.astype(str)
list(Comm_1.columns)
Comm_1 = Comm_1.drop('241927201', axis=1)

Comm = pd.get_dummies(Fusion_1['ffcodinsee'])
Comm.columns = Comm.columns.astype(str)
list(Comm.columns)
Comm = Comm.drop('76260', axis=1)

#Year = pd.get_dummies(Fusion_1['dateannee'])
#Year.columns = Year.columns.astype(str)
#Year = Year.drop('2012', axis=1)

Maison = pd.get_dummies(Fusion_1['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion_1['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion_1['ffshab']*Fusion_1['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion_1['ffsdep']

Garage = pd.cut(Fusion_1['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion_1['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
list(X_train.columns)
list(X_test.columns)
#%%Linear regression
#Hyperparamètres
from sklearn.linear_model import LinearRegression
OLS = LinearRegression()
OLS.fit(X_train, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test))/y_test),0.75)*100,2)
#SR
import random
sample_mean_y1 = []
sample_mean_y2 = []
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(OLS.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))

#%%Gradient boosting
X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm_1], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
list(X_train.columns)
list(X_test.columns)
#
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
grid = RandomizedSearchCV(HGB, param_grid, verbose = 3, cv=3,
                          n_iter = 100)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(loss = 'squared_error',
                     l2_regularization = 0.4,
                     max_depth = 4,
                     learning_rate = 0.3,
                     max_leaf_nodes = 30,
                     max_bins = 30)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
#SR
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(model.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
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
grid = RandomizedSearchCV(XGB, param_grid, verbose = 3, cv=3,
                          n_iter = 100)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight= 2, 
                     max_depth= 5,
                     reg_lambda= 0.6, 
                     gamma= 3.4, 
                     eta= 0.6, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
#SR
import random
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(model.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
#%%Prédiction
Fusion_1_Pred = Fusion_Pred[(Fusion_Pred['DENS'] == 3)]
#%%
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Comm_1_Pred.columns = Comm_1_Pred.columns.astype(str)
list(Comm_1_Pred.columns)
Comm_1_Pred = Comm_1_Pred.drop('241927201', axis=1)

Maison_Pred = pd.get_dummies(Fusion_1_Pred['dteloc'])
Maison_Pred.columns = Maison_Pred.columns.astype(str)
Maison_Pred = Maison_Pred.drop('2', axis=1)

Surface_Pred = pd.DataFrame(Fusion_1_Pred['stoth'])
Surface_Pred = Surface_Pred.rename(columns={'stoth': 'Surface'})

Surface_sq_Pred = pd.DataFrame(Fusion_1_Pred['stoth']*Fusion_1_Pred['stoth'])
Surface_sq_Pred = Surface_sq_Pred.rename(columns={'stoth': 'Surface_sq'})

Surf_dep_Pred = pd.DataFrame(Fusion_1_Pred['stotd'])
Surf_dep_Pred = Surf_dep_Pred.rename(columns={'stotd': 'ffsdep'})

Garage_Pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,0,20], labels=['0', '1'])
Garage_Pred = pd.get_dummies(Garage_Pred)
Garage_Pred = Garage_Pred.drop('0', axis=1)
Garage_Pred = Garage_Pred.rename(columns={'1': 'Garage'})

Terrasse_Pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_Pred = pd.get_dummies(Terrasse_Pred)
Terrasse_Pred = Terrasse_Pred.drop('0', axis=1)
Terrasse_Pred = Terrasse_Pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_Pred, Terrasse_Pred, Const_Year_Pred,
                    Room_count_Pred, Surface_Pred,
                    Surface_sq_Pred,
               Surf_dep_Pred, Garage_Pred, Maison_Pred, Comm_1_Pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)

list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.min(Fusion_1_Pred['Predicted_price'])
np.max(Fusion_1_Pred['Predicted_price'])
mean(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>0)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_Dens_3.csv', sep=',', encoding='utf-8')
#%%Ceintures urbaines
Fusion_1 = Fusion[(Fusion['DENS'] == 4)]
Fusion_1['LIB_DENS'].value_counts()
#Par région et par densité ?
#%%
y = Fusion_1['valeurfonc']
Floor = pd.cut(Fusion_1['ffetage'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion_1['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion_1['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Comm_1 = pd.get_dummies(Fusion_1['EPCI'])
Comm_1.columns = Comm_1.columns.astype(str)
list(Comm_1.columns)
Comm_1 = Comm_1.drop('247400690', axis=1)

Comm = pd.get_dummies(Fusion_1['ffcodinsee'])
Comm.columns = Comm.columns.astype(str)
list(Comm.columns)
Comm = Comm.drop('54366', axis=1)

#Year = pd.get_dummies(Fusion_1['dateannee'])
#Year.columns = Year.columns.astype(str)
#Year = Year.drop('2012', axis=1)

Maison = pd.get_dummies(Fusion_1['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion_1['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion_1['ffshab']*Fusion_1['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion_1['ffsdep']

Garage = pd.cut(Fusion_1['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion_1['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
list(X_train.columns)
list(X_test.columns)
#%%Linear regression
#Hyperparamètres
from sklearn.linear_model import LinearRegression
OLS = LinearRegression()
OLS.fit(X_train, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test))/y_test),0.75)*100,2)
#SR
import random
sample_mean_y1 = []
sample_mean_y2 = []
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(OLS.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
#%%Gradient boosting
X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm_1], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
list(X_train.columns)
list(X_test.columns)
#
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
grid = RandomizedSearchCV(HGB, param_grid, verbose = 3, cv=3,
                          n_iter = 100)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(loss = 'squared_error',
                     l2_regularization = 0.0,
                     max_depth = 3,
                     learning_rate = 0.6,
                     max_leaf_nodes = 10,
                     max_bins = 30)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
#SR
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(model.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
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
grid = RandomizedSearchCV(XGB, param_grid, verbose = 3, cv=3,
                          n_iter = 100)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight= 4, 
                     max_depth= 4,
                     reg_lambda= 0.5, 
                     gamma= 3.2, 
                     eta= 0.45, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
#SR
import random
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(model.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
#%%Prédiction
Fusion_1_Pred = Fusion_Pred[(Fusion_Pred['DENS'] == 4)]
#%%
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Comm_1_Pred.columns = Comm_1_Pred.columns.astype(str)
list(Comm_1_Pred.columns)
Comm_1_Pred = Comm_1_Pred.drop('247400690', axis=1)

Maison_Pred = pd.get_dummies(Fusion_1_Pred['dteloc'])
Maison_Pred.columns = Maison_Pred.columns.astype(str)
Maison_Pred = Maison_Pred.drop('2', axis=1)

Surface_Pred = pd.DataFrame(Fusion_1_Pred['stoth'])
Surface_Pred = Surface_Pred.rename(columns={'stoth': 'Surface'})

Surface_sq_Pred = pd.DataFrame(Fusion_1_Pred['stoth']*Fusion_1_Pred['stoth'])
Surface_sq_Pred = Surface_sq_Pred.rename(columns={'stoth': 'Surface_sq'})

Surf_dep_Pred = pd.DataFrame(Fusion_1_Pred['stotd'])
Surf_dep_Pred = Surf_dep_Pred.rename(columns={'stotd': 'ffsdep'})

Garage_Pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,0,20], labels=['0', '1'])
Garage_Pred = pd.get_dummies(Garage_Pred)
Garage_Pred = Garage_Pred.drop('0', axis=1)
Garage_Pred = Garage_Pred.rename(columns={'1': 'Garage'})

Terrasse_Pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_Pred = pd.get_dummies(Terrasse_Pred)
Terrasse_Pred = Terrasse_Pred.drop('0', axis=1)
Terrasse_Pred = Terrasse_Pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_Pred, Terrasse_Pred, Const_Year_Pred,
                    Room_count_Pred, Surface_Pred,
                    Surface_sq_Pred,
               Surf_dep_Pred, Garage_Pred, Maison_Pred, Comm_1_Pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)

list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.min(Fusion_1_Pred['Predicted_price'])
np.max(Fusion_1_Pred['Predicted_price'])
mean(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>0)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_Dens_4.csv', sep=',', encoding='utf-8')

#%%Bourgs ruraux
Fusion_1 = Fusion[(Fusion['DENS'] == 5)]
Fusion_1['LIB_DENS'].value_counts()
#Par région et par densité ?
#%%
y = Fusion_1['valeurfonc']
Floor = pd.cut(Fusion_1['ffetage'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion_1['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion_1['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Comm_1 = pd.get_dummies(Fusion_1['Dep'])
Comm_1.columns = Comm_1.columns.astype(str)
Fusion_1['Dep'].value_counts()
Comm_1 = Comm_1.drop('85', axis=1)

Comm = pd.get_dummies(Fusion_1['ffcodinsee'])
Comm.columns = Comm.columns.astype(str)
Fusion_1['ffcodinsee'].value_counts()
Comm = Comm.drop('83107', axis=1)

#Year = pd.get_dummies(Fusion_1['dateannee'])
#Year.columns = Year.columns.astype(str)
#Year = Year.drop('2012', axis=1)

Maison = pd.get_dummies(Fusion_1['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion_1['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion_1['ffshab']*Fusion_1['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion_1['ffsdep']

Garage = pd.cut(Fusion_1['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion_1['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
list(X_train.columns)
list(X_test.columns)
#%%Linear regression
#Hyperparamètres
from sklearn.linear_model import LinearRegression
OLS = LinearRegression()
OLS.fit(X_train, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test))/y_test),0.75)*100,2)
#SR
import random
sample_mean_y1 = []
sample_mean_y2 = []
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(OLS.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
#%%Gradient boosting
X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm_1], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
list(X_train.columns)
list(X_test.columns)
#
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
grid = RandomizedSearchCV(HGB, param_grid, verbose = 3, cv=3,
                          n_iter = 100)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(loss = 'squared_error',
                     l2_regularization = 0.55,
                     max_depth = 3,
                     learning_rate = 0.3,
                     max_leaf_nodes = 10,
                     max_bins = 50)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
#SR
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(model.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
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
grid = RandomizedSearchCV(XGB, param_grid, verbose = 3, cv=3,
                          n_iter = 100)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight= 3, 
                     max_depth= 8,
                     reg_lambda= 0.6, 
                     gamma= 3.2, 
                     eta= 0.5, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
#SR
import random
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(model.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
#%%Prédiction
Fusion_1_Pred = Fusion_Pred[(Fusion_Pred['DENS'] == 5)]
#%%
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['Dep'])
Comm_1_Pred.columns = Comm_1_Pred.columns.astype(str)
list(Comm_1_Pred.columns)
Comm_1_Pred = Comm_1_Pred.drop('85', axis=1)

Maison_Pred = pd.get_dummies(Fusion_1_Pred['dteloc'])
Maison_Pred.columns = Maison_Pred.columns.astype(str)
Maison_Pred = Maison_Pred.drop('2', axis=1)

Surface_Pred = pd.DataFrame(Fusion_1_Pred['stoth'])
Surface_Pred = Surface_Pred.rename(columns={'stoth': 'Surface'})

Surface_sq_Pred = pd.DataFrame(Fusion_1_Pred['stoth']*Fusion_1_Pred['stoth'])
Surface_sq_Pred = Surface_sq_Pred.rename(columns={'stoth': 'Surface_sq'})

Surf_dep_Pred = pd.DataFrame(Fusion_1_Pred['stotd'])
Surf_dep_Pred = Surf_dep_Pred.rename(columns={'stotd': 'ffsdep'})

Garage_Pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,0,20], labels=['0', '1'])
Garage_Pred = pd.get_dummies(Garage_Pred)
Garage_Pred = Garage_Pred.drop('0', axis=1)
Garage_Pred = Garage_Pred.rename(columns={'1': 'Garage'})

Terrasse_Pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_Pred = pd.get_dummies(Terrasse_Pred)
Terrasse_Pred = Terrasse_Pred.drop('0', axis=1)
Terrasse_Pred = Terrasse_Pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_Pred, Terrasse_Pred, Const_Year_Pred,
                    Room_count_Pred, Surface_Pred,
                    Surface_sq_Pred,
               Surf_dep_Pred, Garage_Pred, Maison_Pred, Comm_1_Pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)

list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.min(Fusion_1_Pred['Predicted_price'])
np.max(Fusion_1_Pred['Predicted_price'])
mean(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>0)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_Dens_5.csv', sep=',', encoding='utf-8')

#%%Zones rurales
Fusion_1 = Fusion[(Fusion['DENS'] == 6) | (Fusion['DENS'] == 7)]
Fusion_1['LIB_DENS'].value_counts()
#Par région et par densité ?
#%%
y = Fusion_1['valeurfonc']
Floor = pd.cut(Fusion_1['ffetage'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion_1['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion_1['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Comm_1 = pd.get_dummies(Fusion_1['Dep'])
Comm_1.columns = Comm_1.columns.astype(str)
Fusion_1['Dep'].value_counts()
Comm_1 = Comm_1.drop('24', axis=1)

Comm = pd.get_dummies(Fusion_1['ffcodinsee'])
Comm.columns = Comm.columns.astype(str)
Fusion_1['ffcodinsee'].value_counts()
Comm = Comm.drop('83068', axis=1)

#Year = pd.get_dummies(Fusion_1['dateannee'])
#Year.columns = Year.columns.astype(str)
#Year = Year.drop('2012', axis=1)

Maison = pd.get_dummies(Fusion_1['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion_1['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion_1['ffshab']*Fusion_1['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion_1['ffsdep']

Garage = pd.cut(Fusion_1['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion_1['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
list(X_train.columns)
list(X_test.columns)
#%%Linear regression
#Hyperparamètres
from sklearn.linear_model import LinearRegression
OLS = LinearRegression()
OLS.fit(X_train, y_train)
round(np.quantile(abs((y_test-OLS.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-OLS.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-OLS.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-OLS.predict(X_test))/y_test),0.75)*100,2)
#SR
import random
sample_mean_y1 = []
sample_mean_y2 = []
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(OLS.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
#%%Gradient boosting
X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm_1], axis = 1)
X.columns = X.columns.astype(str)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
list(X_train.columns)
list(X_test.columns)
#
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
grid = RandomizedSearchCV(HGB, param_grid, verbose = 3, cv=3,
                          n_iter = 100)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(loss = 'squared_error',
                     l2_regularization = 0.75,
                     max_depth = 3,
                     learning_rate = 0.8,
                     max_leaf_nodes = 10,
                     max_bins = 40)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
#SR
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(model.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
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
grid = RandomizedSearchCV(XGB, param_grid, verbose = 3, cv=3,
                          n_iter = 100)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight= 4, 
                     max_depth= 3,
                     reg_lambda= 0.1, 
                     gamma= 3, 
                     eta= 0.3, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
#SR
import random
for i in range(1000):
  y1 = random.sample(y_test.tolist(), 4)
  y2 = random.sample(model.predict(X_test).tolist(), 4)
  avg_y1 = np.mean(y1)
  avg_y2 = np.mean(y2)
  sample_mean_y1.append(avg_y1)
  sample_mean_y2.append(avg_y2)
print(round(np.mean(sample_mean_y2)/np.mean(sample_mean_y1),3))
#%%Prédiction
Fusion_1_Pred = Fusion_Pred[(Fusion_Pred['DENS'] == 6) | (Fusion_Pred['DENS'] == 7)]
#%%
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['Dep'])
Comm_1_Pred.columns = Comm_1_Pred.columns.astype(str)
list(Comm_1_Pred.columns)
Comm_1_Pred = Comm_1_Pred.drop('24', axis=1)

Maison_Pred = pd.get_dummies(Fusion_1_Pred['dteloc'])
Maison_Pred.columns = Maison_Pred.columns.astype(str)
Maison_Pred = Maison_Pred.drop('2', axis=1)

Surface_Pred = pd.DataFrame(Fusion_1_Pred['stoth'])
Surface_Pred = Surface_Pred.rename(columns={'stoth': 'Surface'})

Surface_sq_Pred = pd.DataFrame(Fusion_1_Pred['stoth']*Fusion_1_Pred['stoth'])
Surface_sq_Pred = Surface_sq_Pred.rename(columns={'stoth': 'Surface_sq'})

Surf_dep_Pred = pd.DataFrame(Fusion_1_Pred['stotd'])
Surf_dep_Pred = Surf_dep_Pred.rename(columns={'stotd': 'ffsdep'})

Garage_Pred = pd.cut(Fusion_1_Pred['nbgarpark'], bins=[-1,0,20], labels=['0', '1'])
Garage_Pred = pd.get_dummies(Garage_Pred)
Garage_Pred = Garage_Pred.drop('0', axis=1)
Garage_Pred = Garage_Pred.rename(columns={'1': 'Garage'})

Terrasse_Pred = pd.cut(Fusion_1_Pred['nbterrasse'], bins=[-1,0,20], labels=['0', '1'])
Terrasse_Pred = pd.get_dummies(Terrasse_Pred)
Terrasse_Pred = Terrasse_Pred.drop('0', axis=1)
Terrasse_Pred = Terrasse_Pred.rename(columns={'1': 'Terrasse'})

X_pred = pd.concat([Floor_Pred, Terrasse_Pred, Const_Year_Pred,
                    Room_count_Pred, Surface_Pred,
                    Surface_sq_Pred,
               Surf_dep_Pred, Garage_Pred, Maison_Pred, Comm_1_Pred], axis = 1)
X_pred.columns = X_pred.columns.astype(str)

list(X.columns)
list(X_pred.columns)

y_pred = model.predict(X_pred)
y_pred = pd.DataFrame(y_pred)
y_pred = y_pred.rename(columns={0 : 'Predicted_price'})
y_pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred.reset_index(drop=True, inplace=True)
Fusion_1_Pred = pd.concat([y_pred, Fusion_1_Pred], axis = 1)
np.min(Fusion_1_Pred['Predicted_price'])
np.max(Fusion_1_Pred['Predicted_price'])
mean(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>0)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_Dens_6_7.csv', sep=',', encoding='utf-8')
