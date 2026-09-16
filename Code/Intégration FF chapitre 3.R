rm(list=ls())
library(dplyr)
library(readr)
#Propriétaires
#R11
R11 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/PROPRIETAIRE/R11.csv")
colnames(R11)
library(data.table)
library(lubridate)
R11$Date_Naissance = dmy(R11$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R11$Age = age(R11$Date_Naissance, "2022-10-01")
R11$ID_Unique = with(R11, paste(dnomus, dprnus,
                                  Date_Naissance))
head(R11$ID_Unique)
R11 = R11 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R11, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/PROPRIETAIRE/R11_Treated.csv",
          row.names=FALSE)
#R24
R24 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R24/PROPRIETAIRE.csv")
colnames(R24)
library(data.table)
library(lubridate)
R24$Date_Naissance = dmy(R24$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R24$Age = age(R24$Date_Naissance, "2022-10-01")
R24$ID_Unique = with(R24, paste(dnomus, dprnus,
                                Date_Naissance))
head(R24$ID_Unique)
R24 = R24 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R24, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R24_Treated.csv",
          row.names=FALSE)

#R27
R27 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R27/PROPRIETAIRE.csv")
colnames(R27)
library(data.table)
library(lubridate)
R27$Date_Naissance = dmy(R27$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R27$Age = age(R27$Date_Naissance, "2022-10-01")
R27$ID_Unique = with(R27, paste(dnomus, dprnus,
                                Date_Naissance))
head(R27$ID_Unique)
R27 = R27 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R27, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R27_Treated.csv",
          row.names=FALSE)

#R28
R28 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R28/PROPRIETAIRE.csv")
colnames(R28)
library(data.table)
library(lubridate)
R28$Date_Naissance = dmy(R28$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R28$Age = age(R28$Date_Naissance, "2022-10-01")
R28$ID_Unique = with(R28, paste(dnomus, dprnus,
                                Date_Naissance))
head(R28$ID_Unique)
R28 = R28 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R28, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R28.csv",
          row.names=FALSE)

#R32
R32 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R32/PROPRIETAIRE.csv")
colnames(R32)
library(data.table)
library(lubridate)
R32$Date_Naissance = dmy(R32$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R32$Age = age(R32$Date_Naissance, "2022-10-01")
R32$ID_Unique = with(R32, paste(dnomus, dprnus,
                                Date_Naissance))
head(R32$ID_Unique)
R32 = R32 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R32, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R32.csv",
          row.names=FALSE)

#R44
R44 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R44/PROPRIETAIRE.csv")
colnames(R44)
library(data.table)
library(lubridate)
R44$Date_Naissance = dmy(R44$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R44$Age = age(R44$Date_Naissance, "2022-10-01")
R44$ID_Unique = with(R44, paste(dnomus, dprnus,
                                Date_Naissance))
head(R44$ID_Unique)
R44 = R44 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R44, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R44.csv",
          row.names=FALSE)

#R52
R52 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R52/PROPRIETAIRE.csv")
colnames(R52)
library(data.table)
library(lubridate)
R52$Date_Naissance = dmy(R52$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R52$Age = age(R52$Date_Naissance, "2022-10-01")
R52$ID_Unique = with(R52, paste(dnomus, dprnus,
                                Date_Naissance))
head(R52$ID_Unique)
R52 = R52 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R52, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R52_Treated.csv",
          row.names=FALSE)

#R53
R53 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R53/PROPRIETAIRE.csv")
colnames(R53)
library(data.table)
library(lubridate)
R53$Date_Naissance = dmy(R53$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R53$Age = age(R53$Date_Naissance, "2022-10-01")
R53$ID_Unique = with(R53, paste(dnomus, dprnus,
                                Date_Naissance))
head(R53$ID_Unique)
R53 = R53 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R53, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R53.csv",
          row.names=FALSE)

#R75
R75 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R75/PROPRIETAIRE.csv")
colnames(R75)
library(data.table)
library(lubridate)
R75$Date_Naissance = dmy(R75$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R75$Age = age(R75$Date_Naissance, "2022-10-01")
R75$ID_Unique = with(R75, paste(dnomus, dprnus,
                                Date_Naissance))
head(R75$ID_Unique)
R75 = R75 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R75, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R75.csv",
          row.names=FALSE)

#R76
R76 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R76/PROPRIETAIRE.csv")
colnames(R76)
library(data.table)
library(lubridate)
R76$Date_Naissance = dmy(R76$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R76$Age = age(R76$Date_Naissance, "2022-10-01")
R76$ID_Unique = with(R76, paste(dnomus, dprnus,
                                Date_Naissance))
head(R76$ID_Unique)
R76 = R76 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R76, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/PROPRIETAIRE/R76.csv",
          row.names=FALSE)

