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

#Catégories croisées
comptes_categories_croisees <- Fusion_2022 %>%
  group_by(catpro3) %>%
  summarise(n = n(),
            Valo = sum(Price))
writexl::write_xlsx(comptes_categories_croisees, 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Catégories_propriétaires_croisées_2.xlsx')
library(tidyr)
###
logements_long <- Fusion_2022 %>%
  select(catpro3, Price)%>%
  separate_rows(catpro3, sep = " ") # Éclate les catégories multiples

# Étape 2 : Compter les occurrences individuelles
comptes_categories <- logements_long %>%
  group_by(catpro3) %>%
  summarise(n = n(),
            Valo = sum(Price),
            , .groups = "drop")
writexl::write_xlsx(comptes_categories, 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Catégories_propriétaires_croisées_1.xlsx')

###

logements_long <- Fusion_2022 %>%
  select(catpro3)

library(data.table)
logements_long = as.data.table(logements_long)
logements_long[, catpro3 := strsplit(catpro3, " ")] # Transforme chaque catégorie en une liste

# Étape 2 : Compter les occurrences
comptes_categories <- logements_long[, .(catpro3 = unlist(catpro3))] # Unlist pour avoir une colonne "longue"
comptes_resultat <- comptes_categories[, .N, by = catpro3]      # Compte les occurrences par catégorie

# Trier les résultats pour lisibilité (optionnel)
comptes_resultat <- comptes_resultat[order(-N)]

# Résultat final
print(comptes_resultat)
writexl::write_xlsx(comptes_resultat, 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Catégories_propriétaires.xlsx')


####% de multipropriétaires par ville####
Fusion_2022_Pysique = Fusion_2022 %>%
  filter(Type_Proprio=="Personne physique",
         Age>=18, Age<=100)
help(quantile)
quantile(Fusion_2022_Pysique$Price, probs = seq(0.999,1, 0.001))

DF_Proprio <- Fusion_2022_Pysique %>%
  group_by(ID_Unique) %>%                     # Grouper par l'identifiant du propriétaire
  mutate(Multi = ifelse(n() > 1, 1, 0)) %>% # Identifier si le propriétaire a plusieurs logements
  ungroup()
mean(DF_Proprio$Multi)

DF_Proprio <- Fusion_2022_Pysique %>%
  group_by(idcom) %>%
  summarise(Valo = sum(Price)) %>%
  ungroup()
writexl::write_xlsx(DF_Proprio, 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_Commune_Sans_Age.xlsx')

####Classe d'âge####
Fusion_2022_Pysique = Fusion_2022_Pysique %>%
  mutate(Age_Class = case_when(Age >=18&Age <=30 ~"18-30",
                               Age >=31&Age <=40 ~"31-40",
                               Age >=41&Age <=50 ~"41-50",
                               Age >=51&Age <=65 ~"51-65",
                               Age >65~"65+"))

Fusion_Age_18 = Fusion_2022_Pysique %>%
  filter(Age_Class=="65+") %>%
  group_by(EPCI) %>%
  summarise(Patrimoine = sum(Price))
writexl::write_xlsx(Fusion_Age_18, 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_65+_EPCI.xlsx')

Proprio_NA = Fusion_2022_Pysique[is.na(Fusion_2022_Pysique$Age),]
options(scipen = 10)
sum(Proprio_NA$Price)

###Multiproprio par commune####
colnames(Fusion_2022_Pysique)
DF_Proprio_1 = Fusion_2022_Pysique %>%
  group_by(idcom, Age_Class) %>%
  summarise(Valeur_foncière_2022 = sum(Price),
            Proprio_2022 = n())%>%
  ungroup()
colnames(DF_Proprio_1)

Ensemble_Prix = DF_Proprio_1 %>%
  group_by(idcom) %>% 
  mutate(Pct_Valo = (Valeur_foncière_2022[2]/(Valeur_foncière_2022[1]+Valeur_foncière_2022[2]))*100)
Ensemble_Prix = Ensemble_Prix[!duplicated(Ensemble_Prix$Dep),]

writexl::write_xlsx(Ensemble_Prix, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_Age_Dep_2022.xlsx")

###Multiproprio par EPCI####
Correspondance_EPCI = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Intercommunalite_Metropole_au_01-01-2023.xlsx",
                                        sheet = "Composition_communale")
Fusion_2022_Pysique = left_join(Fusion_2022_Pysique, Correspondance_EPCI,
                                by = "idcom")

Ens_Prix_EPCI = DF_Proprio %>%
  group_by(EPCI) %>%
  summarise(Valeur_foncière_2022 = sum(Price),
            NB = n())%>%
  ungroup()
write.csv(Ens_Prix_EPCI, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_Par_EPCI_2022.csv")

Ens_Prix_EPCI = Fusion_2022_Pysique %>%
  group_by(Age,idcom) %>%
  summarise(Valeur_foncière_2022 = sum(Price),
            NB = n())%>%
  ungroup()
writexl::write_xlsx(Ens_Prix_EPCI, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_Age_Comm_2022.xlsx")


DF_Proprio_1 = DF_Proprio %>%
  group_by(EPCI, Multi) %>%
  summarise(Valeur_foncière_2022 = sum(Price),
            Proprio_2022 = n())%>%
  ungroup()
colnames(DF_Proprio_1)

Ensemble_Prix = DF_Proprio_1 %>%
  group_by(EPCI) %>% 
  mutate(Pct_Multi = (Valeur_foncière_2022[2]/(Valeur_foncière_2022[1]+Valeur_foncière_2022[2]))*100)
Ensemble_Prix = Ensemble_Prix[!duplicated(Ensemble_Prix$EPCI),]
writexl::write_xlsx(Ensemble_Prix, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Multi_2022_Var_EPCI.xlsx")


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

Correspondance = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Tableau de correspondances 2012_2022.xlsx")
Fusion_2012 = left_join(Fusion_2012, Correspondance,
                                by = "idcom")
colnames(Fusion_2012)
Fusion_2012 = Fusion_2012 %>% ungroup %>%
  select(-idcom)
Fusion_2012 = Fusion_2012 %>%
  rename(idcom = idcom_2023)

####% de multipropriétaires par ville####
Fusion_2012_Pysique = Fusion_2012 %>%
  filter(Type_Proprio=="Personne physique",
         Age>=18, Age<=100)

Proprio_NA = Fusion_2012_Pysique[is.na(Fusion_2012_Pysique$Age),]
options(scipen = 10)
sum(Proprio_NA$Price)
1+1

quantile(Fusion_2012_Pysique$Price, probs = seq(0.999,1, 0.001))

####Classe d'âge####
Fusion_2012_Pysique = Fusion_2012_Pysique %>%
  mutate(Age_Class = case_when(Age >=18&Age <=30 ~"18-30",
                               Age >=31&Age <=40 ~"31-40",
                               Age >=41&Age <=50 ~"41-50",
                               Age >=51&Age <=65 ~"51-65",
                               Age >65~"65+"))

Fusion_Age_18 = Fusion_2012_Pysique %>%
  filter(Age_Class=="65+") %>%
  group_by(EPCI) %>%
  summarise(Patrimoine = sum(Price))
writexl::write_xlsx(Fusion_Age_18, 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_65+_EPCI_2012.xlsx')


DF_Proprio_2012 <- Fusion_2012_Pysique %>%
  group_by(ID_Unique) %>%                     # Grouper par l'identifiant du propriétaire
  mutate(Multi = ifelse(n() > 1, 1, 0)) %>% # Identifier si le propriétaire a plusieurs logements
  ungroup()

###Multiproprio par commune####
DF_Proprio_1 = Fusion_2012_Pysique %>%
  group_by(Dep, Age_Class) %>%
  summarise(Valeur_foncière_2012 = sum(Price),
            Proprio_2012 = n())%>%
  ungroup()
colnames(DF_Proprio_1)

Ensemble_Prix = DF_Proprio_1 %>%
  group_by(Dep) %>% 
  mutate(Pct_Valo = (Valeur_foncière_2012[2]/(Valeur_foncière_2012[1]+Valeur_foncière_2012[2]))*100)
Ensemble_Prix = Ensemble_Prix[!duplicated(Ensemble_Prix$Dep),]

writexl::write_xlsx(Ensemble_Prix, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_EPCI_2012.xlsx")

Valo_Age_EPCI_2012 <- read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_Age_EPCI_2012.xlsx")
Valo_Age_EPCI_2022 <- read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_Age_EPCI_2022.xlsx")

Valo_Age_EPCI = left_join(Valo_Age_EPCI_2022, Valo_Age_EPCI_2012, by = c("EPCI","Age"))
writexl::write_xlsx(Valo_Age_EPCI, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_Age_EPCI.xlsx")




Multi_2012 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo65+_2012_Var.xlsx")
Multi_2022 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo65+_2022_Var.xlsx")

Multi = inner_join(Multi_2012, Multi_2022, by = "idcom")
writexl::write_xlsx(Multi, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Comm_Diff_Var.xlsx")

###Multiproprio par EPCI####
Correspondance_EPCI = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Intercommunalite_Metropole_au_01-01-2023.xlsx",
                                        sheet = "Composition_communale")
Fusion_2012 = left_join(Fusion_2012, Correspondance_EPCI,
                       by = "idcom")
table(is.na(DF_Proprio_2012$EPCI))/nrow(DF_Proprio_2012)

Ens_Prix_EPCI = Fusion_2012_Pysique %>%
  group_by(idcom) %>%
  summarise(Valeur_foncière_2012 = sum(Price))%>%
  ungroup()

writexl::write_xlsx(Ens_Prix_EPCI, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_Par_Commune_2012_Sans_Age.xlsx")
Comm_2022 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_Commune_Sans_Age.xlsx")

Issou = inner_join(Ens_Prix_EPCI, Comm_2022, by = 'idcom')
writexl::write_xlsx(Issou, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Var_K_Commune_Sans_Age.xlsx")

Multi_2012 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo65+2022_Var.xlsx")
Multi_2022 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo65+2012_Var.xlsx")

Multi = inner_join(Multi_2012, Multi_2022, by = "EPCI")
Multi$Var_Valo = log(Multi$Valeur_foncière_2022)-log(Multi$Valeur_foncière_2012)
writexl::write_xlsx(Multi, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Var_Valo_EPCI.xlsx")


DF_Proprio_1 = DF_Proprio_2012 %>%
  group_by(EPCI, Multi) %>%
  summarise(Valeur_foncière_2012 = sum(Price),
            Proprio_2012 = n())%>%
  ungroup()
colnames(DF_Proprio_1)

Ensemble_Prix = DF_Proprio_1 %>%
  group_by(EPCI) %>% 
  mutate(Pct_Multi = (Valeur_foncière_2012[2]/(Valeur_foncière_2012[1]+Valeur_foncière_2012[2]))*100)
Ensemble_Prix = Ensemble_Prix[!duplicated(Ensemble_Prix$EPCI),]
writexl::write_xlsx(Ensemble_Prix, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Multi_2012_Var_EPCI.xlsx")

####Modélisation Multiproprio EPCI####
BDD_GWR_Diff <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Var_OLDDEP_EPCI_Par_EPCI.xlsx")
Multi_Diff <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Multi_Diff_Var_EPCI.xlsx")
Insee_Indicateurs_Diff <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Insee_Diff_Variations_EPCI.xlsx")
Var_Valo <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Var_Valo_EPCI.xlsx")

BDD_GWR_Diff = BDD_GWR_Diff %>%
  left_join(Insee_Indicateurs_Diff, by = "EPCI") %>%
  left_join(Multi_Diff, by = "EPCI")%>%
  left_join(Var_Valo, by = "EPCI")
writexl::write_xlsx(BDD_GWR_Diff, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/BDD_GWR_Diff_EPCI.xlsx")

colnames(BDD_GWR_Diff)
library(lmtest)
library(sandwich)
options(scipen = 5)
OLS = lm(Diff~Var_Nb_Log+Var_Nb_Res_Princ+Var_Part_Res_Princ+
           Var_Part_Res_Sec+Var_Part_Prop+Var_Part_Loc+TN+TM+
           Var_Part_Pers_65+EPHAD+Taux_Pauv+Lycee+
           Med_Gen+Var_Valo,
         data = BDD_GWR_Diff)
summary(OLS)
coeftest(OLS, vcov = vcovHC, type = "HC0")
modelsummary::modelsummary(coeftest(OLS, vcov = vcovHC, type = "HC0"))
qqplot(BDD_GWR_Diff$Var_Part_65, BDD_GWR_Diff$Diff)
#Effets linéaires

OLS_2 = lm(Multi_Diff~Var_Nb_Log+Var_Nb_Res_Princ+Var_Part_Res_Princ+
             Var_Part_Res_Sec+Var_Part_Prop+Var_Part_Loc+TN+TM+
             Var_Part_Pers_65+EPHAD+Taux_Pauv+Lycee+
             Med_Gen+Var_Valo,
         data = BDD_GWR_Diff)
summary(OLS_2)
coeftest(OLS_2, vcov = vcovHC, type = "HC0")
modelsummary::modelsummary(coeftest(OLS_2, vcov = vcovHC, type = "HC0"))
qqplot(BDD_GWR_Diff$Var_Part_65, BDD_GWR_Diff$Multi_Diff)

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
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$EPHAD),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Taux_Pauv),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Lycee),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Med_Gen),]

library(GWmodel)
my.sf.point <- sf::st_as_sf(x = BDD_GWR_Diff,
                            coords = c("Longitude", "Latitude"),
                            crs = "+proj=longlat +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0")
Fusion_EPCI_patial <- as(my.sf.point, "Spatial")

coords <- as.matrix(coordinates(Fusion_EPCI_patial))
dm.calib <- gw.dist(dp.locat=coordinates(Fusion_EPCI_patial))

bw0 <- bw.gwr(Diff~Var_Nb_Log+Var_Nb_Res_Princ+Var_Part_Res_Princ+
                Var_Part_Res_Sec+Var_Part_Prop+Var_Part_Loc+TN+TM+
                Var_Part_Pers_65+EPHAD+Taux_Pauv+Lycee+
                Med_Gen+Var_Valo,
              data = Fusion_EPCI_patial, approach="AICc",
              kernel="gaussian",
              adaptive=F,dMat=dm.calib)

GWR_Robust = gwr.robust(Diff~Var_Nb_Log+Var_Nb_Res_Princ+Var_Part_Res_Princ+
                          Var_Part_Res_Sec+Var_Part_Prop+Var_Part_Loc+TN+TM+
                          Var_Part_Pers_65+EPHAD+Taux_Pauv+Lycee+
                          Med_Gen+Var_Valo,
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

bw0 <- bw.gwr(Multi_Diff~Var_Nb_Log+Var_Nb_Res_Princ+Var_Part_Res_Princ+
                Var_Part_Res_Sec+Var_Part_Prop+Var_Part_Loc+TN+TM+
                Var_Part_Pers_65+EPHAD+Taux_Pauv+Lycee+
                Med_Gen+Var_Valo,
              data = Fusion_EPCI_patial, approach="AICc",
              kernel="gaussian",
              adaptive=T,dMat=dm.calib)

GWR_Robust = gwr.robust(Multi_Diff~Var_Nb_Log+Var_Nb_Res_Princ+Var_Part_Res_Princ+
                          Var_Part_Res_Sec+Var_Part_Prop+Var_Part_Loc+TN+TM+
                          Var_Part_Pers_65+EPHAD+Taux_Pauv+Lycee+
                          Med_Gen+Var_Valo,
                        data=Fusion_EPCI_patial,
                        dMat = dm.calib,
                        bw = bw0,
                        kernel="gaussian",adaptive=T)
GWR_Robust
sp = GWR_Robust$SDF
sp$EPCI = BDD_GWR_Diff$EPCI
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
library(raster)
shapefile(sp, "Cartes GWR/GWR_EPCI_Multi_Diff.shp",overwrite=TRUE)


####Modélisation Multiproprio Commune####
rm(list=ls())
library(dplyr)
BDD_GWR_Diff <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Comm_Diff_Var.xlsx")
Multi_Diff <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Multi_Diff_Var.xlsx")
Insee_Indicateurs_Diff <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Insee_Diff_Variations.xlsx")
Loi_Litt <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/typo_loilitt.xlsx")
Valo_Communes <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_Commune_2022.xlsx")
OLDDEP <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Var_OLDDEP_Commune_Final.xlsx")
UU <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Unité urbaine INSEE.xlsx")
UU$UU = as.factor(UU$UU)

BDD_GWR_Diff = BDD_GWR_Diff %>%
  left_join(Insee_Indicateurs_Diff, by = "idcom") %>%
  left_join(Valo_Communes, by = "idcom") %>%
  left_join(Multi_Diff, by = "idcom") %>%
  left_join(Loi_Litt, by = 'idcom')%>%
  left_join(OLDDEP, by = 'idcom')%>%
  left_join(UU, by = 'idcom')

writexl::write_xlsx(BDD_GWR_Diff, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Base_Finale_Modélisation.xlsx")

BDD_GWR_Diff$Dep = substr(BDD_GWR_Diff$idcom, start = 1, stop = 2)
BDD_GWR_Diff$Dep = factor(BDD_GWR_Diff$Dep)
colnames(BDD_GWR_Diff)
library(lmtest)
library(sandwich)

OLS_1 = lm(Diff_Niveau~Var_Part_Res_Sec+
             Var_Part_Prop+
             Multi_Diff+TN+TM+
             Var_Part_Pers_65,
         data=BDD_GWR_Diff)
summary(OLS_1)
colnames(BDD_GWR_Diff)
coeftest(OLS_1, vcov = vcovHC, type = "HC0")
modelsummary::modelsummary(coeftest(OLS_1, vcov = vcovHC, type = "HC0"))
qqplot(BDD_GWR_Diff$Var_Part_Pers_65, BDD_GWR_Diff$Diff_Niveau)

#
colnames(BDD_GWR_Diff)
OLS_2 = lm(Diff_Niveau~Var_Part_Res_Sec+
             Var_Part_Prop+
             Multi_Diff+TN+TM+
             Var_Part_Pers_65*
             relevel(UU, ref = "H")+
             loilitt_simp+log(`Logements 2021`),
           data=BDD_GWR_Diff)
summary(OLS_2)
coeftest(OLS_2, vcov = vcovHC, type = "HC0")
Result_OLS_2 = coeftest(OLS_2, vcov = vcovHC, type = "HC0")
modelsummary::modelsummary(Result_OLS_2)
modelsummary::modelsummary(OLS_2)

OLS_3 = lm(Diff_Niveau~Var_Part_Res_Sec+
             Var_Part_Prop+
             Multi_Diff+TN+TM+
             Var_Part_Pers_65*
             relevel(UU, ref = "H")+relevel(Dep, ref = "69"),
           data=BDD_GWR_Diff)
summary(OLS_3)
Result_OLS_3 = coeftest(OLS_3, vcov = vcovHC, type = "HC0")
modelsummary::modelsummary(Result_OLS_3)
modelsummary::modelsummary(OLS_3)

hist(BDD_GWR_Diff$Multi_Diff)


####GWR par commune####
Comm_SHP = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/DSN/Communes France + ROM',
                       layer = 'COMMUNE')
trueCentroids = sf::st_centroid(Comm_SHP,byid=TRUE)
Centroides = as.data.frame(trueCentroids$geometry)
EPCI_Data = as.data.frame(Comm_SHP$INSEE_COM)
trueCentroids = data.frame(sf::st_coordinates(sf::st_cast(trueCentroids$geometry,"POINT")))
trueCentroids = trueCentroids %>%
  rename(Longitude = X,
         Latitude = Y)
Comm_SHP = cbind(EPCI_Data, trueCentroids)
Comm_SHP = Comm_SHP %>%
  rename(idcom = `Comm_SHP$INSEE_COM`)

BDD_GWR_Diff = left_join(BDD_GWR_Diff, Comm_SHP,
                         by = "idcom")
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Var_Part_Res_Sec),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Var_Part_Prop),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Var_Part_Loc),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Multi_Diff),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$TM),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$TN),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Var_Part_Pers_65),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Longitude),]

library(spdep)
library(sp)
library(GWmodel)
my.sf.point <- sf::st_as_sf(x = BDD_GWR_Diff,
                            coords = c("Longitude", "Latitude"),
                            crs = "+proj=longlat +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0")
Fusion_EPCI_patial <- as(my.sf.point, "Spatial")

coords <- as.matrix(coordinates(Fusion_EPCI_patial))
dm.calib <- gw.dist(dp.locat=coordinates(Fusion_EPCI_patial))

bw0 <- bw.gwr(Diff_Niveau~Var_Part_Res_Sec+
                Var_Part_Prop+
                Multi_Diff+TN+TM+
                Var_Part_Pers_65,
              data = Fusion_EPCI_patial, approach="AICc",
              kernel="bisquare",
              adaptive=T,dMat=dm.calib)
#425
Sca_GWR = gwr.scalable(Diff_Niveau~Var_Part_Res_Sec+
                         Var_Part_Prop+
                         Multi_Diff+TN+TM+
                         Var_Part_Pers_65,
                        data=Fusion_EPCI_patial,
                        dMat = dm.calib,
                       bw.adapt = 310, longlat = F,
                        kernel="gaussian")
Sca_GWR
sp = Sca_GWR$SDF
BDD_GWR_Diff$Var_OLDDEP_Niv
sp$idcom = BDD_GWR_Diff$idcom
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
library(raster)
shapefile(sp, "Cartes GWR/GWR_Commune_Diff_OLDDEP.shp",overwrite=TRUE)

Sca_GWR_2 = gwr.scalable(Multi_Diff~Var_Part_Res_Princ+
                         Var_Part_Res_Sec+Var_Part_Prop+
                         Var_Part_Loc+Var_Part_Pers_65+
                         TM+TN+Part_Cadres_Sup+
                         log(Valeur_foncière_2022_Ensemble),
                       data=Fusion_EPCI_patial,
                       dMat = dm.calib,
                       bw.adapt = 425, longlat = F,
                       kernel="gaussian")
Sca_GWR_2
sp = Sca_GWR_2$SDF
sp$idcom = BDD_GWR_Diff$idcom
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
library(raster)
shapefile(sp, "Cartes GWR/GWR_Commune_Diff_Multi.shp",overwrite=TRUE)

library(ggplot2)
ggplot() + geom_sf(data = sf, aes(fill=Var_Part_Pers_65)) +
  coord_sf()

#Effets linéaires
spdep::lm.LMtests(OLS,W,test="RLMerr")
spdep::lm.LMtests(OLS,W,test="RLMlag")


library(spdep)
Comm_SHP = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/DSN/EPCI',
                       layer = 'EPCI')
Comm_SHP <- sf::st_transform(Comm_SHP, crs = 4326)
Comm_SHP = Comm_SHP %>%
  rename(EPCI = `CODE_SIREN`)
Comm_SHP = Comm_SHP %>%
  right_join(BDD_GWR_Diff, by = "EPCI")

Comm_SHP = Comm_SHP[!is.na(Comm_SHP$TN),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$TM),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$Var_Part_Res_Princ),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$Var_Taux_Act),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$Var_Valo),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$Var_Part_65),]

