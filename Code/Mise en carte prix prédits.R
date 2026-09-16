rm(list=ls())
library(dplyr)
library(readr)
Fusion_predict_R_24 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_predict_R_52.csv")
Fusion_predict_R_24$Predicted_Price_sq_m_1 = exp(Fusion_predict_R_24$Predicted_price_sq_m)
Fusion_predict_R_24$Predicted_Price = Fusion_predict_R_24$Predicted_Price_sq_m_1*Fusion_predict_R_24$stoth
mean(Fusion_predict_R_24$Predicted_Price)

Fusion_Prix = Fusion_predict_R_24 %>%
  group_by(idcom)%>%
  summarise(Price_sq_m = round(median(Predicted_Price_sq_m_1),2),
            Price = round(median(Predicted_Price),2))
writexl::write_xlsx(Fusion_Prix,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Cartes/Prix_prédits_R52_2022.xlsx")

Indice_IRL <- read_excel("C:/Users/guill/Indice_IRL.xlsx")
Indice_IRL = Indice_IRL[!is.na(Indice_IRL$gr_medianPriceM2),]
Indices_Structures = Indice_IRL %>% 
  group_by(date) %>%
  summarise(Moyenne_Croissance = weighted.mean(wma4_medianPriceM2, sum4_count, na.rm = T))
writexl::write_xlsx(Indices_Structures,"C:/Users/guill/Indice_IRL_évolution.xlsx")