#R84
R84 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R84/PROPRIETAIRE.csv")
colnames(R84)
library(data.table)
library(lubridate)
R84$Date_Naissance = dmy(R84$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R84$Age = age(R84$Date_Naissance, "2022-10-01")
R84$ID_Unique = with(R84, paste(dnomus, dprnus,
                                Date_Naissance))
head(R84$ID_Unique)
R84 = R84 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R84, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R84_Treated.csv",
          row.names=FALSE)

#R93
R93 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R93/PROPRIETAIRE.csv")
colnames(R93)
library(data.table)
library(lubridate)
R93$Date_Naissance = dmy(R93$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R93$Age = age(R93$Date_Naissance, "2022-10-01")
R93$ID_Unique = with(R93, paste(dnomus, dprnus,
                                Date_Naissance))
head(R93$ID_Unique)
R93 = R93 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R93, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R93_Treated.csv",
          row.names=FALSE)

#R94
R94 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R94/PROPRIETAIRE.csv")
colnames(R94)
library(data.table)
library(lubridate)
R94$Date_Naissance = dmy(R94$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R94$Age = age(R94$Date_Naissance, "2022-10-01")
R94$ID_Unique = with(R94, paste(dnomus, dprnus,
                                Date_Naissance))
head(R94$ID_Unique)
R94 = R94 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R94, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R94_Treated.csv",
          row.names=FALSE)

#R01
R01 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R01.csv")
colnames(R01)
library(data.table)
library(lubridate)
R01$Date_Naissance = dmy(R01$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R01$Age = age(R01$Date_Naissance, "2022-10-01")
R01$ID_Unique = with(R01, paste(dnomus, dprnus,
                                Date_Naissance))
head(R01$ID_Unique)
R01 = R01 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R01, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R01_Treated.csv",
          row.names=FALSE)

#R02
R02 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R02.csv")
colnames(R02)
library(data.table)
library(lubridate)
R02$Date_Naissance = dmy(R02$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R02$Age = age(R02$Date_Naissance, "2022-10-01")
R02$ID_Unique = with(R02, paste(dnomus, dprnus,
                                Date_Naissance))
head(R02$ID_Unique)
R02 = R02 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R02, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R02_Treated.csv",
          row.names=FALSE)

#R04
R04 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R04.csv")
colnames(R04)
library(data.table)
library(lubridate)
R04$Date_Naissance = dmy(R04$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R04$Age = age(R04$Date_Naissance, "2022-10-01")
R04$ID_Unique = with(R04, paste(dnomus, dprnus,
                                Date_Naissance))
head(R04$ID_Unique)
R04 = R04 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R04, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/PROPRIETAIRE/R04_Treated.csv",
          row.names=FALSE)

###########################2012##########################
#Propriétaires
#R11
R11 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R11.csv")
colnames(R11)
library(data.table)
library(lubridate)
R11$Date_Naissance = dmy(R11$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R11$Age = age(R11$Date_Naissance, "2012-10-01")
colnames(R11)
R11$ID_Unique = with(R11, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R11$ID_Unique)
R11 = R11 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R11, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R11_Treated.csv",
          row.names=FALSE)
#R24
R24 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R24.csv")
colnames(R24)
library(data.table)
library(lubridate)
R24$Date_Naissance = dmy(R24$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R24$Age = age(R24$Date_Naissance, "2012-10-01")
R24$ID_Unique = with(R24, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R24$ID_Unique)
R24 = R24 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R24, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R24_Treated.csv",
          row.names=FALSE)

#R27
R27 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R27.csv")
colnames(R27)
library(data.table)
library(lubridate)
R27$Date_Naissance = dmy(R27$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R27$Age = age(R27$Date_Naissance, "2012-10-01")
R27$ID_Unique = with(R27, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R27$ID_Unique)
R27 = R27 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R27, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R27_Treated.csv",
          row.names=FALSE)

#R28
R28 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R28.csv")
colnames(R28)
library(data.table)
library(lubridate)
R28$Date_Naissance = dmy(R28$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R28$Age = age(R28$Date_Naissance, "2012-10-01")
R28$ID_Unique = with(R28, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R28$ID_Unique)
R28 = R28 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R28, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R28_Treated.csv",
          row.names=FALSE)

#R32
R32 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R32.csv")
colnames(R32)
library(data.table)
library(lubridate)
R32$Date_Naissance = dmy(R32$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R32$Age = age(R32$Date_Naissance, "2012-10-01")
R32$ID_Unique = with(R32, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R32$ID_Unique)
R32 = R32 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R32, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R32_Treated.csv",
          row.names=FALSE)

#R44
R44 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R44.csv")
colnames(R44)
library(data.table)
library(lubridate)
R44$Date_Naissance = dmy(R44$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R44$Age = age(R44$Date_Naissance, "2012-10-01")
R44$ID_Unique = with(R44, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R44$ID_Unique)
R44 = R44 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R44, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R44_Treated.csv",
          row.names=FALSE)

