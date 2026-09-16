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

#%%Paris
Fusion = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/11_Fusion.csv",sep = ",")
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
Fusion = Fusion[(Fusion['DENS'] == 0)]
#%%
y = Fusion['valeurfonc']/Fusion['ffshab']
Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Comm = pd.get_dummies(Fusion['ffcodinsee'])
Fusion['ffcodinsee'].value_counts()
Comm = Comm.drop('75115', axis=1)

Maison = pd.get_dummies(Fusion['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(np.log(Fusion['ffshab']))
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surf_dep = Fusion['ffsdep']

Garage = pd.cut(Fusion['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, #Surface,
               #Surf_dep, 
               Garage, #Maison, 
               Comm], axis = 1)

+ cave piscine terrain pour les maisons
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
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_train, model.predict(X_train))),2)
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
#%%
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
                          n_iter = 300)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes = 30,
                                     max_depth = 2, 
                                     max_bins = 10, 
                                     loss = 'squared_error', 
                                     learning_rate = 0.3, 
                                     l2_regularization = 0.55)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_train, model.predict(X_train))),2)
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
                          n_iter = 300)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight= 1,
                     max_depth= 1,
                     reg_lambda= 0.45,
                     gamma= 0.8,
                     eta= 0.3,
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(mean_squared_error(y_test, OLS.predict(X_test), squared=False),2)
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
model.fit(X, y)
#%% Prédiction
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R11.csv",sep = ",")
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred['DENS'].value_counts()

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
list(Fusion_pred.columns)
Fusion_pred.drop(['ccodep', 'nbpiscine', 'nbannexe',
                      'loghlls'], axis=1, inplace=True)
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['DENS'] = 0)]
Fusion_1_Pred = Fusion_1_Pred[(Fusion_1_Pred['stoth'] >= 9)]

#
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Comm_Pred.columns = Comm_Pred.columns.astype(str)
Fusion['EPCI'].value_counts()
Comm_Pred = Comm_Pred.drop('200054781', axis=1)

Maison_Pred = pd.get_dummies(Fusion_1_Pred['dteloc'])
Maison_Pred.columns = Maison_Pred.columns.astype(str)
Maison_Pred = Maison_Pred.drop('2', axis=1)

Surface_Pred = pd.DataFrame(np.log(Fusion_1_Pred['stoth']))
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
np.max(Fusion_1_Pred['Predicted_price'])
np.min(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>100)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_predict_Paris.csv', sep=',', encoding='utf-8')

#%% IDF
Fusion = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/11_Fusion.csv",sep = ",")
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
Fusion = Fusion[(Fusion['DENS'] != 0)]
#%%
y = Fusion['valeurfonc']/Fusion['ffshab']
Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('200054781', axis=1)

Maison = pd.get_dummies(Fusion['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(np.log(Fusion['ffshab']))
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surf_dep = Fusion['ffsdep']

Garage = pd.cut(Fusion['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,
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
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_train, model.predict(X_train))),2)
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
#%%
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
                          n_iter = 300)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = HistGradientBoostingRegressor(max_leaf_nodes = 10,
                                     max_depth = 4, 
                                     max_bins = 30, 
                                     loss = 'squared_error', 
                                     learning_rate = 0.6, 
                                     l2_regularization = 0.1)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_train, model.predict(X_train))),2)
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
                          n_iter = 300)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight= 3,
                     max_depth= 9,
                     reg_lambda= 0.3,
                     gamma= 1,
                     eta= 0.3,
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(mean_squared_error(y_test, OLS.predict(X_test), squared=False),2)
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
model.fit(X, y)
#%% Prédiction
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R11.csv",sep = ",")
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred['DENS'].value_counts()

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
list(Fusion_pred.columns)
Fusion_pred.drop(['ccodep', 'nbpiscine', 'nbannexe',
                      'loghlls'], axis=1, inplace=True)
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['DENS'] != 0)]
Fusion_1_Pred = Fusion_1_Pred[(Fusion_1_Pred['stoth'] >= 9)]

#
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,50], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Comm_Pred.columns = Comm_Pred.columns.astype(str)
Fusion['EPCI'].value_counts()
Comm_Pred = Comm_Pred.drop('200054781', axis=1)

Maison_Pred = pd.get_dummies(Fusion_1_Pred['dteloc'])
Maison_Pred.columns = Maison_Pred.columns.astype(str)
Maison_Pred = Maison_Pred.drop('2', axis=1)

Surface_Pred = pd.DataFrame(np.log(Fusion_1_Pred['stoth']))
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
np.max(Fusion_1_Pred['Predicted_price'])
np.min(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>100)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_predict_R_11.csv', sep=',', encoding='utf-8')

