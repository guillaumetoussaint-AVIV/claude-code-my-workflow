rm(list=ls())
library(dplyr)
library(readr)
library(ggplot2)
Paris <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Paris_Prix_Proprio.csv")
Fusion_Predict_Dens_R11 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R11_Prix_Proprio.csv")
Fusion_Predict_Dens_R11 = Fusion_Predict_Dens_R11 %>% select(-Nom)
Fusion_Predict_Dens_R24 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R24_Prix_Proprio.csv")
Fusion_Predict_Dens_R24 = Fusion_Predict_Dens_R24 %>% select(-Nom)
Fusion_Predict_Dens_R27 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R27_Prix_Proprio.csv")
Fusion_Predict_Dens_R27 = Fusion_Predict_Dens_R27 %>% select(-Nom)
Fusion_Predict_Dens_R28 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R28_Prix_Proprio.csv")
Fusion_Predict_Dens_R28 = Fusion_Predict_Dens_R28 %>% select(-Nom)
Fusion_Predict_Dens_R32 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R32_Prix_Proprio.csv")
Fusion_Predict_Dens_R44 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R44_Prix_Proprio.csv")
Fusion_Predict_Dens_R44 = Fusion_Predict_Dens_R44 %>% select(-Nom)
Fusion_Predict_Dens_R52 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R52_Prix_Proprio.csv")
Fusion_Predict_Dens_R52 = Fusion_Predict_Dens_R52 %>% select(-Nom)
Fusion_Predict_Dens_R53 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R53_Prix_Proprio.csv")
Fusion_Predict_Dens_R53 = Fusion_Predict_Dens_R53 %>% select(-Nom)
Fusion_Predict_Dens_R75 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R75_Prix_Proprio.csv")
Fusion_Predict_Dens_R75 = Fusion_Predict_Dens_R75 %>% select(-Nom)
Fusion_Predict_Dens_R76 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R76_Prix_Proprio.csv")
Fusion_Predict_Dens_R76 = Fusion_Predict_Dens_R76 %>% select(-Nom)
Fusion_Predict_Dens_R84 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R84_Prix_Proprio.csv")
Fusion_Predict_Dens_R93 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R93_Prix_Proprio.csv")
Fusion_Predict_Dens_R94 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R94_Prix_Proprio.csv")

colnames(Fusion_Predict_Dens_R11)
colnames(Fusion_Predict_Dens_R32)
####Statistiques descriptives####
Fusion = rbind(Paris, Fusion_Predict_Dens_R11, Fusion_Predict_Dens_R24, Fusion_Predict_Dens_R27,
               Fusion_Predict_Dens_R28, Fusion_Predict_Dens_R32, Fusion_Predict_Dens_R44,
               Fusion_Predict_Dens_R52, Fusion_Predict_Dens_R53,
               Fusion_Predict_Dens_R75, Fusion_Predict_Dens_R76,
               Fusion_Predict_Dens_R84, Fusion_Predict_Dens_R93, Fusion_Predict_Dens_R94)
rm(Paris, Fusion_Predict_Dens_R11, Fusion_Predict_Dens_R24, Fusion_Predict_Dens_R27,
   Fusion_Predict_Dens_R28, Fusion_Predict_Dens_R32, Fusion_Predict_Dens_R44,
   Fusion_Predict_Dens_R52,Fusion_Predict_Dens_R53, 
   Fusion_Predict_Dens_R75, Fusion_Predict_Dens_R76,
   Fusion_Predict_Dens_R84, Fusion_Predict_Dens_R93, Fusion_Predict_Dens_R94)
colnames(Fusion)

Age_Moyen_Commune = Fusion %>%
  group_by(idcom)%>%
  summarise(Prix_Median = median(Predicted_price, na.rm = T))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Cartes")
writexl::write_xlsx(Age_Moyen_Commune, "Prix_2022.xlsx")

Age_Moyen_Commune_Mais_App = Fusion %>%
  group_by(idcom, dteloc)%>%
  summarise(Age_Moyen = mean(Age, na.rm = T),
            Age_Median = median(Age, na.rm = T),
            Prix_Median = median(Predicted_price, na.rm = T))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Cartes")
writexl::write_xlsx(Age_Moyen_Commune, "Répartition_Age_Prix_2022_Appart_Mais.xlsx")

options(digits = 8)
sum(Fusion$Predicted_price)
mean(Fusion$Predicted_price)

####Valeur totale par département####
Fusion$Dep = substr(Fusion$idcom, start = 1, stop = 2)
Age_Moyen_Commune_Mais_App = Fusion %>%
  group_by(Dep)%>%
  summarise(Valorisation = sum(Predicted_price, na.rm = T))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Statistiques descriptives")
writexl::write_xlsx(Age_Moyen_Commune_Mais_App, "Valeur_par_département.xlsx")

Fusion$Dep = substr(Fusion$idcom, start = 1, stop = 2)
Fusion = Fusion %>% mutate(Age_2 = case_when(Age>=80~80,
                                             Age<=25~25,
                                             TRUE~Age))
table(is.na(Fusion$Age))

Age_Moyen_Commune_Mais_App = Fusion %>%
  group_by(Dep, Age)%>%
  summarise(Valorisation = sum(Predicted_price, na.rm = T))%>%
  filter(Age<=99,
         Age>=25)
Age_Moyen_Commune_Mais_App = Age_Moyen_Commune_Mais_App[!is.na(Age_Moyen_Commune_Mais_App$Age),]
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Statistiques descriptives")
writexl::write_xlsx(Age_Moyen_Commune_Mais_App, "Valeur_par_département_par_âge.xlsx")