#Faire correspondre les lignes de la matrice W et la DF

Comm_SHP_patial <- as(Comm_SHP, "Spatial")

library(sp)
library(spatialreg)
library(spdep)
#Première matrice de poids
nb = poly2nb(Comm_SHP, queen=T, row.names = Comm_SHP$EPCI)
Comm_SHP = as.data.frame(Comm_SHP)
rownames(Comm_SHP) = Comm_SHP$idcom
W <- nb2listw(nb, style = "W",zero.policy = T)
length(W$neighbours)

SDM = lagsarlm(Diff~Var_Part_Prop+TN+TM+
                 Var_Part_Res_Princ+Var_Taux_Act+
                 Var_Valo+Var_Part_65,
               listw=W, data=Comm_SHP, 
               type = "mixed", method="MC",
               zero.policy = T)
summary(SDM)
Impacts_SDM = impacts(SDM, listw = W, R = 100)
summary(Impacts_SDM)

plot(BDD_GWR_Diff$Var_Part_Pers_65, BDD_GWR_Diff$Diff_Niveau)
help(plot)


SDM_2 = lagsarlm(Multi_Diff~Var_Part_Prop+TN+TM+
                 Var_Part_Res_Princ+Var_Taux_Act+
                 Var_Valo+Var_Part_65,
               listw=W, data=Comm_SHP, 
               type = "mixed", method="MC",
               zero.policy = T)
