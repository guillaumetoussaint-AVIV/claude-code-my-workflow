rm(list=ls())
library(dplyr)
Local_R11 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R11_LOCAL.csv")
MUT_R11 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R11_MUT.csv")
FusionR11 = left_join(MUT_R11, Local_R11, by = "idmutation")
Local_R24 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R24_LOCAL.csv")
MUT_R24 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R24_MUT.csv")
FusionR24 = left_join(MUT_R24, Local_R24, by = "idmutation")
Local_R27 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R27_LOCAL.csv")
MUT_R27 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R27_MUT.csv")
FusionR27 = left_join(MUT_R27, Local_R27, by = "idmutation")
Local_R28 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R28_LOCAL.csv")
MUT_R28 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R28_MUT.csv")
FusionR28 = left_join(MUT_R28, Local_R28, by = "idmutation")
Local_R32 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R32_LOCAL.csv")
MUT_R32 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R32_MUT.csv")
FusionR32 = left_join(MUT_R32, Local_R32, by = "idmutation")
Local_R44 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R44_LOCAL.csv")
MUT_R44 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R44_MUT.csv")
FusionR44 = left_join(MUT_R44, Local_R44, by = "idmutation")
Local_R52 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R52_LOCAL.csv")
MUT_R52 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R52_MUT.csv")
FusionR52 = left_join(MUT_R52, Local_R52, by = "idmutation")
Local_R53 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R53_LOCAL.csv")
MUT_R53 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R53_MUT.csv")
FusionR53 = left_join(MUT_R53, Local_R53, by = "idmutation")
Local_R75 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R75_LOCAL.csv")
MUT_R75 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R75_MUT.csv")
FusionR75 = left_join(MUT_R75, Local_R75, by = "idmutation")
Local_R76 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R76_LOCAL.csv")
MUT_R76 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R76_MUT.csv")
FusionR76 = left_join(MUT_R76, Local_R76, by = "idmutation")
Local_R84 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R84_LOCAL.csv")
MUT_R84 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R84_MUT.csv")
FusionR84 = left_join(MUT_R84, Local_R84, by = "idmutation")
Local_R93 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R93_LOCAL.csv")
MUT_R93 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R93_MUT.csv")
FusionR93 = left_join(MUT_R93, Local_R93, by = "idmutation")
Local_R94 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R94_LOCAL.csv")
MUT_R94 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/R94_MUT.csv")
FusionR94 = left_join(MUT_R94, Local_R94, by = "idmutation")


Local_ROM = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/ROM_LOCAL.csv")
MUT_ROM = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/ROM_MUT.csv")
FusionROM = left_join(MUT_ROM, Local_ROM, by = "idmutation")

Fusion = rbind(FusionR11,FusionR24,FusionR27,FusionR28,FusionR32,
               FusionR44,FusionR52,FusionR53,FusionR75,FusionR76,
               FusionR84,FusionR93,FusionR94,FusionROM)

Fusion$valeurfonc = as.numeric(Fusion$valeurfonc)
Fusion = Fusion[!is.na(Fusion$valeurfonc),]
Fusion = Fusion[!duplicated(Fusion$idmutation),]
Fusion = Fusion %>% filter(valeurfonc >100, ffshab >8)
colnames(Fusion)
Fusion = Fusion %>% mutate(dateannee = case_when(datemut >= as.Date('2012-01-01')
                                                 & datemut < as.Date('2013-01-01') ~ "2012",
                                                 datemut >= as.Date('2013-01-01')
                                                 & datemut < as.Date('2014-01-01') ~ "2013",
                                                 datemut >= as.Date('2014-01-01')
                                                 & datemut < as.Date('2015-01-01') ~ "2014",
                                                 datemut >= as.Date('2015-01-01')
                                                 & datemut < as.Date('2016-01-01') ~ "2015",
                                                 datemut >= as.Date('2016-01-01')
                                                 & datemut < as.Date('2017-01-01') ~ "2016",
                                                 datemut >= as.Date('2017-01-01')
                                                 & datemut < as.Date('2018-01-01') ~ "2017",
                                                 datemut >= as.Date('2018-01-01')
                                                 & datemut < as.Date('2019-01-01') ~ "2018",
                                                 datemut >= as.Date('2019-01-01')
                                                 & datemut < as.Date('2020-01-01') ~ "2019",
                                                 datemut >= as.Date('2020-01-01')
                                                 & datemut < as.Date('2021-01-01') ~ "2020",
                                                 datemut >= as.Date('2021-01-01')
                                                 & datemut < as.Date('2022-01-01') ~ "2021",
                                                 datemut >= as.Date('2022-01-01')
                                                 & datemut < as.Date('2023-01-01') ~ "2022"))
Fusion = Fusion %>% 
  filter(datemut>=as.Date("2012-01-01"))%>%
  group_by(dateannee,ffcodinsee)%>%
  mutate(Q1=quantile(valeurfonc,probs=0.25), Q3 = quantile(valeurfonc,probs=0.75),
         IQR = Q3-Q1)%>%
  ungroup()%>%
  filter(valeurfonc > Q1-1.5*IQR,
         valeurfonc < Q3+1.5*IQR)%>%
  select(-Q1,-Q3,-IQR)%>%
  mutate(cstperiod = case_when(ffancst<1853~"Avant 1853",
                               ffancst>=1853&ffancst<=1870~"1853-1870",
                               ffancst>=1871&ffancst<=1948~"1871-1948",
                               ffancst>=1949&ffancst<=1974~"1949-1974",
                               ffancst>=1975&ffancst<=1981~"1975-1989",
                               ffancst>=1990&ffancst<=1998~"1990-1998",
                               ffancst>=1999&ffancst<=2010~"1999-2010",
                               ffancst>=2011~"Après 2010",
                               TRUE ~"NA"))%>%
  mutate(nb_piece = case_when(ffnbpprinc == 1 ~ "1 pièce",
                              ffnbpprinc >= 1 & ffnbpprinc <= 2 ~ "2 pièces",
                              ffnbpprinc >= 3 & ffnbpprinc <= 4 ~ "3 pièces",
                              ffnbpprinc >= 4~ "4 pièces et plus"))%>%
  mutate(maison = case_when(ffctyploc == 2 ~ 1,
                            ffctyploc ==1 ~ 0))
  

Fusion$terrasse_oui = ifelse(Fusion$ffnbpterra >=1,1,0)
Fusion$garage_oui = ifelse(Fusion$ffnbpgarag >=1,1,0)
Fusion$piscine_oui = ifelse(Fusion$ffnbppisci >=1,1,0)
Fusion$logement_social = as.numeric(Fusion$fflogsoc)
Fusion$etage_RDC = ifelse(Fusion$ffetage ==0,1,0)
Fusion$etage_1_3 = ifelse(Fusion$ffetage >=1&Fusion$ffetage<=3,1,0)
Fusion$etage_4_6 = ifelse(Fusion$ffetage >=4&Fusion$ffetage<=6,1,0)
Fusion$etage_7 = ifelse(Fusion$ffetage >=7,1,0)

colnames(Fusion)
Fusion = Fusion %>% select(valeurfonc,dateannee,cstperiod,etage_RDC,etage_1_3,etage_4_6,
                           etage_7,ffshab,nb_piece,terrasse_oui,garage_oui,
                           piscine_oui,logement_social,maison,ffvalloc,ffnbpann,long,lat)

write.csv2(Fusion, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 3 valorisation/Données/DV3F/DV3F_CSV/DV3F_FINAL/Fusion.csv",
           row.names = F)
