rm(list=ls())
library(dplyr)
library(ggplot2)
####Intégration des données####
R11 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R11_Prix_Proprio.csv")
R24 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R24_Prix_Proprio.csv")
R27 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R27_Prix_Proprio.csv")
R28 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R28_Prix_Proprio.csv")
R32 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R32_Prix_Proprio.csv")
R44 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R44_Prix_Proprio.csv")
R52 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R52_Prix_Proprio.csv")
R53 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R53_Prix_Proprio.csv")
R75 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R75_Prix_Proprio.csv")
R76 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R76_Prix_Proprio.csv")
R84 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R84_Prix_Proprio.csv")
R93 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R93_Prix_Proprio.csv")
R94 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R94_Prix_Proprio.csv")
Paris = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_Paris_Prix_Proprio.csv")
R01 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R01_Prix_Proprio.csv")
R02 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R02_Prix_Proprio.csv")
R04 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R04_Prix_Proprio.csv")
RAM = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_RAM_Prix_Proprio.csv")
RAM$Nb_piece_App_Mais = NA
RAM$Predicted_price_sq_m = log(RAM$Predicted_price_sq_m)
RAM = RAM %>% filter(stoth>0)

Fusion_2022 = rbind(R11, R24, R27, R28, R32, R44, R52, R53, R75, R76,
               R84, R93, R94, Paris, R01, R02, R04, RAM)

rm(R11, R24, R27, R28, R32, R44, R52, R53, R75, R76,
   R84, R93, R94, Paris, R01, R02, R04, RAM)

Fusion_2022$Predicted_price_sq_m_1 = exp(Fusion_2022$Predicted_price_sq_m)
Fusion_2022$Price = Fusion_2022$Predicted_price_sq_m_1*Fusion_2022$stoth
Fusion_2022$NB = 1
Fusion_2022$Dep = substr(Fusion_2022$idcom, start = 1, stop = 2)

Fusion_2022_97 = Fusion_2022 %>% filter(Dep>=97)
Fusion_2022 = Fusion_2022 %>% filter(Dep<97)
Fusion_2022_97$Dep = substr(Fusion_2022_97$idcom, start = 1, stop = 3)
table(Fusion_2022_97$Dep)
Fusion_2022 = rbind(Fusion_2022, Fusion_2022_97)

Fusion_2022 = Fusion_2022 %>%  
  mutate(Type_Proprio = case_when(grepl("F1a",catpro3 ) ~ "Logement social",
                                  grepl("F7b",catpro3 ) ~ "Investisseur privé",
                                  grepl("X1a",catpro3 ) ~ "Personne physique",
                                  TRUE ~catpro3))

Ensemble_Prix = Fusion_2022 %>%
  group_by(Type_Proprio) %>%
  summarise(Valeur_foncière = sum(Price, na.rm = T),
            Nombre_logements = sum(NB))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
writexl::write_xlsx(Ensemble_Prix, "Valo_Type_Proprio_Décomposé_2022.xlsx")

####Age par dep####
Fusion_2022_Sans_Moral = Fusion_2022[!is.na(Fusion_2022$dldnss),]
Fusion_2022_Sans_Moral = Fusion_2022_Sans_Moral %>%
  mutate(Age_connu = case_when(Age >= 0 ~ "Né en France",
                                   TRUE ~ "Né à l'étranger"))
Ensemble_Prix = Fusion_2022_Sans_Moral %>%
  group_by(Dep,Age_connu) %>%
  summarise(Valeur_foncière = sum(Price, na.rm = T),
            Nombre_logements = sum(NB, na.rm = T))

Ensemble_Prix = Fusion_2022 %>%
  group_by(Dep, Age) %>%
  filter(Age>=18, Age<=100)%>%
  summarise(Valeur_foncière = sum(Price, na.rm = T),
            Nombre_logements = sum(NB, na.rm = T))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