summary(SDM_2)
Impacts_SDM_2 = impacts(SDM_2, listw = W, R = 100)
summary(Impacts_SDM_2)

library(ggplot2)
library(ggthemes)
help(cor)
stats::cor.test(BDD_GWR_Diff$Diff_Niveau, BDD_GWR_Diff$Var_Part_Pers_65, method = "spearman", na.rm = T)
ggplot(BDD_GWR_Diff, aes(y = Diff_Niveau, x = Var_Part_Pers_65)) +
  theme_minimal()+
  geom_smooth(method = lm, formula = y ~ x, se = FALSE, color = "cyan4") +
  geom_point()+
  geom_text(x = -50, y = 47,
            label = paste0(expression(Delta~"HOUSDEP"), 0.429),
            color = 'black', size = 7, family = "serif")+
  ylab(expression(Delta~"HOUSDEP"))+
  xlab(expression(Delta~"Retirees"))+
  theme(axis.text.x = element_text(size = 19, family="serif", color = "black"),
        axis.text.y = element_text(size = 19, family="serif", color = "black"),
        axis.title.y = element_text(size = 22, family="serif", color = "black"),
        axis.title.x = element_text(size = 22, family="serif", color = "black"))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
ggsave("Retirees_Housdep.jpeg", units="in", width=10, height=6.5)