#%% Centre val de Loire
Fusion = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/24_Fusion.csv",sep = ",")
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
#%%
y = Fusion['valeurfonc']/Fusion['ffshab']
Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Comm_1 = pd.get_dummies(Fusion['DENS'])
Comm_1.columns = Comm_1.columns.astype(str)
list(Comm_1.columns)
Comm_1 = Comm_1.drop('1.0', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('243700754', axis=1)

Maison = pd.get_dummies(Fusion['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(np.log(Fusion['ffshab']))
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion['ffshab']*Fusion['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion['ffsdep']

Garage = pd.cut(Fusion['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,
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
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_train, OLS.predict(X_train))),2)
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
#%%
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
model = HistGradientBoostingRegressor(max_leaf_nodes= 10, 
                                      max_depth= 4, max_bins= 40, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.4, 
                                      l2_regularization= 0.0)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_train, model.predict(X_train))),2)
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
                          n_iter = 300)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight= 4, 
                     max_depth= 4,
                     reg_lambda= 0.0, 
                     gamma= 3.6, 
                     eta= 0.7, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(mean_squared_error(y_test, OLS.predict(X_test), squared=False),2)
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
model.fit(X, y)
#%% Prédiction
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R24.csv",sep = ",")
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred['DENS'].value_counts()

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
list(Fusion_pred.columns)
Fusion_pred['EPCI'].value_counts()
Fusion_pred.drop(['ccodep', 'nbpiscine', 'nbannexe',
                      'loghlls'], axis=1, inplace=True)
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)]
#
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Fusion_1_Pred['EPCI'].value_counts()
Comm_Pred = Comm_Pred.drop('243700754', axis=1)

Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['DENS'])
Comm_1_Pred.columns = Comm_1_Pred.columns.astype(str)
list(Comm_1.columns)
Comm_1_Pred = Comm_1_Pred.drop('1.0', axis=1)

Maison_Pred = pd.get_dummies(Fusion_1_Pred['dteloc'])
Maison_Pred.columns = Maison_Pred.columns.astype(str)
Maison_Pred = Maison_Pred.drop('2', axis=1)

Surface_Pred = pd.DataFrame(np.log(Fusion_1_Pred['stoth']))
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
np.max(Fusion_1_Pred['Predicted_price'])
np.min(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>100)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_predict_R_24.csv', sep=',', encoding='utf-8')

#%% Bourgogne Franche comté
Fusion = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/27_Fusion.csv",sep = ",")
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
#%%
y = Fusion['valeurfonc']/Fusion['ffshab']
Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Comm_1 = pd.get_dummies(Fusion['DENS'])
Comm_1.columns = Comm_1.columns.astype(str)
list(Comm_1.columns)
Comm_1 = Comm_1.drop('1.0', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('242500361', axis=1)

Maison = pd.get_dummies(Fusion['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion['ffshab']*Fusion['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion['ffsdep']

Garage = pd.cut(Fusion['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
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
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_train, OLS.predict(X_train))),2)
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
#%%
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
model = HistGradientBoostingRegressor(max_leaf_nodes= 50, 
                                      max_depth= 3, max_bins= 50, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.8, 
                                      l2_regularization= 0.75)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_train, model.predict(X_train))),2)
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
                     max_depth= 9,
                     reg_lambda= 0.3, 
                     gamma= 0, 
                     eta= 0.25, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(mean_squared_error(y_test, OLS.predict(X_test), squared=False),2)
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
model.fit(X, y)
#%% Prédiction
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R27.csv",sep = ",")
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred['DENS'].value_counts()

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
list(Fusion_pred.columns)
Fusion_pred['EPCI'].value_counts()
Fusion_pred.drop(['ccodep', 'nbpiscine', 'nbannexe',
                      'loghlls'], axis=1, inplace=True)
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)]
#
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Fusion_1_Pred['EPCI'].value_counts()
Comm_Pred = Comm_Pred.drop('242500361', axis=1)

Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['DENS'])
Comm_1_Pred.columns = Comm_1_Pred.columns.astype(str)
list(Comm_1.columns)
Comm_1_Pred = Comm_1_Pred.drop('1.0', axis=1)

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
np.max(Fusion_1_Pred['Predicted_price'])
np.min(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>100)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_predict_R_27.csv', sep=',', encoding='utf-8')

#%% Normandie
Fusion = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/28_Fusion.csv",sep = ",")
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
#%%
y = Fusion['valeurfonc']/Fusion['ffshab']
Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Comm_1 = pd.get_dummies(Fusion['DENS'])
Comm_1.columns = Comm_1.columns.astype(str)
list(Comm_1.columns)
Comm_1 = Comm_1.drop('1', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('200023414', axis=1)

Maison = pd.get_dummies(Fusion['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion['ffshab']*Fusion['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion['ffsdep']

Garage = pd.cut(Fusion['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
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
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_train, OLS.predict(X_train))),2)
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
#%%
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
model = HistGradientBoostingRegressor(max_leaf_nodes= 50, 
                                      max_depth= 4, 
                                      max_bins= 30, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.4, 
                                      l2_regularization= 0.4)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_train, model.predict(X_train))),2)
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
                     max_depth= 4,
                     reg_lambda= 0.4, 
                     gamma= 2.2, 
                     eta= 0.3, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(mean_squared_error(y_test, model.predict(X_test), squared=False),2)
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
model.fit(X, y)
#%% Prédiction
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R28.csv",sep = ",")
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred['DENS'].value_counts()

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
list(Fusion_pred.columns)
Fusion_pred['EPCI'].value_counts()
Fusion_pred.drop(['ccodep', 'nbpiscine', 'nbannexe',
                      'loghlls'], axis=1, inplace=True)
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)]
#
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Fusion_1_Pred['EPCI'].value_counts()
Comm_Pred = Comm_Pred.drop('200023414', axis=1)

Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].astype(str)
Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].str.replace('.0','')
Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['DENS'])
list(Comm_1_Pred.columns)
Comm_1_Pred = Comm_1_Pred.drop('1', axis=1)

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
np.max(Fusion_1_Pred['Predicted_price'])
np.min(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>100)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_predict_R_28.csv', sep=',', encoding='utf-8')