writexl::write_xlsx(Ensemble_Prix, "Valo_Lieu_Naissance.xlsx")

####Dep####
Ensemble_Prix = Fusion_2022 %>%
  group_by(Dep) %>%
  summarise(Valeur_foncière = sum(Price),
            Nombre_logements = sum(NB))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
writexl::write_xlsx(Ensemble_Prix, "Valo_Départements_2022.xlsx")

####Capital par propriétaire physique####
Fusion_2022_Pysique = Fusion_2022 %>%
  filter(Type_Proprio=="Personne physique",
         Age>=18, Age<=100)

Fusion_2022_Pysique = Fusion_2022_Pysique %>% mutate(Retraité = case_when(Age<65~"Actifs",
                                                     Age>=65~"Retraités"))

Capital_2022 = Fusion_2022_Pysique %>%
  group_by(ID_Unique) %>%
  summarise(Valorisation = sum(Price),
            Nombre_Logements = sum(NB),
            Surface = median(stoth),
            Age = unique(Age),
            Sexe = unique(dqualp))

setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données")
write.csv(Capital_2022, "Valo_Propriétaire.csv",row.names=FALSE)

#Dénominateur France entière
Ensemble_Prix = Fusion_2022_Pysique %>%
  group_by(idcom, Retraité) %>%
  summarise(Valeur_foncière = sum(Price, na.rm = T),
            Nombre_logements = sum(NB))
library(zoo)
Valeurfonc_totale = sum(Ensemble_Prix$Valeur_foncière)
Ensemble_Prix = Ensemble_Prix %>%
  group_by(idcom) %>% 
  mutate(Pct_Retr = (Valeur_foncière[2]/Valeurfonc_totale)*100)
Ensemble_Prix = Ensemble_Prix[!duplicated(Ensemble_Prix$idcom),]

setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
writexl::write_xlsx(Ensemble_Prix, "Valo_Commune_OLDDEP_2022.xlsx")

Correspondance_EPCI = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Intercommunalite_Metropole_au_01-01-2023.xlsx")
Fusion_2022_Pysique = left_join(Fusion_2022_Pysique, Correspondance_EPCI,
                          by = "idcom")

Ensemble_Prix_EPCI = Fusion_2022_Pysique %>%
  group_by(EPCI) %>%
  summarise(Valo = sum(Price))

Ensemble_Prix_EPCI = Ensemble_Prix %>%
  group_by(EPCI) %>%
  summarise(Pct_Retr = sum(Pct_Retr, na.rm = T))
writexl::write_xlsx(Ensemble_Prix_EPCI, "Valo_EPCI_Physique_2022.xlsx")


#Dénominateur échelle locale
Ensemble_Prix = Fusion_2022_Pysique %>%
  group_by(idcom, Retraité) %>%
  summarise(Valeur_foncière = sum(Price, na.rm = T),
            Nombre_logements = sum(NB))
library(zoo)
Valeurfonc_totale = sum(Ensemble_Prix$Valeur_foncière)
Ensemble_Prix = Ensemble_Prix %>%
  group_by(idcom) %>% 
  mutate(Pct_Retr = (Valeur_foncière[2]/(Valeur_foncière[1]+Valeur_foncière[2]))*100)
Ensemble_Prix = Ensemble_Prix[!duplicated(Ensemble_Prix$idcom),]

setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
writexl::write_xlsx(Ensemble_Prix, "Valo_Commune_OLDDEP_2022_Par_commune.xlsx")

Correspondance_EPCI = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Intercommunalite_Metropole_au_01-01-2023.xlsx")
Fusion_2022_Pysique = left_join(Fusion_2022_Pysique, Correspondance_EPCI,
                                by = "idcom")

Ensemble_Prix = Fusion_2022_Pysique %>%
  group_by(EPCI, Retraité) %>%
  summarise(Valeur_foncière = sum(Price, na.rm = T),
            Nombre_logements = sum(NB))