issou = read.csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Valo_Propriétaire.csv")
colnames(issou)
quantile(issou$Valorisation, probs = seq(0.999,1, by = 0.001), na.rm = T)


issou = read.csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Valo_Propriétaire_2012.csv")
quantile(issou$Valorisation, probs = seq(0.999,1, by = 0.001), na.rm = T)


####Fusions cartes ages####
#18-30
library(readxl)
Age_18_EPCI <- read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_18-30_EPCI.xlsx")
Age_18_EPCI_2012 <- read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_18-30_EPCI_2012.xlsx")
Valo_Comm_2012 <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_EPCI_OLDDEP_2012_Par_EPCI.xlsx")
Valo_Comm_2012 = Valo_Comm_2012 %>% select(EPCI, Valeur_foncière_2012)
Valo_Comm <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_EPCI_OLDDEP_2022_Par_EPCI.xlsx")
Valo_Comm = Valo_Comm %>% select(EPCI, Valeur_foncière_2022)

Age_18_VarK = Age_18_EPCI %>%
  inner_join(Age_18_EPCI_2012, by = "EPCI")%>%
  inner_join(Valo_Comm_2012, by = "EPCI")%>%
  inner_join(Valo_Comm, by = "EPCI")
  
Age_18_VarK$K_2012 = Age_18_VarK$Patrimoine_2012/Age_18_VarK$Valeur_foncière_2012
Age_18_VarK$K_2022 = Age_18_VarK$Patrimoine_2022/Age_18_VarK$Valeur_foncière_2022
Age_18_VarK$Diff_K_18 = Age_18_VarK$K_2022-Age_18_VarK$K_2012
mean(Age_18_VarK$Diff_K_18)

