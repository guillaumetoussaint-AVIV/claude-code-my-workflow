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

Correspondance_EPCI_2022 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Intercommunalite_Metropole_au_01-01-2022.xlsx",
                                             sheet = "Composition_communale")

Fusion_2022 = Fusion_2022 %>% 
  left_join(Correspondance_EPCI_2022, by = "idcom")

table(is.na(Fusion_2022$EPCI_2022))/nrow(Fusion_2022)

Fusion_2022_Pysique = Fusion_2022 %>%
  filter(Type_Proprio=="Personne physique",
         Age>=18, Age<=100)

Fusion_2022_Pysique = Fusion_2022_Pysique %>%
  mutate(Age_Class = case_when(Age >=18&Age <=30 ~"18-30",
                               Age >=31&Age <=40 ~"31-40",
                               Age >=41&Age <=50 ~"41-50",
                               Age >=51&Age <=64 ~"51-64",
                               Age >64~"64+"))

Fusion_Age_18 = Fusion_2022_Pysique %>%
  filter(Age_Class=="18-30") %>%
  group_by(EPCI_2022) %>%
  summarise(Patrimoine = sum(Price),
            Patrimoine_per_ind_mean = mean(Price),
            Patrimoine_per_ind_D1 = quantile(Price, probs = 0.1),
            Patrimoine_per_ind_D2 = quantile(Price, probs = 0.2),
            Patrimoine_per_ind_D3 = quantile(Price, probs = 0.3),
            Patrimoine_per_ind_D4 = quantile(Price, probs = 0.4),
            Patrimoine_per_ind_D5 = quantile(Price, probs = 0.5),
            Patrimoine_per_ind_D6 = quantile(Price, probs = 0.6),
            Patrimoine_per_ind_D7 = quantile(Price, probs = 0.7),
            Patrimoine_per_ind_D8 = quantile(Price, probs = 0.8),
            Patrimoine_per_ind_D9 = quantile(Price, probs = 0.9),
            Sum_Pers = n())

Fusion_Age_31 = Fusion_2022_Pysique %>%
  filter(Age_Class=="31-40") %>%
  group_by(EPCI_2022) %>%
  summarise(Patrimoine = sum(Price),
            Patrimoine_per_ind_mean = mean(Price),
            Patrimoine_per_ind_D1 = quantile(Price, probs = 0.1),
            Patrimoine_per_ind_D2 = quantile(Price, probs = 0.2),
            Patrimoine_per_ind_D3 = quantile(Price, probs = 0.3),
            Patrimoine_per_ind_D4 = quantile(Price, probs = 0.4),
            Patrimoine_per_ind_D5 = quantile(Price, probs = 0.5),
            Patrimoine_per_ind_D6 = quantile(Price, probs = 0.6),
            Patrimoine_per_ind_D7 = quantile(Price, probs = 0.7),
            Patrimoine_per_ind_D8 = quantile(Price, probs = 0.8),
            Patrimoine_per_ind_D9 = quantile(Price, probs = 0.9),
            Sum_Pers = n())

Fusion_Age_41 = Fusion_2022_Pysique %>%
  filter(Age_Class=="41-50") %>%
  group_by(EPCI_2022) %>%
  summarise(Patrimoine = sum(Price),
            Patrimoine_per_ind_mean = mean(Price),
            Patrimoine_per_ind_D1 = quantile(Price, probs = 0.1),
            Patrimoine_per_ind_D2 = quantile(Price, probs = 0.2),
            Patrimoine_per_ind_D3 = quantile(Price, probs = 0.3),
            Patrimoine_per_ind_D4 = quantile(Price, probs = 0.4),
            Patrimoine_per_ind_D5 = quantile(Price, probs = 0.5),
            Patrimoine_per_ind_D6 = quantile(Price, probs = 0.6),
            Patrimoine_per_ind_D7 = quantile(Price, probs = 0.7),
            Patrimoine_per_ind_D8 = quantile(Price, probs = 0.8),
            Patrimoine_per_ind_D9 = quantile(Price, probs = 0.9),
            Sum_Pers = n())

