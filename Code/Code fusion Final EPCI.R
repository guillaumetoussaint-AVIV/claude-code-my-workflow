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
nrow(Fusion_2022)




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
rm(Fusion_2022_97)

####EPCI####
Correspondance_EPCI_2024 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/EPCI_au_01-01-2024.xlsx",
                                        sheet = "Composition_communale")
Correspondance_EPCI_2023 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Intercommunalite_Metropole_au_01-01-2023.xlsx",
                                        sheet = "Composition_communale")
Correspondance_EPCI_2022 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Intercommunalite_Metropole_au_01-01-2022.xlsx",
                                             sheet = "Composition_communale")
Correspondance_EPCI_2021 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Intercommunalite_Metropole_au_01-01-2021.xlsx",
                                             sheet = "Composition_communale")

Fusion_2022 = Fusion_2022 %>% 
  left_join(Correspondance_EPCI_2021, by = "idcom") %>%
  left_join(Correspondance_EPCI_2022, by = "idcom") %>%
  left_join(Correspondance_EPCI_2023, by = "idcom") %>%
  left_join(Correspondance_EPCI_2024, by = "idcom")

colnames(Fusion_2022)
table(is.na(Fusion_2022$EPCI_2021))/nrow(Fusion_2022)
table(is.na(Fusion_2022$EPCI_2022))/nrow(Fusion_2022)
table(is.na(Fusion_2022$EPCI_2023))/nrow(Fusion_2022)
table(is.na(Fusion_2022$EPCI_2024))/nrow(Fusion_2022)

NA_EPCI_2022 = Fusion_2022[is.na(Fusion_2022$EPCI_2022),]
NA_EPCI_2023 = Fusion_2022[is.na(Fusion_2022$EPCI_2023),]
NA_EPCI_2024 = Fusion_2022[is.na(Fusion_2022$EPCI_2024),]

Ens_Prix_EPCI_1 = Fusion_2022 %>%
  group_by(EPCI_2022) %>%
  summarise(Valeur_foncière_2022 = sum(Price),
            NB = n())%>%
  ungroup()
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
writexl::write_xlsx(Ens_Prix_EPCI_1,"Valo_EPCI_2022.xlsx")

####% de K détenu par les multipropriétaires####
Fusion_2022_Pysique = Fusion_2022 %>%
  filter(Type_Proprio=="Personne physique",
         Age>=18, Age<=100)
colnames(Fusion_2022_Pysique)

Correspondance_EPCI_2022 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Intercommunalite_Metropole_au_01-01-2022.xlsx",
                                             sheet = "Composition_communale")
Fusion_2022_Pysique = Fusion_2022_Pysique %>% 
  left_join(Correspondance_EPCI_2022, by = "idcom")

Fusion_2022_Pysique <- Fusion_2022_Pysique %>%
  group_by(ID_Unique) %>%                     # Grouper par l'identifiant du propriétaire
  mutate(Multi = ifelse(n() > 1, 1, 0)) %>% # Identifier si le propriétaire a plusieurs logements
  ungroup()
mean(Fusion_2022_Pysique$Multi)
min(Fusion_2022_Pysique$Multi)
max(Fusion_2022_Pysique$Multi)
head(Fusion_2022_Pysique$Multi)

DF_Proprio_1 = Fusion_2022_Pysique %>%
  group_by(EPCI_2022, Multi) %>%
  summarise(Valeur_foncière_2022 = sum(Price),
            Proprio_2022 = n())%>%
  ungroup()

Ensemble_Prix = DF_Proprio_1 %>%
  group_by(EPCI_2022) %>% 
  mutate(Pct_Valo = (Valeur_foncière_2022[2]/(Valeur_foncière_2022[1]+Valeur_foncière_2022[2]))*100)