#%% Hauts de France
Fusion = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/32_Fusion.csv",sep = ",")
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
#Fusion = Fusion[(Fusion['ffctyploc'] == 1)]
Fusion = Fusion[(Fusion['datemut'] >= '2022-01-01') & (Fusion['datemut'] < '2023-01-01')]
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
list(Fusion.columns)
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
Fusion = Fusion[Fusion['DENS'].notna()]
#%% PROBLEMES DE NA
y = Fusion['valeurfonc']/Fusion['ffshab']
Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Fusion['DENS'] = Fusion['DENS'].astype(str)
Fusion['DENS'] = Fusion['DENS'].str.replace('.0','')
Fusion['DENS'].value_counts()
Fusion = Fusion[(Fusion['DENS'] != 'nan')]
Comm_1 = pd.get_dummies(Fusion['DENS'])
Comm_1.columns = Comm_1.columns.astype(str)
list(Comm_1.columns)
Comm_1 = Comm_1.drop('1', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('200093201', axis=1)

Maison = pd.get_dummies(Fusion['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion['ffshab']*Fusion['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion['ffsdep']

Garage = pd.cut(Fusion['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm], axis = 1)
X = X.dropna()
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
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_train, OLS.predict(X_train))),2)
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
#%%
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
model = HistGradientBoostingRegressor(max_leaf_nodes= 40, 
                                      max_depth= 2, 
                                      max_bins= 50, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.5, 
                                      l2_regularization= 0.7)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_train, model.predict(X_train))),2)
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
                     max_depth= 10,
                     reg_lambda= 0.1, 
                     gamma= 3.6, 
                     eta= 0.25, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(mean_squared_error(y_test, model.predict(X_test), squared=False),2)
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
model.fit(X, y)
#%% Prédiction
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R32.csv",sep = ",")
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred['DENS'].value_counts()

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
list(Fusion_pred.columns)
Fusion_pred['EPCI'].value_counts()
Fusion_pred.drop(['ccodep', 'nbpiscine', 'nbannexe',
                      'loghlls'], axis=1, inplace=True)
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)]
Fusion_1_Pred = Fusion_1_Pred[Fusion_1_Pred['DENS'].notna()]
#
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Fusion_1_Pred['EPCI'].value_counts()
Comm_Pred = Comm_Pred.drop('200093201', axis=1)

Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].astype(str)
Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].str.replace('.0','')
Fusion_1_Pred['DENS'].value_counts()
Fusion_1_Pred = Fusion_1_Pred[(Fusion_1_Pred['DENS'] != 'nan')]
Fusion_1_Pred['DENS'].value_counts()
Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['DENS'])
Comm_1_Pred = Comm_1_Pred.drop('1', axis=1)

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
np.max(Fusion_1_Pred['Predicted_price'])
np.min(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>100)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_predict_R_32.csv', sep=',', encoding='utf-8')

#%% Grand Est
Fusion = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/44_Fusion.csv",sep = ",")
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
#%%
y = Fusion['valeurfonc']/Fusion['ffshab']
Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Comm_1 = pd.get_dummies(Fusion['DENS'])
Comm_1.columns = Comm_1.columns.astype(str)
list(Comm_1.columns)
Comm_1 = Comm_1.drop('1', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('200067213', axis=1)

Maison = pd.get_dummies(Fusion['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion['ffshab']*Fusion['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion['ffsdep']

Garage = pd.cut(Fusion['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
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
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_train, OLS.predict(X_train))),2)
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
#%%
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
model = HistGradientBoostingRegressor(max_leaf_nodes= 40, 
                                      max_depth= 4, 
                                      max_bins= 10, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.8, 
                                      l2_regularization= 0.0)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_train, model.predict(X_train))),2)
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
                          n_iter = 300)
results = grid.fit(X_train, y_train)
# Summarize
print('Config: %s' % results.best_params_)
model = XGBRegressor(min_child_weight= 5, 
                     max_depth= 7,
                     reg_lambda= 0.75, 
                     gamma= 3.2, 
                     eta= 0.3, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(mean_squared_error(y_test, model.predict(X_test), squared=False),2)
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
model.fit(X, y)

#%% Prédiction
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R44.csv",sep = ",")
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred['DENS'].value_counts()

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
list(Fusion_pred.columns)
Fusion_pred['EPCI'].value_counts()
Fusion_pred.drop(['ccodep', 'nbpiscine', 'nbannexe',
                      'loghlls'], axis=1, inplace=True)
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)]
Fusion_1_Pred['Dep'] = Fusion_1_Pred['idcom'].astype(str).str[:2]
Fusion_1_Pred['Dep'].value_counts()
Fusion_1_Pred = Fusion_1_Pred[(Fusion_1_Pred['Dep'] != '57') 
                          & (Fusion_1_Pred['Dep'] != '67')
                          & (Fusion_1_Pred['Dep'] != '68')]
