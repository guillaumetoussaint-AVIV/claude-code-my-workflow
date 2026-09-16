rm(list=ls())
library(dplyr)
R52 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_R52_Prix_Proprio.csv")
R52$Price = exp(R52$Predicted_price_sq_m)*R52$stoth
colnames(R52)

R52_Age = R52 %>% group_by(Age) %>%
  summarise(Somme = sum(Price))%>%
  filter(Age<=100, Age >=18)
plot(R52_Age$Age, R52_Age$Somme, type = 'l')
writexl::write_xlsx(R52_Age, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Répartition_Age_Patrimoine_R52.xlsx")


R52_Date_Achat = R52 %>% group_by(jdatatan) %>%
  filter(Age<=100, Age >=18,
         jdatatan>=1970)%>%
  summarise(Somme = sum(Price))
plot(R52_Date_Achat$jdatatan, R52_Date_Achat$Somme, type = 'l')
writexl::write_xlsx(R52_Date_Achat, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Répartition_Date_achat_Patrimoine_R52.xlsx")

sum(R52$Price)
table(R52$catpro3)
R52_Social = R52 %>% filter(catpro3 == "F1a")
nrow(R52_Social)/nrow(R52)#11.04%
sum(R52_Social$Price)/sum(R52$Price)#8.38%