Ensemble_Prix = Ensemble_Prix[!duplicated(Ensemble_Prix$EPCI_2022),]
writexl::write_xlsx(Ensemble_Prix, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Multi_2022_EPCI.xlsx")


####2012####
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
nrow(Fusion_2012)
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
table(is.na(Fusion_2012$idcom_2022))/nrow(Fusion_2012)

Fusion_2012 = Fusion_2012 %>% ungroup %>%
  select(-idcom)
Fusion_2012 = Fusion_2012 %>%
  rename(idcom = idcom_2022)

####EPCI####
Correspondance_EPCI_2022 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Intercommunalite_Metropole_au_01-01-2022.xlsx",
                                             sheet = "Composition_communale")
Fusion_2012 = Fusion_2012 %>% 
  left_join(Correspondance_EPCI_2022, by = "idcom")

Ens_Prix_EPCI_1 = Fusion_2012 %>%
  group_by(EPCI_2022) %>%
  summarise(Valeur_foncière_2012 = sum(Price),
            NB = n())%>%
  ungroup()
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
writexl::write_xlsx(Ens_Prix_EPCI_1,"Valo_EPCI_2012.xlsx")

####% de K détenu par les multipropriétaires####
Fusion_2012_Pysique = Fusion_2012 %>%
  filter(Type_Proprio=="Personne physique",
         Age>=18, Age<=100)

Fusion_2012_Pysique <- Fusion_2012_Pysique %>%
  group_by(ID_Unique) %>%                     # Grouper par l'identifiant du propriétaire
  mutate(Multi = ifelse(n() > 1, 1, 0)) %>% # Identifier si le propriétaire a plusieurs logements
  ungroup()
mean(Fusion_2012_Pysique$Multi)

DF_Proprio_1 = Fusion_2012_Pysique %>% 
  group_by(EPCI_2022, Multi) %>% 
  summarise(Valeur_foncière_2012 = sum(Price),
            Proprio_2012 = n())%>% 
  ungroup()

Ensemble_Prix = DF_Proprio_1 %>%
  group_by(EPCI_2022) %>% 
  mutate(Pct_Valo = (Valeur_foncière_2012[2]/(Valeur_foncière_2012[1]+Valeur_foncière_2012[2]))*100)