#
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Fusion_1_Pred['EPCI'].value_counts()
Comm_Pred = Comm_Pred.drop('200067213', axis=1)

Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].astype(str)
Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].str.replace('.0','')
Fusion_1_Pred['DENS'].value_counts()
Fusion_1_Pred = Fusion_1_Pred[(Fusion_1_Pred['DENS'] != 'nan')]
Fusion_1_Pred['DENS'].value_counts()
Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['DENS'])
Comm_1_Pred = Comm_1_Pred.drop('1', axis=1)

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
np.max(Fusion_1_Pred['Predicted_price'])
np.min(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>100)]
Fusion_1_Pred = Fusion_1_Pred.drop('Dep', axis=1)
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_predict_R_44.csv', sep=',', encoding='utf-8')

#%% Pays de la Loire
Fusion = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/52_Fusion.csv",sep = ",")
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
Fusion = Fusion[Fusion['DENS'].notna()]
#%% PROBLEMES DE NA
y = Fusion['valeurfonc']/Fusion['ffshab']
Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Fusion['DENS'] = Fusion['DENS'].astype(str)
Fusion['DENS'] = Fusion['DENS'].str.replace('.0','')
Fusion['DENS'].value_counts()
Fusion = Fusion[(Fusion['DENS'] != 'nan')]
Comm_1 = pd.get_dummies(Fusion['DENS'])
Comm_1.columns = Comm_1.columns.astype(str)
list(Comm_1.columns)
Comm_1 = Comm_1.drop('1', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('244900015', axis=1)

Maison = pd.get_dummies(Fusion['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion['ffshab']*Fusion['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion['ffsdep']

Garage = pd.cut(Fusion['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm], axis = 1)
X = X.dropna()
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
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_train, OLS.predict(X_train))),2)
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
#%%
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
model = HistGradientBoostingRegressor(max_leaf_nodes= 50, 
                                      max_depth= 4, 
                                      max_bins= 30, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.7, 
                                      l2_regularization= 0.65)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_train, model.predict(X_train))),2)
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
                     max_depth= 7,
                     reg_lambda= 0.4, 
                     gamma= 3, 
                     eta= 0.35, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(mean_squared_error(y_test, model.predict(X_test), squared=False),2)
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
model.fit(X, y)
#%% Prédiction
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R52.csv",sep = ",")
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred['DENS'].value_counts()

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
list(Fusion_pred.columns)
Fusion_pred['EPCI'].value_counts()
Fusion_pred.drop(['ccodep', 'nbpiscine', 'nbannexe',
                      'loghlls'], axis=1, inplace=True)
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)]
Fusion_1_Pred = Fusion_1_Pred[Fusion_1_Pred['DENS'].notna()]
#
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Fusion_1_Pred['EPCI'].value_counts()
Comm_Pred = Comm_Pred.drop('244900015', axis=1)

Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].astype(str)
Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].str.replace('.0','')
Fusion_1_Pred['DENS'].value_counts()
Fusion_1_Pred = Fusion_1_Pred[(Fusion_1_Pred['DENS'] != 'nan')]
Fusion_1_Pred['DENS'].value_counts()
Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['DENS'])
Comm_1_Pred = Comm_1_Pred.drop('1', axis=1)

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
np.max(Fusion_1_Pred['Predicted_price'])
np.min(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>100)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_predict_R_52.csv', sep=',', encoding='utf-8')

#%% Bretagne
Fusion = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/53_Fusion.csv",sep = ",")
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
Fusion = Fusion[Fusion['DENS'].notna()]
#%% PROBLEMES DE NA
y = Fusion['valeurfonc']/Fusion['ffshab']
Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Fusion['DENS'] = Fusion['DENS'].astype(str)
Fusion['DENS'] = Fusion['DENS'].str.replace('.0','')
Fusion['DENS'].value_counts()
Fusion = Fusion[(Fusion['DENS'] != 'nan')]
Comm_1 = pd.get_dummies(Fusion['DENS'])
Comm_1.columns = Comm_1.columns.astype(str)
list(Comm_1.columns)
Comm_1 = Comm_1.drop('1', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('243500139', axis=1)

Maison = pd.get_dummies(Fusion['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion['ffshab']*Fusion['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion['ffsdep']

Garage = pd.cut(Fusion['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm], axis = 1)
X = X.dropna()
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
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_train, OLS.predict(X_train))),2)
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
#%%
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
model = HistGradientBoostingRegressor(max_leaf_nodes= 30, 
                                      max_depth= 4, 
                                      max_bins= 50, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.6, 
                                      l2_regularization= 0.35)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_train, model.predict(X_train))),2)
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
model = XGBRegressor(min_child_weight= 1, 
                     max_depth= 4,
                     reg_lambda= 0.45, 
                     gamma= 0.2, 
                     eta= 0.5, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(mean_squared_error(y_test, model.predict(X_test), squared=False),2)
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
model.fit(X, y)
#%% Prédiction
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R53.csv",sep = ",")
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred['DENS'].value_counts()

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
list(Fusion_pred.columns)
Fusion_pred['EPCI'].value_counts()
Fusion_pred.drop(['ccodep', 'nbpiscine', 'nbannexe',
                      'loghlls'], axis=1, inplace=True)
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)]
Fusion_1_Pred = Fusion_1_Pred[Fusion_1_Pred['DENS'].notna()]
#
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Fusion_1_Pred['EPCI'].value_counts()
Comm_Pred = Comm_Pred.drop('243500139', axis=1)

Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].astype(str)
Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].str.replace('.0','')
Fusion_1_Pred['DENS'].value_counts()
Fusion_1_Pred = Fusion_1_Pred[(Fusion_1_Pred['DENS'] != 'nan')]
Fusion_1_Pred['DENS'].value_counts()
Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['DENS'])
Comm_1_Pred = Comm_1_Pred.drop('1', axis=1)

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
np.max(Fusion_1_Pred['Predicted_price'])
np.min(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>100)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_predict_R_53.csv', sep=',', encoding='utf-8')