Ensemble_Prix = Ensemble_Prix %>%
  group_by(EPCI) %>% 
  mutate(Pct_Retr = (Valeur_foncière[2]/(Valeur_foncière[1]+Valeur_foncière[2]))*100)
Ensemble_Prix = Ensemble_Prix[!duplicated(Ensemble_Prix$EPCI),]


Ensemble_Prix = Fusion_2022 %>%
  group_by(idcom) %>%
  summarise(Valeur_foncière = sum(Price, na.rm = T),
            Nombre_logements = sum(NB))
writexl::write_xlsx(Ensemble_Prix, "Valo_Commune_2022.xlsx")

######
library(dplyr)
OLDDEP_2012 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_EPCI_OLDDEP_2012.xlsx")
OLDDEP_2022 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_EPCI_OLDDEP_2022.xlsx")
OLDDEP = inner_join(OLDDEP_2012, OLDDEP_2022, by = "idcom")
OLDDEP$Diff = OLDDEP$Pct_Retr-OLDDEP$Pct_Retr_2012*100
writexl::write_xlsx(OLDDEP, "Var_OLDDEP_Commune.xlsx")

####% de multipropriétaires par ville####
DF_Proprio <- Fusion_2022_Pysique %>%
  group_by(ID_Unique) %>%                     # Grouper par l'identifiant du propriétaire
  mutate(Multi = ifelse(n() > 1, 1, 0)) %>% # Identifier si le propriétaire a plusieurs logements
  ungroup()
mean(DF_Proprio$Multi)

#Multipropriétaires par commune
colnames(DF_Proprio)
DF_Proprio_1 = DF_Proprio %>%
  group_by(idcom) %>%
  summarise(Multiprop = sum(Multi),
            Proprio = n())%>%
  ungroup()