#31-40
Age_31_40_EPCI <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_31-40_EPCI.xlsx")
Age_31_40_EPCI_2012 <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_31-40_EPCI_2012.xlsx")

Age_31_40_VarK = Age_31_40_EPCI %>%
  inner_join(Age_31_40_EPCI_2012, by = "EPCI")%>%
  inner_join(Valo_Comm_2012, by = "EPCI")%>%
  inner_join(Valo_Comm, by = "EPCI")

Age_31_40_VarK$K_2012 = Age_31_40_VarK$Patrimoine_2012/Age_31_40_VarK$Valeur_foncière_2012
Age_31_40_VarK$K_2022 = Age_31_40_VarK$Patrimoine_2022/Age_31_40_VarK$Valeur_foncière_2022
Age_31_40_VarK$Diff_K_31_40 = Age_31_40_VarK$K_2022-Age_31_40_VarK$K_2012
mean(Age_31_40_VarK$Diff_K_31_40)

#41-50
Age_41_50_EPCI <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_41-50_EPCI.xlsx")
Age_41_50_EPCI_2012 <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_41-50_EPCI_2012.xlsx")

Age_41_50_VarK = Age_41_50_EPCI %>%
  inner_join(Age_41_50_EPCI_2012, by = "EPCI")%>%
  inner_join(Valo_Comm_2012, by = "EPCI")%>%
  inner_join(Valo_Comm, by = "EPCI")