#%% Nouvelle Aquitaine
Fusion = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/75_Fusion.csv",sep = ",")
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
Fusion = Fusion[Fusion['DENS'].notna()]
#%% PROBLEMES DE NA
y = Fusion['valeurfonc']/Fusion['ffshab']
Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Fusion['DENS'] = Fusion['DENS'].astype(str)
Fusion['DENS'] = Fusion['DENS'].str.replace('.0','')
Fusion['DENS'].value_counts()
Fusion = Fusion[(Fusion['DENS'] != 'nan')]
Comm_1 = pd.get_dummies(Fusion['DENS'])
Comm_1.columns = Comm_1.columns.astype(str)
list(Comm_1.columns)
Comm_1 = Comm_1.drop('1', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('243300316', axis=1)

Maison = pd.get_dummies(Fusion['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion['ffshab']*Fusion['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion['ffsdep']

Garage = pd.cut(Fusion['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm], axis = 1)
X = X.dropna()
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
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_train, OLS.predict(X_train))),2)
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
#%%
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
model = HistGradientBoostingRegressor(max_leaf_nodes= 50, 
                                      max_depth= 4, 
                                      max_bins= 40, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.5, 
                                      l2_regularization= 0.0)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_train, model.predict(X_train))),2)
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
model = XGBRegressor(min_child_weight= 1, 
                     max_depth= 7,
                     reg_lambda= 0.35, 
                     gamma= 2.4, 
                     eta= 0.25, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(mean_squared_error(y_test, model.predict(X_test), squared=False),2)
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
model.fit(X, y)
#%% Prédiction
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R75.csv",sep = ",")
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred['DENS'].value_counts()

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
list(Fusion_pred.columns)
Fusion_pred['EPCI'].value_counts()
Fusion_pred.drop(['ccodep', 'nbpiscine', 'nbannexe',
                      'loghlls'], axis=1, inplace=True)

Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)]
Fusion_1_Pred = Fusion_1_Pred[Fusion_1_Pred['DENS'].notna()]
#
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Fusion_1_Pred['EPCI'].value_counts()
Comm_Pred = Comm_Pred.drop('243300316', axis=1)

Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].astype(str)
Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].str.replace('.0','')
Fusion_1_Pred['DENS'].value_counts()
Fusion_1_Pred = Fusion_1_Pred[(Fusion_1_Pred['DENS'] != 'nan')]
Fusion_1_Pred['DENS'].value_counts()
Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['DENS'])
Comm_1_Pred = Comm_1_Pred.drop('1', axis=1)

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
np.max(Fusion_1_Pred['Predicted_price'])
np.min(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>100)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_predict_R_75.csv', sep=',', encoding='utf-8')