DF_Proprio_1$Part_Multi = DF_Proprio_1$Multiprop/DF_Proprio_1$Proprio
writexl::write_xlsx(DF_Proprio_1, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Multi_2022.xlsx")


#######################2012#######################
rm(list=ls())
library(dplyr)
library(ggplot2)
####Intégration des données####
R11 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R11_Prix_Proprio.csv")
R24 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R24_Prix_Proprio.csv")
R27 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R27_Prix_Proprio.csv")
R28 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R28_Prix_Proprio.csv")
R32 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R32_Prix_Proprio.csv")
R44 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R44_Prix_Proprio.csv")
R52 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R52_Prix_Proprio.csv")
R53 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R53_Prix_Proprio.csv")
R75 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R75_Prix_Proprio.csv")
R76 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R76_Prix_Proprio.csv")
R84 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R84_Prix_Proprio.csv")
R93 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R93_Prix_Proprio.csv")
R94 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R94_Prix_Proprio.csv")
Paris = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_Paris_Prix_Proprio.csv")
R01 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R01_Prix_Proprio.csv")
R02 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R02_Prix_Proprio.csv")
R04 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R04_Prix_Proprio.csv")
RAM = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_RAM_Prix_Proprio.csv")
RAM$Nb_piece_App_Mais = NA
RAM = RAM %>% filter(stoth>0)
RAM$Predicted_price_sq_m = log(RAM$Predicted_price_sq_m)
RAM = RAM[!is.na(RAM$Predicted_price_sq_m),]
colnames(Paris)

Fusion_2012 = rbind(R11, R24, R27, R28, R32, R44, R52, R53, R75, R76,
                    R84, R93, R94, Paris, R01, R02, R04, RAM)

rm(R11, R24, R27, R28, R32, R44, R52, R53, R75, R76,
   R84, R93, R94, Paris, R01, R02, R04, RAM)

Fusion_2012$Predicted_price_sq_m_1 = exp(Fusion_2012$Predicted_price_sq_m)
Fusion_2012$Price = Fusion_2012$Predicted_price_sq_m_1*Fusion_2012$stoth
Fusion_2012$NB = 1

####Prix par commune####
#colnames(Fusion_2012)
#Ensemble_Prix = Fusion_2012 %>%
#  group_by(idcom) %>%
#  summarise(Prix_prédits_médians = median(Predicted_price_sq_m_1))
#setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
#writexl::write_xlsx(Ensemble_Prix, "Prix_prédits_ensemble_2012.xlsx")

####Taille du parc social par département####
Fusion_2012 = Fusion_2012 %>%
  mutate(Type_Proprio = case_when(grepl("05",typprop ) ~ "Logement social",
                                  grepl("10",typprop ) ~ "Investisseur privé",
                                  grepl("20",typprop ) ~ "Personne physique",
                                  TRUE ~"Autre"))
Fusion_2012$Dep = substr(Fusion_2012$idcom, start = 1, stop = 2)

Fusion_2012_97 = Fusion_2012 %>% filter(Dep>=97)
Fusion_2012 = Fusion_2012 %>% filter(Dep<97)
Fusion_2012_97$Dep = substr(Fusion_2012_97$idcom, start = 1, stop = 3)
table(Fusion_2012_97$Dep)
Fusion_2012 = rbind(Fusion_2012, Fusion_2012_97)


Ensemble_Prix = Fusion_2012 %>%
  group_by(Dep, Type_Proprio) %>%
  summarise(Valeur_foncière = sum(Price, na.rm = T),
            Nombre_logements = sum(NB))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
writexl::write_xlsx(Ensemble_Prix, "Valo_Départements_Type_Proprio_2012.xlsx")

####Age par dep####
Ensemble_Prix = Fusion_2012 %>%
  group_by(Dep, Age) %>%
  filter(Age>=18, Age<=100)%>%
  summarise(Valeur_foncière = sum(Price, na.rm = T),
            Nombre_logements = sum(NB, na.rm = T))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
writexl::write_xlsx(Ensemble_Prix, "Valo_Départements_Age_2012.xlsx")

####Dep####
Ensemble_Prix = Fusion_2012 %>%
  group_by(Dep) %>%
  summarise(Valeur_foncière = sum(Price),
            Nombre_logements = sum(NB))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
writexl::write_xlsx(Ensemble_Prix, "Valo_Départements_2012.xlsx")

####Capital par propriétaire physique####
Fusion_2012_Pysique = Fusion_2012 %>%
  filter(Type_Proprio=="Personne physique",
         Age>=18, Age<=100)

Capital_2012 = Fusion_2012_Pysique %>%
  group_by(ID_Unique) %>%
  summarise(Valorisation = sum(Price),
            Nombre_Logements = sum(NB),
            Surface = median(stoth),
            Age = unique(Age),
            Sexe = unique(dqualp))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données")
write.csv(Capital_2012, "Valo_Propriétaire_2012.csv",row.names=FALSE)

Fusion_2012_Pysique = Fusion_2012_Pysique %>% mutate(Retraité = case_when(Age<65~"Actifs",
                                                                          Age>=65~"Retraités"))

Correspondance = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Tableau de correspondances 2012_2022.xlsx")
Fusion_2012_Pysique_Corr = left_join(Fusion_2012_Pysique, Correspondance,
                          by = "idcom")

Ensemble_Prix = Fusion_2012_Pysique_Corr %>%
  group_by(idcom_2023, Retraité) %>%
  summarise(Valeur_foncière = sum(Price, na.rm = T),
            Nombre_logements = sum(NB))
library(zoo)
Valeurfonc_totale = sum(Ensemble_Prix$Valeur_foncière)
Ensemble_Prix = Ensemble_Prix %>%
  group_by(idcom_2023) %>% 
  mutate(Pct_Retr = (Valeur_foncière[2]/Valeurfonc_totale)*100)
Ensemble_Prix = Ensemble_Prix[!duplicated(Ensemble_Prix$idcom_2023),]

setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
writexl::write_xlsx(Ensemble_Prix, "Valo_Commune_OLDDEP_2012.xlsx")

Correspondance = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Tableau de correspondances 2012_2022.xlsx")
Ensemble_Prix = left_join(Ensemble_Prix, Correspondance,
                                by = "idcom")
colnames(Ensemble_Prix)
Ensemble_Prix = Ensemble_Prix %>% ungroup %>%
  select(-idcom)
Ensemble_Prix = Ensemble_Prix %>%
  rename(idcom = idcom_2023)

Correspondance_EPCI = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Intercommunalite_Metropole_au_01-01-2023.xlsx")
Ensemble_Prix = left_join(Ensemble_Prix, Correspondance_EPCI,
                                by = "idcom")
Ensemble_Prix_EPCI = Ensemble_Prix %>%
  group_by(EPCI) %>%
  summarise(Pct_Retr = sum(Pct_Retr, na.rm = T))
writexl::write_xlsx(Ensemble_Prix_EPCI, "Valo_EPCI_OLDDEP_2012.xlsx")

Ensemble_Prix = Fusion_2012_Pysique_Corr %>%
  group_by(idcom_2023) %>%
  summarise(Valeur_foncière = sum(Price, na.rm = T),
            Nombre_logements = sum(NB))
writexl::write_xlsx(Ensemble_Prix, "Valo_Commune(2023)_2012.xlsx")

#Dénominateur échelle locale
Correspondance = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Tableau de correspondances 2012_2022.xlsx")
Fusion_2012_Pysique_Corr = left_join(Fusion_2012_Pysique, Correspondance,
                                     by = "idcom")

Ensemble_Prix = Fusion_2012_Pysique_Corr %>%
  group_by(idcom_2023, Retraité) %>%
  summarise(Valeur_foncière = sum(Price, na.rm = T),
            Nombre_logements = sum(NB))
library(zoo)
Valeurfonc_totale = sum(Ensemble_Prix$Valeur_foncière)
Ensemble_Prix = Ensemble_Prix %>%
  group_by(idcom_2023) %>% 
  mutate(Pct_Retr = (Valeur_foncière[2]/(Valeur_foncière[1]+Valeur_foncière[2]))*100)
Ensemble_Prix = Ensemble_Prix[!duplicated(Ensemble_Prix$idcom_2023),]

setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
writexl::write_xlsx(Ensemble_Prix, "Valo_Commune_OLDDEP_2012_Par_commune.xlsx")

Correspondance_EPCI = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Intercommunalite_Metropole_au_01-01-2023.xlsx")
Correspondance_EPCI = Correspondance_EPCI %>%
  rename(idcom_2023 = idcom)
colnames(Correspondance_EPCI)

Fusion_2012_Pysique_Corr = left_join(Fusion_2012_Pysique_Corr, Correspondance_EPCI,
                          by = "idcom_2023")

Ensemble_Prix_EPCI = Fusion_2012_Pysique_Corr %>%
  group_by(EPCI, Retraité) %>%
  summarise(Valeur_foncière = sum(Price, na.rm = T),
            Nombre_logements = sum(NB))

Ensemble_Prix_EPCI = Ensemble_Prix_EPCI %>%
  group_by(EPCI) %>%
  mutate(Pct_Retr = (Valeur_foncière[2]/(Valeur_foncière[1]+Valeur_foncière[2]))*100)
Ensemble_Prix_EPCI = Ensemble_Prix_EPCI[!duplicated(Ensemble_Prix_EPCI$EPCI),]

writexl::write_xlsx(Ensemble_Prix_EPCI, "Valo_EPCI_OLDDEP_2012_Par_EPCI.xlsx")

Ensemble_Prix = Fusion_2012_Pysique_Corr %>%
  group_by(idcom_2023) %>%
  summarise(Valeur_foncière = sum(Price, na.rm = T),
            Nombre_logements = sum(NB))
writexl::write_xlsx(Ensemble_Prix, "Valo_Commune(2023)_2012.xlsx")

######
OLDDEP_2012 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_Commune_2022.xlsx")
OLDDEP_2022 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_Commune(2023)_2012.xlsx")
OLDDEP = inner_join(OLDDEP_2012, OLDDEP_2022, by = "idcom")
colnames(OLDDEP)
OLDDEP$Diff = OLDDEP$Pct_Retr_2022-OLDDEP$Pct_Retr_2012
writexl::write_xlsx(OLDDEP, "Var_Valo_Communes_Tous_logements.xlsx")
######

Ensemble_Prix = Fusion_2012_Pysique %>%
  group_by(EPCI, Retraité) %>%
  summarise(Valeur_foncière = sum(Price, na.rm = T),
            Nombre_logements = sum(NB))
library(zoo)

Ensemble_Prix = Ensemble_Prix %>%
  group_by(EPCI) %>% 
  mutate(Pct_Retr = Valeur_foncière[2]/(Valeur_foncière[1]+Valeur_foncière[2]))
Ensemble_Prix = Ensemble_Prix[!duplicated(Ensemble_Prix$EPCI),]
writexl::write_xlsx(Ensemble_Prix, "Valo_EPCI_OLDDEP_2012.xlsx")

################Modélisation################
Capital_2012 = read.csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Valo_Propriétaire_2012.csv")
Capital_2012 = Capital_2012 %>% mutate(Age_Class = case_when(Age<65~"Actifs",
                                                             Age>=65~"Retraités"))
table(Capital_2012$Age_Class)
Capital_2012$Age_Class = factor(Capital_2012$Age_Class)
Capital_2012$Age_Class = relevel(Capital_2012$Age_Class,
                                 ref = 'Actifs')
colnames(Capital_2012)

Capital_2012 = Capital_2012 %>%
  mutate(Sexe = case_when(Sexe == "MLE"~"MME",
                          TRUE~Sexe))

OLS_2012 = lm(log(Valorisation)~Nombre_Logements+log(Surface)+Age+
                Sexe, 
              data = Capital_2012)
summary(OLS_2012)
Coefs = lmtest::coeftest(OLS_2012)[,] %>%
  as.data.frame() %>% 
  tibble::rownames_to_column(var = "term")
writexl::write_xlsx(Coefs, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/OLS_Propriétaire_2012.xlsx")

library(mgcv)
library(gratia)
GAM_2012 = gam(log(Valorisation)~Nombre_Logements+log(Surface)+s(Age)+
                Sexe, 
              data = Capital_2012)
summary(GAM_2012)
modelsummary::modelsummary(GAM_2012)
draw(GAM_2012)

ggplot(GAM_2012, aes(x = Age, y = Valorisation)) +
  geom_line() +
  theme(legend.position = "none") +
  labs(y = "Partial effect", x = "Age")


Capital_2022 = read.csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Valo_Propriétaire.csv")
Capital_2022 = Capital_2022 %>% mutate(Age_Class = case_when(Age<65~"Actifs",
                                                             Age>=65~"Retraités"))
table(Capital_2022$Age_Class)
Capital_2022$Age_Class = factor(Capital_2022$Age_Class)
Capital_2022$Age_Class = relevel(Capital_2022$Age_Class,
                                 ref = 'Actifs')
colnames(Capital_2022)

OLS_2022 = lm(log(Valorisation)~Nombre_Logements+log(Surface)+Age_Class+
           Sexe, 
         data = Capital_2022)
summary(OLS_2022)

Coefs = lmtest::coeftest(OLS_2022)[,] %>%
  as.data.frame() %>% 
  tibble::rownames_to_column(var = "term")
writexl::write_xlsx(Coefs, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/OLS_Propriétaire_2022.xlsx")

GAM_2022 = mgcv::gam(log(Valorisation)~Nombre_Logements+log(Surface)+s(Age)+
                 Sexe, 
               data = Capital_2022)
modelsummary::modelsummary(GAM_2022)
plot(GAM_2022)

Capital_IFI = Capital_2022 %>%
  filter(Valorisation >= 1300000)
mean(Capital_IFI$Valorisation)
quantile(Capital_IFI$Valorisation, probs = seq(0, 1, 0.010))

Iss = as.data.frame(quantile(Capital_2022$Valorisation, probs = seq(0, 1, 0.10)))
nrow(Capital_IFI)/nrow(Capital_2022)*100
##########################################################
Richesse_2012 = Capital_2012 %>%
  select(ID_Unique, Valorisation, Nombre_Logements)%>%
  rename(Valorisation_2012 = Valorisation,
         Nombre_Logements_2012 = Nombre_Logements)

Richesse_2022 = Capital_2022 %>%
  select(ID_Unique, Valorisation, Nombre_Logements, Age_Class, Sexe)%>%
  rename(Valorisation_2022 = Valorisation,
         Nombre_Logements_2022 = Nombre_Logements)

Variation_Richesse = inner_join(Richesse_2012, Richesse_2022, by = "ID_Unique")
Variation_Richesse$Var = (log(Variation_Richesse$Valorisation_2022)/log(Variation_Richesse$Valorisation_2012))-1
Variation_Richesse$Var_NB = Variation_Richesse$Nombre_Logements_2022/Variation_Richesse$Nombre_Logements_2012-1

mean(Variation_Richesse$Var)*100
mean(Variation_Richesse$Var_NB)*100

colnames(Fusion_2022)
###Nombre de départements dans lesquels le propriétaire détient un logement
#Départements en indicatrices : dep en colonne codé en 0 et 1

OLS_Var = lm(Var~Var_NB+Age_Class+
               Sexe, 
             data = Variation_Richesse)
summary(OLS_Var)

Multiproprio_2012 = Capital_2012 %>%
  filter(Nombre_Logements>1)
nrow(Multiproprio_2012)/nrow(Capital_2012)#20% de multipropriétaires en 2012

Multiproprio_2022 = Capital_2022 %>%
  filter(Nombre_Logements>1)
nrow(Multiproprio_2022)/nrow(Capital_2022)#20% de multipropriétaires en 2022

########################GWR#######################
library(dplyr)
library(lmtest)
library(sandwich)
BDD_GWR_Diff <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Var_OLDDEP_EPCI_Par_EPCI.xlsx")
Insee_Indicateurs_Diff <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Insee_Indicateurs_Diff.xlsx")
Valo_EPCI = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_EPCI_Physique_2022.xlsx")
EPCI_Metro_Dep <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Intercommunalite_Metropole_01-01-2023.xlsx")

colnames(Insee_Indicateurs_Diff)
BDD_GWR_Diff = BDD_GWR_Diff %>%
  left_join(Insee_Indicateurs_Diff, by = "EPCI") %>%
  left_join(Valo_EPCI, by = "EPCI")%>%
  left_join(EPCI_Metro_Dep, by = "EPCI")

OLS = lm(Diff~log(Res_Princ)+Taux_Act+TM+TN+Part_Prop+
           Ind_Vieil*log(Valo)+DEP,data = BDD_GWR_Diff)
coeftest(OLS, vcov = vcovHC, type = "HC0")
summary(OLS)
modelsummary::modelsummary(OLS)
#Une augmentation de la valorisation de l'EPCI conduit à une
#augmentation de la différence de richesse entre retraités
#et actifs

#Plus un EPCI est vieillissant, plus l'effet de la valorisation
#sur la différence de richesse va être important:
#Pour chaque augmentation d'1 point de l'indice de vieillissement,
#l'augmentation de la valeur du capital de logement dans l'EPCI
#entraine une hausse du glissement du patrimoine total de 
#logement des actifs vers les retraités de 0.3%.
#Isolement de l'effet du vieillissement: les vieux se sont bien
#enrichis par rapport aux actifs (en moyenne).

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
library(lmtest)
library(sandwich)

OLS = lm(Diff_Niveau~Var_Part_Propr+TN+TM+
           Var_Part_Res_Princ+Var_Taux_Act+
           Var_Valo+`Var_Part_65+`+
           relevel(Dep, ref = "69"),
         data = BDD_GWR_Diff)
summary(OLS)
coeftest(OLS, vcov = vcovHC, type = "HC0")
modelsummary::modelsummary(coeftest(OLS, vcov = vcovHC, type = "HC0"))
cor.test(BDD_GWR_Diff$`Var_Part_65+`, BDD_GWR_Diff$Diff)

OLS_Metro = lm(Var_Valo~Var_Part_Propr+TN+TM+
                 Var_Part_Res_Princ+Var_Taux_Act+
                 Diff+`Var_Part_65+`+
                 relevel(Dep, ref = "69"),
         data = BDD_GWR_Diff)
summary(OLS_Metro)
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
#SDM
n_data <- nrow(model.frame(SDM))  # Nombre d'observations dans le modèle
n_listw <- length(W$neighbours)    # Nombre de voisins dans listw
print(c(n_data, n_listw))









##Fond de carte SHP##
EPCI_SHP = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/DSN/EPCI',
                       layer = 'EPCI')
EPCI_SHP <- sf::st_transform(EPCI_SHP, crs = 4326)

trueCentroids = sf::st_centroid(EPCI_SHP,byid=TRUE)
Centroides = as.data.frame(trueCentroids$geometry)
EPCI_Data = as.data.frame(EPCI_SHP$CODE_SIREN)
trueCentroids = data.frame(sf::st_coordinates(sf::st_cast(trueCentroids$geometry,"POINT")))
trueCentroids = trueCentroids %>%
  rename(Longitude = X,
         Latitude = Y)
EPCI_SHP = cbind(EPCI_Data, trueCentroids)
EPCI_SHP = EPCI_SHP %>%
  rename(EPCI = `EPCI_SHP$CODE_SIREN`)

BDD_GWR_Diff = left_join(BDD_GWR_Diff, EPCI_SHP,
                         by = "EPCI")
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Longitude),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Niv_Med),]

