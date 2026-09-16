rm(list=ls())
library(dplyr)
library(ggplot2)
Fusion_Predict_Dens_0 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_Dens_Proprio_0.csv")
Fusion_Predict_Dens_1 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_Dens_Proprio_1.csv")
Fusion_Predict_Dens_2 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_Dens_Proprio_2.csv")
Fusion_Predict_Dens_3 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_Dens_Proprio_3.csv")
Fusion_Predict_Dens_4 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_Dens_Proprio_4.csv")
Fusion_Predict_Dens_5 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_Dens_Proprio_5.csv")
Fusion_Predict_Dens_6_7 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2022/Fusion_Predict_Dens_Proprio_6_7.csv")

####Statistiques descriptives####
Fusion = rbind(Fusion_Predict_Dens_0, Fusion_Predict_Dens_1, Fusion_Predict_Dens_2,
               Fusion_Predict_Dens_3, Fusion_Predict_Dens_4, Fusion_Predict_Dens_5,
               Fusion_Predict_Dens_6_7)
rm(Fusion_Predict_Dens_0, Fusion_Predict_Dens_1, Fusion_Predict_Dens_2, 
   Fusion_Predict_Dens_3, Fusion_Predict_Dens_4, Fusion_Predict_Dens_5,
   Fusion_Predict_Dens_6_7)
#Âge moyen des propriétaires
round(mean(Fusion$Age, na.rm = T),0)#58 ans
ggplot(Fusion, aes(x = Age), color = "black") +
  geom_histogram()+
  theme_classic()+
  theme(text=element_text(size = 22,family="serif"),
        axis.text.x = element_text(vjust = +0.6, angle = 0,size = 22,color = "gray22"),
        axis.text.y = element_text(size = 24,color = "black"),
        axis.title.y = element_text(vjust = +1.5),
        panel.grid.major.y = element_line(color = "gray22",
                                          linewidth = 0.5,
                                          linetype = 2),
        panel.grid.major.x = element_line(color = "black",
                                          linewidth = 0.2,
                                          linetype = 2),
        legend.text = element_text(size=20),
        legend.position="bottom")+
  scale_y_continuous(labels=function(x) format(x, big.mark = " ", scientific = FALSE))+
  xlab('')+
  ylab('')
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Graphiques")
ggsave("Répartition_Age_2022.jpeg", units="in", width=14, height=10)
writexl::write_xlsx(Nb_Ventes,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Graphiques/Nombre de ventes par unité urbaine.xlsx")

colnames(Fusion)
Age_Moyen_Commune = Fusion %>%
  group_by(idcom)%>%
  summarise(Age_Moyen = mean(Age, na.rm = T),
            Age_Median = median(Age, na.rm = T),
            Prix_Median = median(Predicted_price, na.rm = T))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Cartes")
writexl::write_xlsx(Age_Moyen_Commune, "Répartition_Age_Prix_2022.xlsx")

Age_Moyen_Commune_Mais_App = Fusion %>%
  group_by(idcom, dteloc)%>%
  summarise(Age_Moyen = mean(Age, na.rm = T),
            Age_Median = median(Age, na.rm = T),
            Prix_Median = median(Predicted_price, na.rm = T))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Cartes")
writexl::write_xlsx(Age_Moyen_Commune, "Répartition_Age_Prix_2022_Appart_Mais.xlsx")