#%% Occitanie
Fusion = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/76_Fusion.csv",sep = ",")
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
Fusion = Fusion[Fusion['DENS'].notna()]
#%% PROBLEMES DE NA
y = Fusion['valeurfonc']/Fusion['ffshab']
Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Fusion['DENS'] = Fusion['DENS'].astype(str)
Fusion['DENS'] = Fusion['DENS'].str.replace('.0','')
Fusion['DENS'].value_counts()
Fusion = Fusion[(Fusion['DENS'] != 'nan')]
Comm_1 = pd.get_dummies(Fusion['DENS'])
Comm_1.columns = Comm_1.columns.astype(str)
list(Comm_1.columns)
Comm_1 = Comm_1.drop('1', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('243100518', axis=1)

Maison = pd.get_dummies(Fusion['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion['ffshab']*Fusion['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion['ffsdep']

Garage = pd.cut(Fusion['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm], axis = 1)
X = X.dropna()
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
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_train, OLS.predict(X_train))),2)
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
#%%
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
model = HistGradientBoostingRegressor(max_leaf_nodes= 10, 
                                      max_depth= 4, 
                                      max_bins= 30, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.7, 
                                      l2_regularization= 0.15)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_train, model.predict(X_train))),2)
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
                     reg_lambda= 0.7, 
                     gamma= 1.6, 
                     eta= 0.5, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(mean_squared_error(y_test, model.predict(X_test), squared=False),2)
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
model.fit(X, y)
#%% Prédiction
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R76.csv",sep = ",")
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred['DENS'].value_counts()

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
list(Fusion_pred.columns)
Fusion_pred['EPCI'].value_counts()
Fusion_pred.drop(['ccodep', 'nbpiscine', 'nbannexe',
                      'loghlls'], axis=1, inplace=True)
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)]
Fusion_1_Pred = Fusion_1_Pred[Fusion_1_Pred['DENS'].notna()]
#
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Fusion_1_Pred['EPCI'].value_counts()
Comm_Pred = Comm_Pred.drop('243100518', axis=1)

Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].astype(str)
Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].str.replace('.0','')
Fusion_1_Pred['DENS'].value_counts()
Fusion_1_Pred = Fusion_1_Pred[(Fusion_1_Pred['DENS'] != 'nan')]
Fusion_1_Pred['DENS'].value_counts()
Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['DENS'])
Comm_1_Pred = Comm_1_Pred.drop('1', axis=1)

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
np.max(Fusion_1_Pred['Predicted_price'])
np.min(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>100)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_predict_R_76.csv', sep=',', encoding='utf-8')

#%% Auvergne Rhône Alpes
Fusion = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/84_Fusion.csv",sep = ",")
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
#Fusion = Fusion[(Fusion['ffctyploc'] == 1)]
Fusion = Fusion[(Fusion['datemut'] >= '2022-01-01') & (Fusion['datemut'] < '2023-01-01')]
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
list(Fusion.columns)
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
Fusion = Fusion[Fusion['DENS'].notna()]
Fusion['EPCI'] = Fusion['EPCI'].replace('200000172', '200067437').replace('200071033', '200067437')

#%% PROBLEMES DE NA
y = Fusion['valeurfonc']/Fusion['ffshab']
Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Fusion['DENS'] = Fusion['DENS'].astype(str)
Fusion['DENS'] = Fusion['DENS'].str.replace('.0','')
Fusion['DENS'].value_counts()
Fusion = Fusion[(Fusion['DENS'] != 'nan')]
Comm_1 = pd.get_dummies(Fusion['DENS'])
Comm_1.columns = Comm_1.columns.astype(str)
list(Comm_1.columns)
Comm_1 = Comm_1.drop('1', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('200046977', axis=1)

Maison = pd.get_dummies(Fusion['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion['ffshab']*Fusion['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion['ffsdep']

Garage = pd.cut(Fusion['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm], axis = 1)
X = X.dropna()
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
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_train, OLS.predict(X_train))),2)
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
#%%
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
model = HistGradientBoostingRegressor(max_leaf_nodes= 20, 
                                      max_depth= 3, 
                                      max_bins= 30, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.7, 
                                      l2_regularization= 0.4)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_train, model.predict(X_train))),2)
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
                     max_depth= 9,
                     reg_lambda= 0.5, 
                     gamma= 0.8, 
                     eta= 0.25, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(mean_squared_error(y_test, model.predict(X_test), squared=False),2)
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
model.fit(X, y)
#%% Prédiction
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R84.csv",sep = ",")
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred['DENS'].value_counts()

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
list(Fusion_pred.columns)
Fusion_pred['EPCI'].value_counts()
Fusion_pred.drop(['ccodep', 'nbpiscine', 'nbannexe',
                      'loghlls'], axis=1, inplace=True)
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)]
Fusion_1_Pred = Fusion_1_Pred[Fusion_1_Pred['DENS'].notna()]
Fusion_1_Pred['EPCI'] = Fusion_1_Pred['EPCI'].replace('200000172', '200067437').replace('200071033', '200067437')
#
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Fusion_1_Pred['EPCI'].value_counts()
Comm_Pred = Comm_Pred.drop('200046977', axis=1)

Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].astype(str)
Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].str.replace('.0','')
Fusion_1_Pred['DENS'].value_counts()
Fusion_1_Pred = Fusion_1_Pred[(Fusion_1_Pred['DENS'] != 'nan')]
Fusion_1_Pred['DENS'].value_counts()
Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['DENS'])
Comm_1_Pred = Comm_1_Pred.drop('1', axis=1)

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
np.max(Fusion_1_Pred['Predicted_price'])
np.min(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>100)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_predict_R_84.csv', sep=',', encoding='utf-8')