Fusion_Age_51 = Fusion_2022_Pysique %>%
  filter(Age_Class=="51-64") %>%
  group_by(EPCI_2022) %>%
  summarise(Patrimoine = sum(Price),
            Patrimoine_per_ind_mean = mean(Price),
            Patrimoine_per_ind_D1 = quantile(Price, probs = 0.1),
            Patrimoine_per_ind_D2 = quantile(Price, probs = 0.2),
            Patrimoine_per_ind_D3 = quantile(Price, probs = 0.3),
            Patrimoine_per_ind_D4 = quantile(Price, probs = 0.4),
            Patrimoine_per_ind_D5 = quantile(Price, probs = 0.5),
            Patrimoine_per_ind_D6 = quantile(Price, probs = 0.6),
            Patrimoine_per_ind_D7 = quantile(Price, probs = 0.7),
            Patrimoine_per_ind_D8 = quantile(Price, probs = 0.8),
            Patrimoine_per_ind_D9 = quantile(Price, probs = 0.9),
            Sum_Pers = n())

Fusion_Age_64 = Fusion_2022_Pysique %>%
  filter(Age_Class=="64+") %>%
  group_by(EPCI_2022) %>%
  summarise(Patrimoine = sum(Price),
            Patrimoine_per_ind_mean = mean(Price),
            Patrimoine_per_ind_D1 = quantile(Price, probs = 0.1),
            Patrimoine_per_ind_D2 = quantile(Price, probs = 0.2),
            Patrimoine_per_ind_D3 = quantile(Price, probs = 0.3),
            Patrimoine_per_ind_D4 = quantile(Price, probs = 0.4),
            Patrimoine_per_ind_D5 = quantile(Price, probs = 0.5),
            Patrimoine_per_ind_D6 = quantile(Price, probs = 0.6),
            Patrimoine_per_ind_D7 = quantile(Price, probs = 0.7),
            Patrimoine_per_ind_D8 = quantile(Price, probs = 0.8),
            Patrimoine_per_ind_D9 = quantile(Price, probs = 0.9),
            Sum_Pers = n())

Fusion_Ens = Fusion_2022_Pysique %>%
  group_by(EPCI_2022) %>%
  summarise(Patrimoine = sum(Price),
            Patrimoine_per_ind_mean = mean(Price),
            Patrimoine_per_ind_D1 = quantile(Price, probs = 0.1),
            Patrimoine_per_ind_D2 = quantile(Price, probs = 0.2),
            Patrimoine_per_ind_D3 = quantile(Price, probs = 0.3),
            Patrimoine_per_ind_D4 = quantile(Price, probs = 0.4),
            Patrimoine_per_ind_D5 = quantile(Price, probs = 0.5),
            Patrimoine_per_ind_D6 = quantile(Price, probs = 0.6),
            Patrimoine_per_ind_D7 = quantile(Price, probs = 0.7),
            Patrimoine_per_ind_D8 = quantile(Price, probs = 0.8),
            Patrimoine_per_ind_D9 = quantile(Price, probs = 0.9),
            Sum_Pers = n())

