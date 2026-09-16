####Modélisation EPCI####
rm(list=ls())
library(dplyr)
BDD_GWR_Diff_1 <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/BDD_Fusion_2012_EPCI.xlsx")
BDD_GWR_Diff_2 <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/BDD_Fusion_2022_EPCI.xlsx")
INSEE <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/INSEE_DATA_V2.xlsx")
HLM <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/HLM_INSEE.xlsx")
APL <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Evol_Med.xlsx")
DEP <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Correspondance EPCI_DEP.xlsx")
Type_EPCI <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Type_EPCI_2022.xlsx")
Multi_EPCI <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Multi_2022_EPCI.xlsx")

####Fusion####
BDD_GWR_Diff = BDD_GWR_Diff_1 %>%
  left_join(BDD_GWR_Diff_2, by = "EPCI_2022") %>%
  left_join(INSEE, by = "EPCI_2022") %>%
  left_join(HLM, by = "EPCI_2022") %>%
  left_join(DEP, by = "EPCI_2022") %>%
  left_join(Type_EPCI, by = "EPCI_2022") %>%
  left_join(Multi_EPCI, by = "EPCI_2022") %>%
  filter(!EPCI_2022==245900428)
colnames(BDD_GWR_Diff)
BDD_GWR_Diff$NATURE_EPCI = as.factor(BDD_GWR_Diff$NATURE_EPCI)

BDD_GWR_Diff = BDD_GWR_Diff %>%
  left_join(APL, by = "DEP")


####Pre-processing####
#####Calcul des différences premières#####
BDD_GWR_Diff$Diff_18 = log(BDD_GWR_Diff$Patrimoine_18_2022/BDD_GWR_Diff$Patrimoine_2022)-log(BDD_GWR_Diff$Patrimoine_18_2012/BDD_GWR_Diff$Patrimoine_2012)
BDD_GWR_Diff$Diff_31 = log(BDD_GWR_Diff$Patrimoine_31_2022/BDD_GWR_Diff$Patrimoine_2022)-log(BDD_GWR_Diff$Patrimoine_31_2012/BDD_GWR_Diff$Patrimoine_2012)
BDD_GWR_Diff$Diff_41 = log(BDD_GWR_Diff$Patrimoine_41_2022/BDD_GWR_Diff$Patrimoine_2022)-log(BDD_GWR_Diff$Patrimoine_41_2012/BDD_GWR_Diff$Patrimoine_2012)
BDD_GWR_Diff$Diff_51 = log(BDD_GWR_Diff$Patrimoine_51_2022/BDD_GWR_Diff$Patrimoine_2022)-log(BDD_GWR_Diff$Patrimoine_51_2012/BDD_GWR_Diff$Patrimoine_2012)
BDD_GWR_Diff$Diff_64 = log(BDD_GWR_Diff$Patrimoine_64_2022/BDD_GWR_Diff$Patrimoine_2022)-log(BDD_GWR_Diff$Patrimoine_64_2012/BDD_GWR_Diff$Patrimoine_2012)
BDD_GWR_Diff$Diff_Valo = log(BDD_GWR_Diff$Patrimoine_2022)-log(BDD_GWR_Diff$Patrimoine_2012)

BDD_GWR_Diff$Var_Part_Prop_64 = log(BDD_GWR_Diff$Sum_Pers_64_2022)-log(BDD_GWR_Diff$Patrimoine_64_2012)

