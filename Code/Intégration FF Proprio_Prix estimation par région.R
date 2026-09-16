rm(list=ls())
library(dplyr)
library(readr)
library(ggplot2)
####Fusion Prix_Propriétaires####
Fusion_Predict_Dens_R11 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_11.csv")
R11 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R11_Treated.csv")
Fusion_Predict_Dens_R11 = left_join(Fusion_Predict_Dens_R11, R11,
                                    by = 'idprocpte')
colnames(Fusion_Predict_Dens_R11)
write.csv(Fusion_Predict_Dens_R11, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R11_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R24 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_24.csv")
R24 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R24_Treated.csv")
Fusion_Predict_Dens_R24 = left_join(Fusion_Predict_Dens_R24, R24,
                                    by = 'idprocpte')
colnames(Fusion_Predict_Dens_R24)
Fusion_Predict_Dens_R24 = Fusion_Predict_Dens_R24 %>% select(-`...1`)
write.csv(Fusion_Predict_Dens_R24, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R24_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R27 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_27.csv")
R27 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R27_Treated.csv")
Fusion_Predict_Dens_R27 = left_join(Fusion_Predict_Dens_R27, R27,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R27, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R27_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R28 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_28.csv")
R28 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R28_Treated.csv")
Fusion_Predict_Dens_R28 = left_join(Fusion_Predict_Dens_R28, R28,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R28, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R28_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R32 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_32.csv")
R32 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R32_Treated.csv")
Fusion_Predict_Dens_R32 = left_join(Fusion_Predict_Dens_R32, R32,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R32, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R32_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R44 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_44.csv")
R44 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R44_Treated.csv")
Fusion_Predict_Dens_R44 = left_join(Fusion_Predict_Dens_R44, R44,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R44, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R44_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R52 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_52.csv")
R52 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R52_Treated.csv")
Fusion_Predict_Dens_R52 = left_join(Fusion_Predict_Dens_R52, R52,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R52, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R52_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R53 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_53.csv")
colnames(Fusion_Predict_Dens_R53)
R53 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R53_Treated.csv")
Fusion_Predict_Dens_R53 = left_join(Fusion_Predict_Dens_R53, R53,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R53, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R53_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R75 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_75.csv")
R75 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R75_Treated.csv")
Fusion_Predict_Dens_R75 = left_join(Fusion_Predict_Dens_R75, R75,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R75, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R75_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R76 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_76.csv")
R76 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R76_Treated.csv")
Fusion_Predict_Dens_R76 = left_join(Fusion_Predict_Dens_R76, R76,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R76, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R76_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R84 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_84.csv")
R84 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R84_Treated.csv")
Fusion_Predict_Dens_R84 = left_join(Fusion_Predict_Dens_R84, R84,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R84, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R84_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R93 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_93.csv")
R93 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R93_Treated.csv")
Fusion_Predict_Dens_R93 = left_join(Fusion_Predict_Dens_R93, R93,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R93, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R93_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R94 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_94.csv")
R94 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R94_Treated.csv")
Fusion_Predict_Dens_R94 = left_join(Fusion_Predict_Dens_R94, R94,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R94, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R94_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Paris <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_Paris.csv")
R11 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R11_Treated.csv")
Fusion_Predict_Paris = left_join(Fusion_Predict_Paris, R11,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Paris, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_Paris_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R01 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_01.csv")
R01 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R01_Treated.csv")
Fusion_Predict_Dens_R01 = left_join(Fusion_Predict_Dens_R01, R01,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R01, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R01_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R02 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_02.csv")
R02 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R02_Treated.csv")
Fusion_Predict_Dens_R02 = left_join(Fusion_Predict_Dens_R02, R02,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R02, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R02_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R04 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_R_04.csv")
R04 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R04_Treated.csv")
Fusion_Predict_Dens_R04 = left_join(Fusion_Predict_Dens_R04, R04,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R04, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R04_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_RAM <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_Alsace_Moselle.csv")
RAM <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R44_Treated.csv")
Fusion_Predict_Dens_RAM = left_join(Fusion_Predict_Dens_RAM, RAM,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_RAM, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_RAM_Prix_Proprio.csv",
          row.names=FALSE)

####2012####
Fusion_Predict_Dens_R11 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_R_11.csv")
R11 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R11_Treated.csv")
Fusion_Predict_Dens_R11 = left_join(Fusion_Predict_Dens_R11, R11,
                                    by = 'idprocpte')
colnames(Fusion_Predict_Dens_R11)
write.csv(Fusion_Predict_Dens_R11, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R11_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R24 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_R_24.csv")
R24 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R24_Treated.csv")
Fusion_Predict_Dens_R24 = left_join(Fusion_Predict_Dens_R24, R24,
                                    by = 'idprocpte')
colnames(Fusion_Predict_Dens_R24)
Fusion_Predict_Dens_R24 = Fusion_Predict_Dens_R24 %>% select(-`...1`)
write.csv(Fusion_Predict_Dens_R24, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R24_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R27 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_R_27.csv")
R27 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R27_Treated.csv")
Fusion_Predict_Dens_R27 = left_join(Fusion_Predict_Dens_R27, R27,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R27, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R27_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R28 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_R_28.csv")
R28 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R28_Treated.csv")
D27 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/D27_Treated.csv")
R28 = rbind(R28, D27)
Fusion_Predict_Dens_R28 = left_join(Fusion_Predict_Dens_R28, R28,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R28, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R28_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R32 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_R_32.csv")
R32 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R32_Treated.csv")
Fusion_Predict_Dens_R32 = left_join(Fusion_Predict_Dens_R32, R32,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R32, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R32_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R44 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_R_44.csv")
R44 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R44_Treated.csv")
Fusion_Predict_Dens_R44 = left_join(Fusion_Predict_Dens_R44, R44,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R44, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R44_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R52 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_R_52.csv")
R52 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R52_Treated.csv")
Fusion_Predict_Dens_R52 = left_join(Fusion_Predict_Dens_R52, R52,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R52, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R52_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R53 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_R_53.csv")
colnames(Fusion_Predict_Dens_R53)
R53 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R53_Treated.csv")
Fusion_Predict_Dens_R53 = left_join(Fusion_Predict_Dens_R53, R53,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R53, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R53_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R75 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_R_75.csv")
R75 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R75_Treated.csv")
Fusion_Predict_Dens_R75 = left_join(Fusion_Predict_Dens_R75, R75,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R75, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R75_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R76 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_R_76.csv")
R76 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R76_Treated.csv")
Fusion_Predict_Dens_R76 = left_join(Fusion_Predict_Dens_R76, R76,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R76, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R76_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R84 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_R_84.csv")
R84 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R84_Treated.csv")
Fusion_Predict_Dens_R84 = left_join(Fusion_Predict_Dens_R84, R84,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R84, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R84_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R93 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_R_93.csv")
R93 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R93_Treated.csv")
Fusion_Predict_Dens_R93 = left_join(Fusion_Predict_Dens_R93, R93,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R93, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R93_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R94 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_R_94.csv")
R94 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R94_Treated.csv")
Fusion_Predict_Dens_R94 = left_join(Fusion_Predict_Dens_R94, R94,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R94, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R94_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Paris <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_Paris.csv")
R11 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/Paris_Treated.csv")
Fusion_Predict_Paris = left_join(Fusion_Predict_Paris, R11,
                                 by = 'idprocpte')
write.csv(Fusion_Predict_Paris, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_Paris_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R01 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_R_01.csv")
R01 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R01_Treated.csv")
Fusion_Predict_Dens_R01 = left_join(Fusion_Predict_Dens_R01, R01,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R01, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R01_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R02 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_R_02.csv")
R02 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R02_Treated.csv")
Fusion_Predict_Dens_R02 = left_join(Fusion_Predict_Dens_R02, R02,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R02, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R02_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_R04 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_R_04.csv")
R04 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R04_Treated.csv")
Fusion_Predict_Dens_R04 = left_join(Fusion_Predict_Dens_R04, R04,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_R04, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_R04_Prix_Proprio.csv",
          row.names=FALSE)

Fusion_Predict_Dens_RAM <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_predict_Alsace_Moselle.csv")
RAM <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R44_Treated.csv")
Fusion_Predict_Dens_RAM = left_join(Fusion_Predict_Dens_RAM, RAM,
                                    by = 'idprocpte')
write.csv(Fusion_Predict_Dens_RAM, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2012/Fusion_Predict_RAM_Prix_Proprio.csv",
          row.names=FALSE)
