rm(list=ls())
library(dplyr)
library(readr)

####Paris####
Local_75 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '75')
Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL/D75.csv")
colnames(Local)
Local$idlocal = as.character(Local$idlocal)
Local_75 <- Local_75 %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Fusion = left_join(Local, Local_75, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2012/R11_75.csv",row.names = F)


####Ile de France####
Local_77 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '77')
Local_78 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '78')
Local_91 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '91')
Local_92 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '92')
Local_93 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '93')
Local_94 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '94')
Local_95 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '95')

Local_Fusion = rbind(Local_77, Local_78, Local_91,
                     Local_92, Local_93, Local_94, Local_95)
Local_Longlat <- Local_Fusion %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL/R11.csv")
colnames(Local)
Local$idlocal = as.character(Local$idlocal)
Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2012/R11.csv",row.names = F)

####Centre val de Loire####
Local_18 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '18')
Local_28 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '28')
Local_36 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '36')
Local_37 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '37')
Local_41 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '41')
Local_45 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '45')

Local_Fusion = rbind(Local_18, Local_28, Local_36,
                     Local_37, Local_41, Local_45)
Local_Longlat <- Local_Fusion %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL/R24.csv")
colnames(Local)
Local$idlocal = as.character(Local$idlocal)
Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2012/R24.csv",row.names = F)


####Normandie####
Local_14 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '14')
Local_27 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '27')
Local_50 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '50')
Local_61 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '61')
Local_76 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '76')

Local_Fusion = rbind(Local_14, Local_27, Local_50,
                     Local_61, Local_76)
Local_Longlat <- Local_Fusion %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL/R28.csv")
colnames(Local)
Local$idlocal = as.character(Local$idlocal)
Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2012/R28.csv",row.names = F)

####Hauts de France####
Local_02 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '02')
Local_59 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '59')
Local_60 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '60')
Local_62 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '62')
Local_80 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '80')

Local_Fusion = rbind(Local_02, Local_59, Local_60,
                     Local_62, Local_80)
Local_Longlat <- Local_Fusion %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL/R32.csv")
colnames(Local)
Local$idlocal = as.character(Local$idlocal)
Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2012/R32.csv",row.names = F)

####Grand Est####
Local_08 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '08')
Local_10 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '10')
Local_51 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '51')
Local_52 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '52')
Local_54 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '54')
Local_55 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '55')
Local_57 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '57')
Local_67 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '67')
Local_68 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '68')
Local_88 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '88')
Local_Fusion = rbind(Local_08, Local_10, Local_51, Local_52, Local_54,
                     Local_55, Local_57, Local_67, Local_68, Local_88)
Local_Longlat <- Local_Fusion %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)
min(Local_Longlat$Longitude)
Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL/R44.csv")
colnames(Local)
Local$idlocal = as.character(Local$idlocal)
Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2012/R44.csv",row.names = F)

####Pays de la loire####
Local_44 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '44')
Local_49 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '49')
Local_53 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '53')
Local_72 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '72')
Local_85 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '85')

Local_Fusion = rbind(Local_44, Local_49, Local_53,
                     Local_72, Local_85)
Local_Longlat <- Local_Fusion %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL/R52.csv")
colnames(Local)
Local$idlocal = as.character(Local$idlocal)
Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2012/R52.csv",row.names = F)


####Bretagne####
Local_22 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '22')
Local_29 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '29')
Local_35 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '35')
Local_56 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '56')

Local_Fusion = rbind(Local_22, Local_29, Local_35,
                     Local_56)
Local_Longlat <- Local_Fusion %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL/R53.csv")
colnames(Local)
Local$idlocal = as.character(Local$idlocal)
Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2012/R53.csv",row.names = F)

#####Bourgogne Franche Comté####
Local_21 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '21')
Local_25 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '25')
Local_39 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '39')
Local_58 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '58')
Local_70 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '70')
Local_71 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '71')
Local_89 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '89')
Local_90 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '90')

Local_Fusion = rbind(Local_21, Local_25, Local_39,
                     Local_58, Local_70, Local_71,
                     Local_89, Local_90)
Local_Longlat <- Local_Fusion %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL/R27.csv")
colnames(Local)
Local$idlocal = as.character(Local$idlocal)
Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2012/R27.csv",row.names = F)

#####Nouvelle Aquitaine####
Local_16 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '16')
Local_17 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '17')
Local_19 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '19')
Local_23 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '23')
Local_24 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '24')
Local_33 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '33')
Local_40 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '40')
Local_47 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '47')
Local_64 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '64')
Local_79 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '79')
Local_86 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '86')
Local_87 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '87')

Local_Fusion = rbind(Local_16, Local_17, Local_19,
                     Local_23, Local_24, Local_33,
                     Local_40, Local_47, Local_64,
                     Local_79, Local_86, Local_87)
Local_Longlat <- Local_Fusion %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL/R75.csv")
colnames(Local)
Local$idlocal = as.character(Local$idlocal)
Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2012/R75.csv",row.names = F)

#####Occitanie####
Local_09 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '09')
Local_11 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '11')
Local_12 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '12')
Local_30 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '30')
Local_31 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '31')
Local_32 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '32')
Local_34 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '34')
Local_46 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '46')
Local_48 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '48')
Local_65 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '65')
Local_66 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '66')
Local_81 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '81')
Local_82 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '82')

Local_Fusion = rbind(Local_09, Local_11, Local_12,
                     Local_30, Local_31, Local_32,
                     Local_34, Local_46, Local_48,
                     Local_65, Local_66, Local_81,
                     Local_82)
Local_Longlat <- Local_Fusion %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL/R76.csv")
colnames(Local)
Local$idlocal = as.character(Local$idlocal)
Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2012/R76.csv",row.names = F)