BDD_GWR_Diff$Diff_coh_31 = log(BDD_GWR_Diff$Patrimoine_31_2022/BDD_GWR_Diff$Patrimoine_2022)-log(BDD_GWR_Diff$Patrimoine_18_2012/BDD_GWR_Diff$Patrimoine_2012)
BDD_GWR_Diff$Diff_coh_41 = log(BDD_GWR_Diff$Patrimoine_41_2022/BDD_GWR_Diff$Patrimoine_2022)-log(BDD_GWR_Diff$Patrimoine_31_2012/BDD_GWR_Diff$Patrimoine_2012)
BDD_GWR_Diff$Diff_coh_51 = log(BDD_GWR_Diff$Patrimoine_51_2022/BDD_GWR_Diff$Patrimoine_2022)-log(BDD_GWR_Diff$Patrimoine_41_2012/BDD_GWR_Diff$Patrimoine_2012)
BDD_GWR_Diff$Diff_coh_64 = log(BDD_GWR_Diff$Patrimoine_64_2022/BDD_GWR_Diff$Patrimoine_2022)-log(BDD_GWR_Diff$Patrimoine_51_2012/BDD_GWR_Diff$Patrimoine_2012)

BDD_GWR_Diff$Diff_Surplus_31 = BDD_GWR_Diff$Diff_coh_31-log(BDD_GWR_Diff$Sum_Pers_31_2012-BDD_GWR_Diff$Sum_Pers_18_2012)
BDD_GWR_Diff$Diff_Surplus_41 = BDD_GWR_Diff$Diff_coh_41-log(BDD_GWR_Diff$Sum_Pers_41_2012-BDD_GWR_Diff$Sum_Pers_31_2012)
BDD_GWR_Diff$Diff_Surplus_51 = BDD_GWR_Diff$Diff_coh_51-log(BDD_GWR_Diff$Sum_Pers_51_2012-BDD_GWR_Diff$Sum_Pers_41_2012)

#### Modélisation  ####
#####Patrimoine global en Y#####
OLS_1 = lm(Diff_18~-1+Var_Res_Sec+
             TN+TM+Diff_Valo+
             Diff_Med_Effectif+Diff_64,
           data=BDD_GWR_Diff)
summary(OLS_1)

OLS_2 = lm(Diff_31~-1+Var_Res_Sec+
             TN+TM+Diff_Valo+
             Diff_Med_Effectif+Diff_64,
           data=BDD_GWR_Diff)
summary(OLS_2)

OLS_3 = lm(Diff_41~Var_Res_Sec+
             TN+TM+Diff_Valo+
             Diff_Med_Effectif+Diff_64,
           data=BDD_GWR_Diff)
summary(OLS_3)

OLS_4 = lm(Diff_51~-1+Var_Res_Sec+
             TN+TM+Diff_Valo+
             Diff_Med_Effectif+Diff_64,
           data=BDD_GWR_Diff)
summary(OLS_4)

#Juste pour tester, ne sera plus dans l'article
OLS_5 = lm(Diff_64~-1+Var_Res_Sec+
             TN+TM+Diff_Valo+
             Diff_Med_Effectif+Var_Nb_65,
           data=BDD_GWR_Diff)
summary(OLS_5)

#####Patrimoine en cohorte (à tester avec + de variables)#####
colnames(BDD_GWR_Diff)
OLS_1 = lm(Diff_coh_31~Var_Res_Sec+
             TM+TN+Diff_Valo+Var_Nb_emplois+
             Log_Diff_Med_Effectif+Var_Part_Prop_64+
             DEP,
           data=BDD_GWR_Diff)
summary(OLS_1)
car::vif(OLS_1)

OLS_2 = lm(Diff_coh_41~Var_Res_Sec+
             TM+TN+Diff_Valo+Var_Nb_emplois+
             Log_Diff_Med_Effectif+Var_Part_Prop_64+
             DEP,
           data=BDD_GWR_Diff)
summary(OLS_2)

OLS_3 = lm(Diff_coh_51~Var_Res_Sec+
             TM+TN+Diff_Valo+Var_Nb_emplois+
             Log_Diff_Med_Effectif+Var_Part_Prop_64,
           data=BDD_GWR_Diff)
summary(OLS_3)

OLS_4 = lm(Diff_Surplus_31~Var_Res_Sec+
             TM+TN+Diff_Valo+Var_Nb_emplois+
             Log_Diff_Med_Effectif+Var_Part_Prop_64+
             DEP,
           data=BDD_GWR_Diff)
summary(OLS_4)