#%% PACA
Fusion = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/93_Fusion.csv",sep = ",")
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
#Fusion = Fusion[(Fusion['ffctyploc'] == 1)]
Fusion = Fusion[(Fusion['datemut'] >= '2022-01-01') & (Fusion['datemut'] < '2023-01-01')]
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
list(Fusion.columns)
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
Fusion = Fusion[Fusion['DENS'].notna()]
#%% PROBLEMES DE NA
y = Fusion['valeurfonc']/Fusion['ffshab']
Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Fusion['DENS'] = Fusion['DENS'].astype(str)
Fusion['DENS'] = Fusion['DENS'].str.replace('.0','')
Fusion['DENS'].value_counts()
Fusion = Fusion[(Fusion['DENS'] != 'nan')]
Comm_1 = pd.get_dummies(Fusion['DENS'])
Comm_1.columns = Comm_1.columns.astype(str)
list(Comm_1.columns)
Comm_1 = Comm_1.drop('1', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('200054807', axis=1)

Maison = pd.get_dummies(Fusion['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion['ffshab']*Fusion['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion['ffsdep']

Garage = pd.cut(Fusion['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm, Comm_1], axis = 1)
X = X.dropna()
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
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_train, OLS.predict(X_train))),2)
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
#%%
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
model = HistGradientBoostingRegressor(max_leaf_nodes= 40, 
                                      max_depth= 2, 
                                      max_bins= 50, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.5, 
                                      l2_regularization= 0.7)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_train, model.predict(X_train))),2)
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
                     reg_lambda= 0.0, 
                     gamma= 2.0, 
                     eta= 0.1, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(mean_squared_error(y_test, model.predict(X_test), squared=False),2)
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
model.fit(X, y)
#%% Prédiction
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R93.csv",sep = ",")
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred['DENS'].value_counts()

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
list(Fusion_pred.columns)
Fusion_pred['EPCI'].value_counts()
Fusion_pred.drop(['ccodep', 'nbpiscine', 'nbannexe',
                      'loghlls'], axis=1, inplace=True)
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)]
Fusion_1_Pred = Fusion_1_Pred[Fusion_1_Pred['DENS'].notna()]
#
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Fusion_1_Pred['EPCI'].value_counts()
Comm_Pred = Comm_Pred.drop('200054807', axis=1)

Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].astype(str)
Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].str.replace('.0','')
Fusion_1_Pred['DENS'].value_counts()
Fusion_1_Pred = Fusion_1_Pred[(Fusion_1_Pred['DENS'] != 'nan')]
Fusion_1_Pred['DENS'].value_counts()
Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['DENS'])
Comm_1_Pred = Comm_1_Pred.drop('1', axis=1)

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
               Surf_dep_Pred, Garage_Pred, Maison_Pred, Comm_Pred,
               Comm_1_Pred], axis = 1)
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
np.min(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>100)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_predict_R_93.csv', sep=',', encoding='utf-8')