Age_41_50_VarK$K_2012 = Age_41_50_VarK$Patrimoine_2012/Age_41_50_VarK$Valeur_foncière_2012
Age_41_50_VarK$K_2022 = Age_41_50_VarK$Patrimoine_2022/Age_41_50_VarK$Valeur_foncière_2022
Age_41_50_VarK$Diff_K_41_50 = Age_41_50_VarK$K_2022-Age_41_50_VarK$K_2012
mean(Age_41_50_VarK$Diff_K_41_50)

#51-65
Age_51_60_EPCI <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_51-65_EPCI.xlsx")
Age_51_60_EPCI_2012 <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_51-65_EPCI_2012.xlsx")

Age_51_60_VarK = Age_51_60_EPCI %>%
  inner_join(Age_51_60_EPCI_2012, by = "EPCI")%>%
  inner_join(Valo_Comm_2012, by = "EPCI")%>%
  inner_join(Valo_Comm, by = "EPCI")

Age_51_60_VarK$K_2012 = Age_51_60_VarK$Patrimoine_2012/Age_51_60_VarK$Valeur_foncière_2012
Age_51_60_VarK$K_2022 = Age_51_60_VarK$Patrimoine_2022/Age_51_60_VarK$Valeur_foncière_2022
Age_51_60_VarK$Diff_K_51_60 = Age_51_60_VarK$K_2022-Age_51_60_VarK$K_2012
mean(Age_51_60_VarK$Diff_K_51_60)