OLS_5 = lm(Diff_Surplus_41~Var_Res_Sec+
             TM+TN+Diff_Valo+Var_Nb_emplois+
             Log_Diff_Med_Effectif+Var_Part_Prop_64+
             DEP,
           data=BDD_GWR_Diff)
summary(OLS_5)

OLS_6 = lm(Diff_Surplus_51~Var_Res_Sec+
             TM+TN+Diff_Valo+Var_Nb_emplois+
             Log_Diff_Med_Effectif+Var_Part_Prop_64+
             DEP,
           data=BDD_GWR_Diff)
summary(OLS_6)

library(modelsummary)
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2")
modelsummary(list(
  "Modèle 31" = OLS_1,
  "Modèle 41" = OLS_2,
  "Modèle 51" = OLS_3)
  ,stars = TRUE, output = "OLS_2.xlsx")

####Modèles spatiaux####
####1 modèle par région####
library(sp)
library(spatialreg)
library(spdep)
Comm_SHP = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/DSN/EPCI',
                       layer = 'EPCI')
Comm_SHP <- sf::st_transform(Comm_SHP, crs = 4326)
Comm_SHP = Comm_SHP %>%
  rename(EPCI_2022 = epci_code)
Comm_SHP = Comm_SHP %>%
  right_join(BDD_GWR_Diff, by = "EPCI_2022")
Comm_SHP = Comm_SHP %>%
  filter()

Comm_SHP = Comm_SHP[!is.na(Comm_SHP$TN),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$TM),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$Var_Res_Sec),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$Diff_Valo),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$Var_Nb_emplois),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$Log_Diff_Med_Effectif),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$Var_Part_Prop_64),]

Comm_SHP_patial <- st_as_sf(Comm_SHP)
nb = poly2nb(Comm_SHP_patial, queen=T, row.names = Comm_SHP_patial$EPCI_2022)
Comm_SHP_patial = as.data.frame(Comm_SHP_patial)
rownames(Comm_SHP_patial) = Comm_SHP_patial$EPCI_2022
W <- nb2listw(nb, style = "W",zero.policy = T)
length(W$neighbours)

moran(Comm_SHP_patial$Diff_coh_31, W, length(Comm_SHP_patial),
      Szero(W))
moran(Comm_SHP_patial$Diff_coh_41, W, length(Comm_SHP_patial),
      Szero(W))
moran(Comm_SHP_patial$Diff_coh_51, W, length(Comm_SHP_patial),
      Szero(W))


moran(Comm_SHP_patial$Var_Part_Prop_64, W, length(Comm_SHP_patial),
      Szero(W))
moran(Comm_SHP_patial$TN, W, length(Comm_SHP_patial),
      Szero(W))
moran(Comm_SHP_patial$TM, W, length(Comm_SHP_patial),
      Szero(W))
moran(Comm_SHP_patial$Var_Res_Sec, W, length(Comm_SHP_patial),
      Szero(W))
moran(Comm_SHP_patial$Log_Diff_Med_Effectif, W, length(Comm_SHP_patial),
      Szero(W))
moran(Comm_SHP_patial$Diff_Nb_Multi, W, length(Comm_SHP_patial),
      Szero(W))
moran(Comm_SHP_patial$Var_Nb_emplois, W, length(Comm_SHP_patial),
      Szero(W))
moran(Comm_SHP_patial$Diff_Valo, W, length(Comm_SHP_patial),
      Szero(W))

#Moran locaux
local_moran <- localmoran(
  Comm_SHP_patial$Diff_coh_31,
  W,
  zero.policy = TRUE
)