Ensemble_Prix = Ensemble_Prix[!duplicated(Ensemble_Prix$EPCI_2022),]
writexl::write_xlsx(Ensemble_Prix, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Multi_2012_EPCI.xlsx")


####Fusion####
EPCI_2012 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_EPCI_2012.xlsx")
EPCI_2022 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_EPCI_2022.xlsx")

EPCI = inner_join(EPCI_2012, EPCI_2022, by = "EPCI_2022")                                             
writexl::write_xlsx(EPCI,"Valo_EPCI_2012-2022.xlsx")


####K des 65 ans et plus####
Fusion_2012_Pysique = Fusion_2012 %>%
  filter(Type_Proprio=="Personne physique",
         Age>=18, Age<=100)

Fusion_2022_Pysique = Fusion_2022 %>%
  filter(Type_Proprio=="Personne physique",
         Age>=18, Age<=100)

Fusion_2012_Pysique = Fusion_2012_Pysique %>%
  mutate(Age_Class = case_when(Age >=18&Age <=64 ~"18-64",
                               Age >=65 ~"65+"))
Fusion_2022_Pysique = Fusion_2022_Pysique %>%
  mutate(Age_Class = case_when(Age >=18&Age <=64 ~"18-64",
                               Age >=65 ~"65+"))

#2012
DF_Proprio_2012 = Fusion_2012_Pysique %>%
  group_by(Age_Class, EPCI_2022) %>%
  summarise(Valeur_foncière_2012 = sum(Price),
            Proprio_2012 = n())%>%
  ungroup()

Ensemble_Prix_2012 = DF_Proprio_2012 %>%
  group_by(EPCI_2022) %>% 
  mutate(Pct_Valo = (Valeur_foncière_2012[2]/(Valeur_foncière_2012[1]+Valeur_foncière_2012[2]))*100)
Ensemble_Prix_2012 = Ensemble_Prix_2012 %>%
  filter(Age_Class == "18-64")
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
writexl::write_xlsx(Ensemble_Prix_2012,"Valo_EPCI_K_2012.xlsx")

#2022
DF_Proprio_2022 = Fusion_2022_Pysique %>%
  group_by(Age_Class, EPCI_2022) %>%
  summarise(Valeur_foncière_2022 = sum(Price),
            Proprio_2022 = n())%>%
  ungroup()

Ensemble_Prix_2022 = DF_Proprio_2022 %>%
  group_by(EPCI_2022) %>% 
  mutate(Pct_Valo = (Valeur_foncière_2022[2]/(Valeur_foncière_2022[1]+Valeur_foncière_2022[2]))*100)
Ensemble_Prix_2022 = Ensemble_Prix_2022 %>%
  filter(Age_Class == "18-64")
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
writexl::write_xlsx(Ensemble_Prix_2022,"Valo_EPCI_K_2022.xlsx")

#Age dep
DF_Proprio_2012 = Fusion_2012_Pysique %>%
  group_by(Age, Dep) %>%
  summarise(Valeur_foncière_2012 = sum(Price),
            Proprio_2012 = n())%>%
  ungroup()
writexl::write_xlsx(DF_Proprio_2012,"Valo_DEP_K_2012.xlsx")


####Classe d'âge####
Fusion_2012_Pysique = Fusion_2012_Pysique %>%
  mutate(Age_Class = case_when(Age >=18&Age <=30 ~"18-30",
                               Age >=31&Age <=40 ~"31-40",
                               Age >=41&Age <=50 ~"41-50",
                               Age >=51&Age <=64 ~"51-64",
                               Age >=65~"65+"))

Fusion_2022_Pysique = Fusion_2022_Pysique %>%
  mutate(Age_Class = case_when(Age >=18&Age <=30 ~"18-30",
                               Age >=31&Age <=40 ~"31-40",
                               Age >=41&Age <=50 ~"41-50",
                               Age >=51&Age <=64 ~"51-64",
                               Age >=65~"65+"))

Fusion_Age_18 = Fusion_2022_Pysique %>%
  filter(Age_Class=="51-65") %>%
  group_by(EPCI_2022) %>%
  summarise(Patrimoine = sum(Price))
writexl::write_xlsx(Fusion_Age_18, 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_65+_EPCI_2022.xlsx')

France_2012 = Fusion_2012_Pysique %>%
  group_by(Age_Class) %>%
  summarise(Patrimoine = sum(Price))

France_2022 = Fusion_2022_Pysique %>%
  group_by(Age_Class) %>%
  summarise(Patrimoine = sum(Price))


#########################################################################
AGE2012 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_65+_EPCI_2012.xlsx")
AGE2012 = AGE2012 %>%
  rename(K_2012 = Patrimoine)
AGE2022 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_65+_EPCI_2022.xlsx")
AGE2022 = AGE2022 %>%
  rename(K_2022 = Patrimoine)
K_2012_2022 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_EPCI_2012-2022.xlsx")

AGEEPCI = AGE2012 %>% 
  inner_join(AGE2022, by = "EPCI_2022")%>%
  inner_join(K_2012_2022, by = "EPCI_2022")

AGEEPCI$K_Classe_Age_2012 = AGEEPCI$K_2012/AGEEPCI$Valeur_foncière_2012
AGEEPCI$K_Classe_Age_2022 = AGEEPCI$K_2022/AGEEPCI$Valeur_foncière_2022
AGEEPCI$Var_K = AGEEPCI$K_Classe_Age_2022-AGEEPCI$K_Classe_Age_2012
writexl::write_xlsx(AGEEPCI, 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Carte_65+_EPCI.xlsx')

Valo_K = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_EPCI_K_2012.xlsx")
Insee_Diff_Variations_EPCI = read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Insee_Diff_Variations_EPCI.xlsx")
Insee_Diff_Variations_EPCI = Insee_Diff_Variations_EPCI %>%
  select(EPCI_2022, Var_Part_Pers_65)
Valo_K = Valo_K %>%
  inner_join(Insee_Diff_Variations_EPCI, by = 'EPCI_2022')
Valo_K$Diff_Var_K = Valo_K$`VarK65+`-Valo_K$Var_Part_Pers_65
writexl::write_xlsx(Valo_K, 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Var_K_65+_EPCI.xlsx')