#####Rhône Alpes####
Local_01 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R84',
                       layer = '01')
Local_03 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R84',
                       layer = '03')
Local_07 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R84',
                       layer = '07')
Local_15 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R84',
                       layer = '15')
Local_26 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R84',
                       layer = '26')
Local_38 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R84',
                       layer = '38')
Local_42 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R84',
                       layer = '42')
Local_43 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R84',
                       layer = '43')
Local_63 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R84',
                       layer = '63')
Local_69 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R84',
                       layer = '69')
Local_73 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R84',
                       layer = '73')
Local_74 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R84',
                       layer = '74')

Local_Fusion = rbind(Local_01, Local_03, Local_07,
                     Local_15, Local_26, Local_38,
                     Local_42, Local_43, Local_63,
                     Local_69, Local_73, Local_74)
Local_Fusion = Local_Fusion %>% filter(dteloc <= 2)%>%
  select(-dteloc)

Local_Longlat <- Local_Fusion %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2019/CSV/R84/LOCAL.csv")
colnames(Local)
Local$idlocal = as.character(Local$idlocal)
table(Local$dteloc)

Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2019/R84.csv",row.names = F)

####PACA####
Local_04 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '04')
Local_05 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '05')
Local_06 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '06')
Local_13 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '13')
Local_83 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '83')
Local_84 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '84')

Local_Fusion = rbind(Local_04, Local_05, Local_06,
                     Local_13, Local_83, Local_84)
Local_Longlat <- Local_Fusion %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL/R93.csv")
Local$idlocal = as.character(Local$idlocal)
Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2012/R93.csv",row.names = F)

####Corse####
Local_2A = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '2A')
Local_2B = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '2B')

Local_Fusion = rbind(Local_2A, Local_2B)
Local_Longlat <- Local_Fusion %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL/R94.csv")
Local$idlocal = as.character(Local$idlocal)
Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2012/R94.csv",row.names = F)

####Guadeloupe####
Local_971 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                       layer = '971')

Local_Longlat <- Local_971 %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL/R01.csv")
colnames(Local)
Local$idlocal = as.character(Local$idlocal)
Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2012/R01.csv",row.names = F)

####Martinique####
Local_972 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                        layer = '972')

Local_Longlat <- Local_972 %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL/R02.csv")
colnames(Local)
Local$idlocal = as.character(Local$idlocal)
Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2012/R02.csv",row.names = F)

####La Réunion####
Local_974 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL',
                        layer = '974')

Local_Longlat <- Local_974 %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2012/LOCAL/R04.csv")
colnames(Local)
Local$idlocal = as.character(Local$idlocal)
Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2012/R04.csv",row.names = F)

##################################################################
Local_75 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '75')
Local_Longlat <- Local_75 %>% tidyr::extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE)

Local <- readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL/R11.csv")
Local$idlocal = as.character(Local$idlocal)
Local$Dep = substr(Local$idcom, start = 1, stop = 2)
Local = Local %>% filter(Dep==75)

Fusion = left_join(Local, Local_Longlat, by = 'idlocal')
Fusion = Fusion %>% select(-idlocal)
Fusion = Fusion[!is.na(Fusion$Longitude),]
min(Fusion$Longitude)
min(Fusion$Latitude)
max(Fusion$Longitude)
max(Fusion$Latitude)
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Input prédictions/2022/R11_75.csv",row.names = F)


Local_971 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = 'd971')
Local_972 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '25')
Local_973 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '973')
Local_974 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Fichiers fonciers/2022/LOCAL',
                       layer = '974')


###############################
 
#####################################################################
Fusion_Alsace_Moselle <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_Predict_R44_Prix_Proprio.csv")
Fusion_Alsace_Moselle$Dep = substr(Fusion_Alsace_Moselle$idcom, start = 1, stop = 2)
table(Fusion_Alsace_Moselle$Dep)

Alsace_Lorraine_PM2_App = readxl::read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Prix communes Alsace Moselle.xlsx',
                                sheet = 'Appartements_2019')
Alsace_Lorraine_PM2_App = Alsace_Lorraine_PM2_App %>% select(idcom, Ens)

Alsace_Lorraine_PM2_Mais = readxl::read_excel('C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Prix communes Alsace Moselle.xlsx',
                                             sheet = 'Maisons_2019')
Alsace_Lorraine_PM2_Mais = Alsace_Lorraine_PM2_Mais %>% select(idcom, Ens)


Fusion_Alsace_Moselle_App = Fusion_Alsace_Moselle %>%
  filter(Dep == 57|Dep == 67|Dep == 68,
         dteloc==2)
Fusion_Alsace_Moselle_App = left_join(Fusion_Alsace_Moselle_App, Alsace_Lorraine_PM2_App, by = 'idcom')

Fusion_Alsace_Moselle_Mais = Fusion_Alsace_Moselle %>%
  filter(Dep == 57|Dep == 67|Dep == 68,
         dteloc==1)
Fusion_Alsace_Moselle_Mais = left_join(Fusion_Alsace_Moselle_Mais, Alsace_Lorraine_PM2_Mais, by = 'idcom')


Fusion_Alsace_Moselle = rbind(Fusion_Alsace_Moselle_App, Fusion_Alsace_Moselle_Mais)

Fusion_Alsace_Moselle = Fusion_Alsace_Moselle %>% 
  select(-Dep)%>%
  rename(Predicted_price_sq_m = Ens)

write.csv(Fusion_Alsace_Moselle,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Bases prédites/2019/Fusion_predict_Alsace_Moselle.csv",row.names = F)