writexl::write_xlsx(Fusion_Age_18,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_18.xlsx")
writexl::write_xlsx(Fusion_Age_31,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_31.xlsx")
writexl::write_xlsx(Fusion_Age_41,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_41.xlsx")
writexl::write_xlsx(Fusion_Age_51,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_51.xlsx")
writexl::write_xlsx(Fusion_Age_64,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_64.xlsx")
writexl::write_xlsx(Fusion_Ens,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Ens.xlsx")

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

Correspondance_EPCI_2022 = readxl::read_xlsx("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Intercommunalite_Metropole_au_01-01-2022.xlsx",
                                             sheet = "Composition_communale")

Fusion_2012 = Fusion_2012 %>% 
  left_join(Correspondance_EPCI_2022, by = "idcom")
table(is.na(Fusion_2012$EPCI_2022))/nrow(Fusion_2012)

Fusion_2012 = Fusion_2012 %>%
  mutate(Type_Proprio = case_when(grepl("05",typprop ) ~ "Logement social",
                                  grepl("10",typprop ) ~ "Investisseur privé",
                                  grepl("20",typprop ) ~ "Personne physique",
                                  TRUE ~"Autre"))

Fusion_2012_Pysique = Fusion_2012 %>%
  filter(Type_Proprio=="Personne physique",
         Age>=18, Age<=100)

Fusion_2012_Pysique = Fusion_2012_Pysique %>%
  mutate(Age_Class = case_when(Age >=18&Age <=30 ~"18-30",
                               Age >=31&Age <=40 ~"31-40",
                               Age >=41&Age <=50 ~"41-50",
                               Age >=51&Age <=64 ~"51-64",
                               Age >64~"64+"))

Fusion_Age_18 = Fusion_2012_Pysique %>%
  filter(Age_Class=="18-30") %>%
  group_by(EPCI_2022) %>%
  summarise(Patrimoine = sum(Price),
            Patrimoine_per_ind_mean = mean(Price),
            Patrimoine_per_ind_D1 = quantile(Price, probs = 0.1),
            Patrimoine_per_ind_D2 = quantile(Price, probs = 0.2),
            Patrimoine_per_ind_D3 = quantile(Price, probs = 0.3),
            Patrimoine_per_ind_D4 = quantile(Price, probs = 0.4),
            Patrimoine_per_ind_D5 = quantile(Price, probs = 0.5),
            Patrimoine_per_ind_D6 = quantile(Price, probs = 0.6),
            Patrimoine_per_ind_D7 = quantile(Price, probs = 0.7),
            Patrimoine_per_ind_D8 = quantile(Price, probs = 0.8),
            Patrimoine_per_ind_D9 = quantile(Price, probs = 0.9),
            Sum_Pers = n())

Fusion_Age_31 = Fusion_2012_Pysique %>%
  filter(Age_Class=="31-40") %>%
  group_by(EPCI_2022) %>%
  summarise(Patrimoine = sum(Price),
            Patrimoine_per_ind_mean = mean(Price),
            Patrimoine_per_ind_D1 = quantile(Price, probs = 0.1),
            Patrimoine_per_ind_D2 = quantile(Price, probs = 0.2),
            Patrimoine_per_ind_D3 = quantile(Price, probs = 0.3),
            Patrimoine_per_ind_D4 = quantile(Price, probs = 0.4),
            Patrimoine_per_ind_D5 = quantile(Price, probs = 0.5),
            Patrimoine_per_ind_D6 = quantile(Price, probs = 0.6),
            Patrimoine_per_ind_D7 = quantile(Price, probs = 0.7),
            Patrimoine_per_ind_D8 = quantile(Price, probs = 0.8),
            Patrimoine_per_ind_D9 = quantile(Price, probs = 0.9),
            Sum_Pers = n())

Fusion_Age_41 = Fusion_2012_Pysique %>%
  filter(Age_Class=="41-50") %>%
  group_by(EPCI_2022) %>%
  summarise(Patrimoine = sum(Price),
            Patrimoine_per_ind_mean = mean(Price),
            Patrimoine_per_ind_D1 = quantile(Price, probs = 0.1),
            Patrimoine_per_ind_D2 = quantile(Price, probs = 0.2),
            Patrimoine_per_ind_D3 = quantile(Price, probs = 0.3),
            Patrimoine_per_ind_D4 = quantile(Price, probs = 0.4),
            Patrimoine_per_ind_D5 = quantile(Price, probs = 0.5),
            Patrimoine_per_ind_D6 = quantile(Price, probs = 0.6),
            Patrimoine_per_ind_D7 = quantile(Price, probs = 0.7),
            Patrimoine_per_ind_D8 = quantile(Price, probs = 0.8),
            Patrimoine_per_ind_D9 = quantile(Price, probs = 0.9),
            Sum_Pers = n())

Fusion_Age_51 = Fusion_2012_Pysique %>%
  filter(Age_Class=="51-64") %>%
  group_by(EPCI_2022) %>%
  summarise(Patrimoine = sum(Price),
            Patrimoine_per_ind_mean = mean(Price),
            Patrimoine_per_ind_D1 = quantile(Price, probs = 0.1),
            Patrimoine_per_ind_D2 = quantile(Price, probs = 0.2),
            Patrimoine_per_ind_D3 = quantile(Price, probs = 0.3),
            Patrimoine_per_ind_D4 = quantile(Price, probs = 0.4),
            Patrimoine_per_ind_D5 = quantile(Price, probs = 0.5),
            Patrimoine_per_ind_D6 = quantile(Price, probs = 0.6),
            Patrimoine_per_ind_D7 = quantile(Price, probs = 0.7),
            Patrimoine_per_ind_D8 = quantile(Price, probs = 0.8),
            Patrimoine_per_ind_D9 = quantile(Price, probs = 0.9),
            Sum_Pers = n())

Fusion_Age_64 = Fusion_2012_Pysique %>%
  filter(Age_Class=="64+") %>%
  group_by(EPCI_2022) %>%
  summarise(Patrimoine = sum(Price),
            Patrimoine_per_ind_mean = mean(Price),
            Patrimoine_per_ind_D1 = quantile(Price, probs = 0.1),
            Patrimoine_per_ind_D2 = quantile(Price, probs = 0.2),
            Patrimoine_per_ind_D3 = quantile(Price, probs = 0.3),
            Patrimoine_per_ind_D4 = quantile(Price, probs = 0.4),
            Patrimoine_per_ind_D5 = quantile(Price, probs = 0.5),
            Patrimoine_per_ind_D6 = quantile(Price, probs = 0.6),
            Patrimoine_per_ind_D7 = quantile(Price, probs = 0.7),
            Patrimoine_per_ind_D8 = quantile(Price, probs = 0.8),
            Patrimoine_per_ind_D9 = quantile(Price, probs = 0.9),
            Sum_Pers = n())

Fusion_Ens = Fusion_2012_Pysique %>%
  group_by(EPCI_2022) %>%
  summarise(Patrimoine = sum(Price),
            Patrimoine_per_ind_mean = mean(Price),
            Patrimoine_per_ind_D1 = quantile(Price, probs = 0.1),
            Patrimoine_per_ind_D2 = quantile(Price, probs = 0.2),
            Patrimoine_per_ind_D3 = quantile(Price, probs = 0.3),
            Patrimoine_per_ind_D4 = quantile(Price, probs = 0.4),
            Patrimoine_per_ind_D5 = quantile(Price, probs = 0.5),
            Patrimoine_per_ind_D6 = quantile(Price, probs = 0.6),
            Patrimoine_per_ind_D7 = quantile(Price, probs = 0.7),
            Patrimoine_per_ind_D8 = quantile(Price, probs = 0.8),
            Patrimoine_per_ind_D9 = quantile(Price, probs = 0.9),
            Sum_Pers = n())

writexl::write_xlsx(Fusion_Age_18,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_18_2012.xlsx")
writexl::write_xlsx(Fusion_Age_31,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_31_2012.xlsx")
writexl::write_xlsx(Fusion_Age_41,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_41_2012.xlsx")
writexl::write_xlsx(Fusion_Age_51,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_51_2012.xlsx")
writexl::write_xlsx(Fusion_Age_64,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_64_2012.xlsx")
writexl::write_xlsx(Fusion_Ens,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Ens_2012.xlsx")



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



#### Fusion valorisation EPCI####
EPCI_18_30_2012 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_18-30_EPCI_2012.xlsx")
EPCI_18_30_2022 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_18-30_EPCI_2022.xlsx")

EPCI_31_40_2012 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_31-40_EPCI_2012.xlsx")
EPCI_31_40_2022 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_31-40_EPCI_2022.xlsx")

EPCI_41_50_2012 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_41-50_EPCI_2012.xlsx")
EPCI_41_50_2022 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_41-50_EPCI_2022.xlsx")

EPCI_51_65_2012 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_51-65_EPCI_2012.xlsx")
EPCI_51_65_2022 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_51-65_EPCI_2022.xlsx")

EPCI_65_2012 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_65+_EPCI_2012.xlsx")
EPCI_65_2022 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Age_65+_EPCI_2022.xlsx")

EPCI_K_2012 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_EPCI_K_2012.xlsx")
EPCI_K_2022 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_EPCI_K_2022.xlsx")

EPCI_Fusion = EPCI_18_30_2012 %>%
  left_join(EPCI_18_30_2022, by = "EPCI_2022") %>%
  left_join(EPCI_31_40_2012, by = "EPCI_2022") %>%
  left_join(EPCI_31_40_2022, by = "EPCI_2022") %>%
  left_join(EPCI_41_50_2012, by = "EPCI_2022") %>%
  left_join(EPCI_41_50_2022, by = "EPCI_2022") %>%
  left_join(EPCI_51_65_2012, by = "EPCI_2022") %>%
  left_join(EPCI_51_65_2022, by = "EPCI_2022") %>%
  left_join(EPCI_65_2012, by = "EPCI_2022") %>%
  left_join(EPCI_65_2022, by = "EPCI_2022")

writexl::write_xlsx(EPCI_Fusion, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/EPCI_Fusion.xlsx")


#### Fusion nouvelles bases ####
rm(list=ls())
Fusion_Age_18_2012 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_18_2012.xlsx")
Fusion_Age_31_2012 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_31_2012.xlsx")
Fusion_Age_41_2012 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_41_2012.xlsx")
Fusion_Age_51_2012 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_51_2012.xlsx")
Fusion_Age_64_2012 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_64_2012.xlsx")
Fusion_Age_ENS_2012 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Ens_2012.xlsx")

Fusion_2012 = Fusion_Age_18_2012 %>%
  left_join(Fusion_Age_31_2012, by = "EPCI_2022") %>%
  left_join(Fusion_Age_41_2012, by = "EPCI_2022") %>%
  left_join(Fusion_Age_51_2012, by = "EPCI_2022") %>%
  left_join(Fusion_Age_64_2012, by = "EPCI_2022") %>%
  left_join(Fusion_Age_ENS_2012, by = "EPCI_2022")


Fusion_Age_18 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_18.xlsx")
Fusion_Age_31 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_31.xlsx")
Fusion_Age_41 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_41.xlsx")
Fusion_Age_51 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_51.xlsx")
Fusion_Age_64 = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Age_64.xlsx")
Fusion_Age_ENS = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/Fusion_Ens.xlsx")

Fusion_2022 = Fusion_Age_18 %>%
  left_join(Fusion_Age_31, by = "EPCI_2022") %>%
  left_join(Fusion_Age_41, by = "EPCI_2022") %>%
  left_join(Fusion_Age_51, by = "EPCI_2022") %>%
  left_join(Fusion_Age_64, by = "EPCI_2022") %>%
  left_join(Fusion_Age_ENS, by = "EPCI_2022")

writexl::write_xlsx(Fusion_2012,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/BDD_Fusion_2012_EPCI.xlsx")
writexl::write_xlsx(Fusion_2022,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats_V2/BDD_Fusion_2022_EPCI.xlsx")