calc_lisa <- function(sf_obj, variable, listw){
  
  x <- sf_obj[[variable]]
  
  lmoran <- localmoran(
    x,
    listw,
    zero.policy = TRUE
  )
  
  x_std <- scale(x)[,1]
  
  lag_x <- lag.listw(
    listw,
    x_std,
    zero.policy = TRUE
  )
  
  cluster <- rep("Non significatif", length(x))
  
  pval <- lmoran[,5]
  
  sig <- pval < 0.05
  
  cluster[sig & x_std > 0 & lag_x > 0] <- "High-High"
  cluster[sig & x_std < 0 & lag_x < 0] <- "Low-Low"
  cluster[sig & x_std > 0 & lag_x < 0] <- "High-Low"
  cluster[sig & x_std < 0 & lag_x > 0] <- "Low-High"
  
  sf_obj[[paste0(variable,"_I")]] <- lmoran[,1]
  sf_obj[[paste0(variable,"_Z")]] <- lmoran[,4]
  sf_obj[[paste0(variable,"_P")]] <- lmoran[,5]
  sf_obj[[paste0(variable,"_LISA")]] <- cluster
  
  return(sf_obj)
  
}
Comm_SHP_export <- Comm_SHP_patial

vars <- c(
  "Diff_coh_31",
  "Diff_coh_41",
  "Diff_coh_51",
  "Diff_coh_64"
)

for(v in vars){
  
  Comm_SHP_export <- calc_lisa(
    Comm_SHP_export,
    v,
    W
  )
  
}

st_write(
  Comm_SHP_patial,
  "LISAs.gpkg",
  delete_dsn = TRUE
)

SDM_1 = lagsarlm(Diff_coh_31~Var_Res_Sec+
                   TM+TN+Diff_Valo+Var_Nb_emplois+
                   Log_Diff_Med_Effectif+Var_Part_Prop_64,
                 listw=W, data=Comm_SHP_patial, 
                 type = "mixed", method="eigen",
                 zero.policy = T)
lmtest::coeftest(SDM_1)
Impacts_SDM = impacts(SDM_1, listw = W, R = 100)
summary(Impacts_SDM)

SDM_2 = lagsarlm(Diff_coh_41~Var_Res_Sec+
                   TM+TN+Diff_Valo+Var_Nb_emplois+
                   Log_Diff_Med_Effectif+Var_Part_Prop_64,
                 listw=W, data=Comm_SHP_patial, 
                 type = "mixed", method="eigen",
                 zero.policy = T)
lmtest::coeftest(SDM_2)
Impacts_SDM_2 = impacts(SDM_2, listw = W, R = 100)
summary(Impacts_SDM_2)

SDM_3 = lagsarlm(Diff_coh_51~Var_Res_Sec+
                   TM+TN+Diff_Valo+Var_Nb_emplois+
                   Log_Diff_Med_Effectif+Var_Part_Prop_64,
                 listw=W, data=Comm_SHP_patial, 
                 type = "mixed", method="eigen",
                 zero.policy = T)
lmtest::coeftest(SDM_3)
Impacts_SDM_3 = impacts(SDM_3, listw = W, R = 100)
summary(Impacts_SDM_3)

SDM_4 = lagsarlm(Diff_Hab_31~Var_Res_Sec+
                   TM+TN+Diff_Valo+Var_Nb_emplois+
                   Log_Diff_Med_Effectif+Var_Part_Prop_64,
                 listw=W, data=Comm_SHP_patial, 
                 type = "mixed", method="eigen",
                 zero.policy = T)
lmtest::coeftest(SDM_4)
Impacts_SDM_4 = impacts(SDM_4, listw = W, R = 100)
summary(Impacts_SDM_4)

SDM_5 = lagsarlm(Diff_Hab_41~Var_Res_Sec+
                   TM+TN+Diff_Valo+Var_Nb_emplois+
                   Log_Diff_Med_Effectif+Var_Part_Prop_64,
                 listw=W, data=Comm_SHP_patial, 
                 type = "mixed", method="eigen",
                 zero.policy = T)
lmtest::coeftest(SDM_5)
Impacts_SDM_5 = impacts(SDM_5, listw = W, R = 100)
summary(Impacts_SDM_5)

SDM_6 = lagsarlm(Diff_Hab_51~Var_Res_Sec+
                   TM+TN+Diff_Valo+Var_Nb_emplois+
                   Log_Diff_Med_Effectif+Var_Part_Prop_64,
                 listw=W, data=Comm_SHP_patial, 
                 type = "mixed", method="eigen",
                 zero.policy = T)