#R52
R52 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R52.csv")
colnames(R52)
library(data.table)
library(lubridate)
R52$Date_Naissance = dmy(R52$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R52$Age = age(R52$Date_Naissance, "2012-10-01")
R52$ID_Unique = with(R52, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R52$ID_Unique)
R52 = R52 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R52, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R52_Treated.csv",
          row.names=FALSE)

#R53
R53 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R53.csv")
colnames(R53)
library(data.table)
library(lubridate)
R53$Date_Naissance = dmy(R53$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R53$Age = age(R53$Date_Naissance, "2012-10-01")
R53$ID_Unique = with(R53, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R53$ID_Unique)
R53 = R53 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R53, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R53_Treated.csv",
          row.names=FALSE)

#R75
R75 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R75.csv")
colnames(R75)
library(data.table)
library(lubridate)
R75$Date_Naissance = dmy(R75$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R75$Age = age(R75$Date_Naissance, "2012-10-01")
R75$ID_Unique = with(R75, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R75$ID_Unique)
R75 = R75 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R75, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R75_Treated.csv",
          row.names=FALSE)

#R76
R76 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R76.csv")
colnames(R76)
library(data.table)
library(lubridate)
R76$Date_Naissance = dmy(R76$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R76$Age = age(R76$Date_Naissance, "2012-10-01")
R76$ID_Unique = with(R76, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R76$ID_Unique)
R76 = R76 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R76, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R76_Treated.csv",
          row.names=FALSE)

#R84
R84 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R84.csv")
colnames(R84)
library(data.table)
library(lubridate)
R84$Date_Naissance = dmy(R84$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R84$Age = age(R84$Date_Naissance, "2012-10-01")
R84$ID_Unique = with(R84, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R84$ID_Unique)
R84 = R84 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R84, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R84_Treated.csv",
          row.names=FALSE)

#R93
R93 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R93.csv")
colnames(R93)
library(data.table)
library(lubridate)
R93$Date_Naissance = dmy(R93$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R93$Age = age(R93$Date_Naissance, "2012-10-01")
R93$ID_Unique = with(R93, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R93$ID_Unique)
R93 = R93 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R93, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R93_Treated.csv",
          row.names=FALSE)

#R94
R94 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R94.csv")
colnames(R94)
library(data.table)
library(lubridate)
R94$Date_Naissance = dmy(R94$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R94$Age = age(R94$Date_Naissance, "2012-10-01")
R94$ID_Unique = with(R94, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R94$ID_Unique)
R94 = R94 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R94, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R94_Treated.csv",
          row.names=FALSE)

#R01
R01 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R01.csv")
colnames(R01)
library(data.table)
library(lubridate)
R01$Date_Naissance = dmy(R01$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R01$Age = age(R01$Date_Naissance, "2012-10-01")
R01$ID_Unique = with(R01, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R01$ID_Unique)
R01 = R01 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R01, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R01_Treated.csv",
          row.names=FALSE)

#R02
R02 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R02.csv")
colnames(R02)
library(data.table)
library(lubridate)
R02$Date_Naissance = dmy(R02$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R02$Age = age(R02$Date_Naissance, "2012-10-01")
R02$ID_Unique = with(R02, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R02$ID_Unique)
R02 = R02 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R02, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R02_Treated.csv",
          row.names=FALSE)

#R04
R04 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R04.csv")
colnames(R04)
library(data.table)
library(lubridate)
R04$Date_Naissance = dmy(R04$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R04$Age = age(R04$Date_Naissance, "2012-10-01")
R04$ID_Unique = with(R04, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R04$ID_Unique)
R04 = R04 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R04, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/R04_Treated.csv",
          row.names=FALSE)

#D27
R04 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/D27.csv")
colnames(R04)
library(data.table)
library(lubridate)
R04$Date_Naissance = dmy(R04$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R04$Age = age(R04$Date_Naissance, "2012-10-01")
R04$ID_Unique = with(R04, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R04$ID_Unique)
R04 = R04 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R04, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/D27_Treated.csv",
          row.names=FALSE)

#Paris
R11 <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/Paris.csv")
colnames(R11)
library(data.table)
library(lubridate)
R11$Date_Naissance = dmy(R11$jdatnss)
age <- function(birth, base = Sys.Date()){
  i <- interval(birth, base)
  p <- as.period(i)
  year(p)
}
R11$Age = age(R11$Date_Naissance, "2012-10-01")
R11$ID_Unique = with(R11, paste(dnomlp, dprnlp,
                                Date_Naissance))
head(R11$ID_Unique)
R11 = R11 %>% select(idprocpte, dldnss, ID_Unique,
                     Age, dqualp)
write.csv(R11, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/PROPRIETAIRE/Paris_Treated.csv",
          row.names=FALSE)