#65+
Age_65_EPCI <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_65+_EPCI.xlsx")
Age_65_EPCI_2012 <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_65+_EPCI_2012.xlsx")

Age_65_VarK = Age_65_EPCI %>%
  inner_join(Age_65_EPCI_2012, by = "EPCI")%>%
  inner_join(Valo_Comm_2012, by = "EPCI")%>%
  inner_join(Valo_Comm, by = "EPCI")

Age_65_VarK$K_2012 = Age_65_VarK$Patrimoine_2012/Age_65_VarK$Valeur_foncière_2012
Age_65_VarK$K_2022 = Age_65_VarK$Patrimoine_2022/Age_65_VarK$Valeur_foncière_2022
Age_65_VarK$Diff_K_65 = Age_65_VarK$K_2022-Age_65_VarK$K_2012
mean(Age_65_VarK$Diff_K_65)

#Exports
writexl::write_xlsx(Age_18_VarK, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Carte_18_30_EPCI.xlsx")
writexl::write_xlsx(Age_31_40_VarK, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Carte_31_40_EPCI.xlsx")
writexl::write_xlsx(Age_41_50_VarK, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Carte_41_50_EPCI.xlsx")
writexl::write_xlsx(Age_51_60_VarK, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Carte_51_60_EPCI.xlsx")
writexl::write_xlsx(Age_65_VarK, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Carte_65+_EPCI.xlsx")