lmtest::coeftest(SDM_6)
Impacts_SDM_6 = impacts(SDM_6, listw = W, R = 100)
summary(Impacts_SDM_6)

modelsummary(list(
  "Modèle 31" = SDM_1,
  "Modèle 41" = SDM_2,
  "Modèle 51" = SDM_3)
  ,stars = TRUE, output = "SDM.xlsx")


mean(BDD_GWR_Diff$Patrimoine_18_2012/BDD_GWR_Diff$Patrimoine_2012)*100
mean(BDD_GWR_Diff$Patrimoine_31_2012/BDD_GWR_Diff$Patrimoine_2012)*100
mean(BDD_GWR_Diff$Patrimoine_41_2012/BDD_GWR_Diff$Patrimoine_2012)*100
mean(BDD_GWR_Diff$Patrimoine_51_2012/BDD_GWR_Diff$Patrimoine_2012)*100
mean(BDD_GWR_Diff$Patrimoine_64_2012/BDD_GWR_Diff$Patrimoine_2012)*100

mean(BDD_GWR_Diff$Patrimoine_18_2022/BDD_GWR_Diff$Patrimoine_2022)*100
mean(BDD_GWR_Diff$Patrimoine_31_2022/BDD_GWR_Diff$Patrimoine_2022)*100
mean(BDD_GWR_Diff$Patrimoine_41_2022/BDD_GWR_Diff$Patrimoine_2022)*100
mean(BDD_GWR_Diff$Patrimoine_51_2022/BDD_GWR_Diff$Patrimoine_2022)*100
mean(BDD_GWR_Diff$Patrimoine_64_2022/BDD_GWR_Diff$Patrimoine_2022)*100

mean(BDD_GWR_Diff$Sum_Pers_18_2012/BDD_GWR_Diff$Sum_Pers_2012)*100
mean(BDD_GWR_Diff$Sum_Pers_31_2012/BDD_GWR_Diff$Sum_Pers_2012)*100
mean(BDD_GWR_Diff$Sum_Pers_41_2012/BDD_GWR_Diff$Sum_Pers_2012)*100
mean(BDD_GWR_Diff$Sum_Pers_51_2012/BDD_GWR_Diff$Sum_Pers_2012)*100
mean(BDD_GWR_Diff$Sum_Pers_64_2012/BDD_GWR_Diff$Sum_Pers_2012)*100

mean(BDD_GWR_Diff$Sum_Pers_18_2022/BDD_GWR_Diff$Sum_Pers_2022)*100
mean(BDD_GWR_Diff$Sum_Pers_31_2022/BDD_GWR_Diff$Sum_Pers_2022)*100
mean(BDD_GWR_Diff$Sum_Pers_41_2022/BDD_GWR_Diff$Sum_Pers_2022)*100
mean(BDD_GWR_Diff$Sum_Pers_51_2022/BDD_GWR_Diff$Sum_Pers_2022)*100
mean(BDD_GWR_Diff$Sum_Pers_64_2022/BDD_GWR_Diff$Sum_Pers_2022)*100

# Classes d'âge, années et variables
classes <- c("18", "31", "41", "51", "64")
annees <- c("2012", "2022")
variables <- c("Patrimoine", "Sum_Pers")

# Création du tableau des résultats
Moyennes <- expand.grid(
  Variable = variables,
  Annee = annees,
  Classe = classes,
  stringsAsFactors = FALSE
)

# Calcul des moyennes
Moyennes$Moyenne <- mapply(function(var, annee, classe) {
  
  num <- BDD_GWR_Diff[[paste0(var, "_", classe, "_", annee)]]
  den <- BDD_GWR_Diff[[paste0(var, "_", annee)]]
  
  mean(num / den, na.rm = TRUE) * 100
  
},
var = Moyennes$Variable,
annee = Moyennes$Annee,
classe = Moyennes$Classe)

# Affichage
Moyennes