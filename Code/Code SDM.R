rm(list=ls())
library(lmtest)
library(sandwich)
library(dplyr)
library(spdep)
library(sp)
####Communes####
BDD_GWR_Diff <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Var_OLDDEP_Communes_Par_Commune.xlsx")
Insee_Indicateurs_Diff <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Insee_Diff_Variations.xlsx")
Valo_Communes <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_Commune_2022.xlsx")

colnames(Insee_Indicateurs_Diff)
BDD_GWR_Diff = BDD_GWR_Diff %>%
  left_join(Insee_Indicateurs_Diff, by = "idcom") %>%
  left_join(Valo_Communes, by = "idcom")

BDD_GWR_Diff$Dep = substr(BDD_GWR_Diff$idcom, start = 1, stop = 2)
BDD_GWR_Diff$Dep = factor(BDD_GWR_Diff$Dep)
colnames(BDD_GWR_Diff)


OLS = lm(Diff~Var_Part_Propr+TN+TM+
           Var_Part_Res_Princ+Var_Taux_Act+
           Var_Valo+`Var_Part_65+`+
           relevel(Dep, ref = "69"),
         data = BDD_GWR_Diff)
summary(OLS)
coeftest(OLS, vcov = vcovHC, type = "HC0")
modelsummary::modelsummary(coeftest(OLS, vcov = vcovHC, type = "HC0"))
cor.test(BDD_GWR_Diff$`Var_Part_65+`, BDD_GWR_Diff$Diff)

library(spdep)
Comm_SHP = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/DSN/Communes France + ROM',
                       layer = 'COMMUNE')
Comm_SHP <- sf::st_transform(Comm_SHP, crs = 4326)
Comm_SHP = Comm_SHP %>%
  rename(idcom = `INSEE_COM`)
Comm_SHP = Comm_SHP %>%
  left_join(BDD_GWR_Diff, by = "idcom")

Comm_SHP_patial <- as(Comm_SHP, "Spatial")
library(spdep)
library(sp)

#
addnbs <- function(sp.sample){
  
  queen_nb <- poly2nb(Comm_SHP_patial, row.names=Comm_SHP_patial$idcom, queen=TRUE)
  
  count = card(queen_nb)
  if(!any(count==0)){
    return(queen_nb)
  }
  
  ## get nearest neighbour index, use centroids:
  nnbs = knearneigh(coordinates(Comm_SHP_patial))$nn
  
  no_edges_from = which(count==0)
  for(i in no_edges_from){
    queen_nb[[i]] = nnbs[i]
  }
  return(queen_nb)
}
nb2 = addnbs(Comm_SHP_patial)

nb = poly2nb(Comm_SHP_patial, queen=T, row.names = Comm_SHP_patial$idcom)
isolated <- which(card(nb) <= 1)
data_cleaned <- Comm_SHP_patial[-isolated, ]
nb_cleaned <- subset(nb, card(nb) > 1)
W <- nb2listw(nb_cleaned, style = "W")
summary(unlist(W$weights))

library(spatialreg)
OLS = lm(Diff~Var_Part_Propr+TN+TM+
           Var_Part_Res_Princ+Var_Taux_Act+
           Var_Valo+Var_Part_65.+
           relevel(Dep, ref = "69"),data = data_cleaned)
spdep::lm.LMtests(OLS,W,test="RLMerr")
spdep::lm.LMtests(OLS,W,test="RLMlag")


SDM = lagsarlm(Diff~Var_Part_Propr+TN+TM+
                 Var_Part_Res_Princ+Var_Taux_Act+
                 Var_Valo+Var_Part_65.,
               listw=W,data=data_cleaned,
               type = "mixed",
               method="MC",zero.policy = T)
summary(SDM)
impacts(SDM, listw = W, R = 100, zero.policy = T)

SAR = lagsarlm(Diff~Var_Part_Propr+TN+TM+
                 Var_Part_Res_Princ+Var_Taux_Act+
                 Var_Valo+Var_Part_65.,
               listw=W,data=data_cleaned,
               method="MC",zero.policy = T)
summary(SAR)
impacts(SAR, listw = W, R = 100)

lrtest(SAR, SDM)

####EPCI####
BDD_GWR_Diff <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Var_OLDDEP_EPCI_Par_EPCI.xlsx")
Insee_Indicateurs_Diff <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Insee_Diff_Variations - EPCI.xlsx")
Valo_EPCI <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_EPCI_Physique_2022.xlsx")

colnames(Insee_Indicateurs_Diff)
BDD_GWR_Diff = BDD_GWR_Diff %>%
  left_join(Insee_Indicateurs_Diff, by = "EPCI") %>%
  left_join(Valo_EPCI, by = "EPCI")

library(lmtest)
library(sandwich)

colnames(BDD_GWR_Diff)

OLS = lm(Diff~Var_Part_Res_Princ+TN+TM+
           Var_Part_Prop+Var_Taux_Act+
           Var_Part_65,
         data = BDD_GWR_Diff)
summary(OLS)
coeftest(OLS, vcov = vcovHC, type = "HC0")

Comm_SHP = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/DSN/EPCI',
                       layer = 'EPCI')
Comm_SHP <- sf::st_transform(Comm_SHP, crs = 4326)
Comm_SHP = Comm_SHP %>%
  rename(EPCI = `CODE_SIREN`)
Comm_SHP = Comm_SHP %>%
  left_join(BDD_GWR_Diff, by = "EPCI")
Comm_SHP_Spatial <- as(Comm_SHP, "Spatial")

library(spdep)
library(sp)
nb = poly2nb(Comm_SHP_Spatial, queen=T)
W <- nb2listw(nb, style = "W", zero.policy = T)
SDM = lagsarlm(Diff~Var_Part_Res_Princ+TN+TM+
                 Var_Part_Prop+Var_Taux_Act+
                 Var_Part_65,
               listw=W,data=Comm_SHP_Spatial,
               type = "mixed",
               method="MC",zero.policy = T)
summary(SDM)