#%% Corse
Fusion = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/94_Fusion.csv",sep = ",")
Fusion = Fusion[(Fusion['fflogsoc'] == False)]
#Fusion = Fusion[(Fusion['ffctyploc'] == 1)]
Fusion = Fusion[(Fusion['datemut'] >= '2022-01-01') & (Fusion['datemut'] < '2023-01-01')]
Fusion['ffcodinsee'] = Fusion['ffcodinsee'].apply(lambda x: '{0:0>5}'.format(x))
list(Fusion.columns)
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
Fusion = Fusion[Fusion['DENS'].notna()]
#%% PROBLEMES DE NA
y = Fusion['valeurfonc']/Fusion['ffshab']
Floor = pd.cut(Fusion['ffetage'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor = pd.get_dummies(Floor)
Floor = Floor.drop('1-3', axis=1)

Const_Year = pd.cut(Fusion['ffancst'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year = pd.get_dummies(Const_Year)
Const_Year = Const_Year.drop('Avant 1949', axis=1)

Room_count = pd.cut(Fusion['ffnbpprinc'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count = pd.get_dummies(Room_count)
Room_count = Room_count.drop('2P', axis=1)

Fusion['DENS'] = Fusion['DENS'].astype(str)
Fusion['DENS'] = Fusion['DENS'].str.replace('.0','')
Fusion['DENS'].value_counts()
Fusion = Fusion[(Fusion['DENS'] != 'nan')]
Comm_1 = pd.get_dummies(Fusion['DENS'])
Comm_1.columns = Comm_1.columns.astype(str)
list(Comm_1.columns)
Comm_1 = Comm_1.drop('2', axis=1)

Comm = pd.get_dummies(Fusion['EPCI'])
Fusion['EPCI'].value_counts()
Comm = Comm.drop('242000354', axis=1)

Maison = pd.get_dummies(Fusion['ffctyploc'])
Maison.columns = Maison.columns.astype(str)
Maison = Maison.drop('2', axis=1)

Surface = pd.DataFrame(Fusion['ffshab'])
Surface = Surface.rename(columns={'ffshab': 'Surface'})

Surface_sq = pd.DataFrame(Fusion['ffshab']*Fusion['ffshab'])
Surface_sq = Surface_sq.rename(columns={'ffshab': 'Surface_sq'})

Surf_dep = Fusion['ffsdep']

Garage = pd.cut(Fusion['ffnbpgarag'], bins=[-1,0,20], labels=['0', '1'])
Garage = pd.get_dummies(Garage)
Garage = Garage.drop('0', axis=1)
Garage = Garage.rename(columns={'1': 'Garage'})

Terrasse = pd.cut(Fusion['ffnbpterra'], bins=[-1,0,20], labels=['0', '1'])
Terrasse = pd.get_dummies(Terrasse)
Terrasse = Terrasse.drop('0', axis=1)
Terrasse = Terrasse.rename(columns={'1': 'Terrasse'})

X = pd.concat([Floor, Terrasse, Const_Year, Room_count, Surface,Surface_sq,
               Surf_dep, Garage, Maison, Comm, Comm_1], axis = 1)
X = X.dropna()
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
from sklearn.metrics import mean_squared_error
round(np.sqrt(mean_squared_error(y_train, OLS.predict(X_train))),2)
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
#%%
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
model = HistGradientBoostingRegressor(max_leaf_nodes= 50, 
                                      max_depth= 3, 
                                      max_bins= 40, 
                                      loss= 'squared_error', 
                                      learning_rate= 0.2, 
                                      l2_regularization= 0.1)
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(np.sqrt(mean_squared_error(y_train, model.predict(X_train))),2)
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
                     max_depth= 7,
                     reg_lambda= 0.0, 
                     gamma= 1.0, 
                     eta= 0.45, 
                     booster= 'gbtree')
# fit model
model.fit(X_train, y_train)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.25)*100,2)
round(np.median(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(mean(abs((y_test-model.predict(X_test))/y_test))*100,2)
round(np.quantile(abs((y_test-model.predict(X_test))/y_test),0.75)*100,2)
round(mean_squared_error(y_test, model.predict(X_test), squared=False),2)
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
model.fit(X, y)
#%% Prédiction
Fusion_pred = pd.read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R94.csv",sep = ",")
Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx')
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred['DENS'].value_counts()

Aires_urbaines = pd.read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Corr_code_insee_EPCI.xlsx')
Aires_urbaines = Aires_urbaines.rename(columns={'ffcodinsee': 'idcom'})
Fusion_pred['idcom'] = Fusion_pred['idcom'].apply(lambda x: '{0:0>5}'.format(x))
Fusion_pred = pd.merge(Fusion_pred, Aires_urbaines, how="left", on=['idcom'])
Fusion_pred = Fusion_pred[(Fusion_pred['loghlls'] != 'OUI') & (Fusion_pred['loghlls'] != 'OUI PROBABLE')]
list(Fusion_pred.columns)
Fusion_pred['EPCI'].value_counts()
Fusion_pred.drop(['ccodep', 'nbpiscine', 'nbannexe',
                      'loghlls'], axis=1, inplace=True)
#Fusion_pred_1.shape[0]/Fusion_pred.shape[0]
#Fusion_pred.shape[0]-Fusion_pred_1.shape[0]
#Pas parfait, il manque 2 millions de logements sociaux non répertoriés...
Fusion_1_Pred = Fusion_pred[(Fusion_pred['stoth'] >= 9)]
Fusion_1_Pred = Fusion_1_Pred[Fusion_1_Pred['DENS'].notna()]
#
Floor_Pred = pd.cut(Fusion_1_Pred['dniv'], bins=[-1,0,3,7,99], labels=['RDC', '1-3', '4-6','7+'])
Floor_Pred = pd.get_dummies(Floor_Pred)
Floor_Pred = Floor_Pred.drop('1-3', axis=1)

Const_Year_Pred = pd.cut(Fusion_1_Pred['jannath'], bins=[0,1948,1975,1983,1991,2000,10000], labels=['Avant 1949', '1949-1974', '1975-1981','1982-1989','1990-1998','Après 1999'])
Const_Year_Pred = pd.get_dummies(Const_Year_Pred)
Const_Year_Pred = Const_Year_Pred.drop('Avant 1949', axis=1)

Room_count_Pred = pd.cut(Fusion_1_Pred['npiece_ff'], bins=[0,1,2,3,1991], labels=['1P', '2P', '3P','4P+'])
Room_count_Pred = pd.get_dummies(Room_count_Pred)
Room_count_Pred = Room_count_Pred.drop('2P', axis=1)

Comm_Pred = pd.get_dummies(Fusion_1_Pred['EPCI'])
Fusion_1_Pred['EPCI'].value_counts()
Comm_Pred = Comm_Pred.drop('242000354', axis=1)

Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].astype(str)
Fusion_1_Pred['DENS'] = Fusion_1_Pred['DENS'].str.replace('.0','')
Fusion_1_Pred['DENS'].value_counts()
Fusion_1_Pred = Fusion_1_Pred[(Fusion_1_Pred['DENS'] != 'nan')]
Fusion_1_Pred['DENS'].value_counts()
Comm_1_Pred = pd.get_dummies(Fusion_1_Pred['DENS'])
Comm_1_Pred = Comm_1_Pred.drop('2', axis=1)

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
               Surf_dep_Pred, Garage_Pred, Maison_Pred, Comm_Pred,
               Comm_1_Pred], axis = 1)
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
np.min(Fusion_1_Pred['Predicted_price'])
Fusion_1_Pred_1 = Fusion_1_Pred[(Fusion_1_Pred['Predicted_price']>100)]
Fusion_1_Pred_1.to_csv(r'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_predict_R_94.csv', sep=',', encoding='utf-8')
