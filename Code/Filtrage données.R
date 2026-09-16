rm(list=ls())
library(dplyr)
library(readr)
library(tidyverse)
Local <- read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/Local_d971_d974.csv")
Mut_971 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV',
                  layer = 'Mutation_d971')
Mut_972 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV',
                      layer = 'Mutation_d972')
Mut_973 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV',
                      layer = 'Mutation_d973')
Mut_974 = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV',
                      layer = 'Mutation_d974')
Mut = rbind(Mut_971, Mut_972, Mut_973, Mut_974)


Mut = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV',
                              layer = 'Mutation_d61_d80')
colnames(Mut)
Mut = Mut %>% filter(nblocmut == 1)%>%
  select(-nblocmut)
Mut <- Mut %>% extract(geometry, c('Longitude', 'Latitude'), '\\((.*), (.*)\\)', convert = TRUE) 
Fusion = left_join(Mut, Local, by = 'idmutation')
Fusion$valeurfonc = as.numeric(Fusion$valeurfonc)
Fusion = Fusion[!is.na(Fusion$idloc),]
Fusion = Fusion[!is.na(Fusion$valeurfonc),]
Fusion$pm2 = Fusion$valeurfonc/Fusion$ffshab
Fusion = Fusion %>% filter(pm2 >=100, ffshab >= 9,ffshab <= 1000,
                                      ffancst>0, pm2 <=50000)
Fusion$datemut1 = lubridate::ymd(Fusion$datemut)
Fusion = Fusion %>% mutate(dateannee = case_when(datemut1<as.Date('2011-01-01')~"2010",
                                                 datemut1 >= as.Date('2011-01-01')
                                                 & datemut1 < as.Date('2012-01-01') ~ "2011",
                                                 datemut1 >= as.Date('2012-01-01')
                                                 & datemut1 < as.Date('2013-01-01') ~ "2012",
                                                 datemut1 >= as.Date('2013-01-01')
                                                 & datemut1 < as.Date('2014-01-01') ~ "2013",
                                                 datemut1 >= as.Date('2014-01-01')
                                                 & datemut1 < as.Date('2015-01-01') ~ "2014",
                                                 datemut1 >= as.Date('2015-01-01')
                                                 & datemut1 < as.Date('2016-01-01') ~ "2015",
                                                 datemut1 >= as.Date('2016-01-01')
                                                 & datemut1 < as.Date('2017-01-01') ~ "2016",
                                                 datemut1 >= as.Date('2017-01-01')
                                                 & datemut1 < as.Date('2018-01-01') ~ "2017",
                                                 datemut1 >= as.Date('2018-01-01')
                                                 & datemut1 < as.Date('2019-01-01') ~ "2018",
                                                 datemut1 >= as.Date('2019-01-01')
                                                 & datemut1 < as.Date('2020-01-01') ~ "2019",
                                                 datemut1 >= as.Date('2020-01-01')
                                                 & datemut1 < as.Date('2021-01-01') ~ "2020",
                                                 datemut1 >= as.Date('2021-01-01')
                                                 & datemut1 < as.Date('2022-01-01') ~ "2021",
                                                 datemut1 >=as.Date('2022-01-01') ~ "2022"))
Fusion$ffcodinsee = as.character(Fusion$ffcodinsee)
Fusion = Fusion %>%
  group_by(dateannee, ffcodinsee)%>%
  mutate(Q1=quantile(pm2,probs=0.25), Q3 = quantile(pm2,probs=0.75),
         IQR = Q3-Q1)%>%
  filter(pm2 >= Q1-1.5*IQR,
         pm2 <= Q3+1.5*IQR)%>%
  ungroup()
write.csv(Fusion,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/Fusion_d971_d974.csv",row.names = F)