library(GWmodel)
my.sf.point <- sf::st_as_sf(x = BDD_GWR_Diff,
                            coords = c("Longitude", "Latitude"),
                            crs = "+proj=longlat +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0")
Fusion_EPCI_patial <- as(my.sf.point, "Spatial")

coords <- as.matrix(coordinates(Fusion_EPCI_patial))
dm.calib <- gw.dist(dp.locat=coordinates(Fusion_EPCI_patial))
plot(Fusion_EPCI_patial)

bw0 <- bw.gwr(Diff~log(Niv_Med)+Taux_Act+
              Ind_Vieil*log(Valo),
              data = Fusion_EPCI_patial, approach="AICc",
              kernel="gaussian",
              adaptive=F,dMat=dm.calib)

GWR_Robust = gwr.robust(Diff~log(Niv_Med)+Taux_Act+
                        Ind_Vieil*log(Valo),
                        data=Fusion_EPCI_patial,
                        dMat = dm.calib,
                        bw = bw0,
                        kernel="gaussian",adaptive=F)
GWR_Robust
sp = GWR_Robust$SDF
sp$EPCI = BDD_GWR_Diff$EPCI
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
library(raster)
shapefile(sp, "Cartes GWR/GWR_EPCI_Diff.shp",overwrite=TRUE)

plot(GWR_Robust[["SDF"]]@data[["log(Valeur_foncière_2022)"]],
     log(Fusion_EPCI_patial$Valeur_foncière_2022))
