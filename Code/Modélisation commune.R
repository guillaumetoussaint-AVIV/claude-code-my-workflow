####Modélisation Multiproprio Commune####
rm(list=ls())
library(dplyr)
BDD_GWR_Diff <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Comm_Diff_Var.xlsx")
Multi_Diff <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Multi_Diff_Var.xlsx")
Insee_Indicateurs_Diff <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Insee_Diff_Variations.xlsx")
Loi_Litt <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/typo_loilitt.xlsx")
Valo_Communes <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valo_Commune_2022.xlsx")
OLDDEP <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Var_OLDDEP_Commune_Final.xlsx")
UU <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Unité urbaine INSEE.xlsx")
APL <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/apl.xlsx")

UU$UU = as.factor(UU$UU)

BDD_GWR_Diff = BDD_GWR_Diff %>%
  left_join(Insee_Indicateurs_Diff, by = "idcom") %>%
  left_join(Valo_Communes, by = "idcom") %>%
  left_join(Multi_Diff, by = "idcom") %>%
  left_join(Loi_Litt, by = 'idcom')%>%
  left_join(OLDDEP, by = 'idcom')%>%
  left_join(UU, by = 'idcom')%>%
  left_join(APL, by = 'idcom')

#writexl::write_xlsx(BDD_GWR_Diff, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Base_Finale_Modélisation.xlsx")
rm(list=ls())
BDD_GWR_Diff_0 <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Base_Finale_Modélisation.xlsx")
BDD_GWR_Diff_1 <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Rev_Med_2010_2021.xlsx")
BDD_GWR_Diff_2 <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/FUA.xlsx")
BDD_GWR_Diff_3 <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Commuting zone.xlsx")
BDD_GWR_Diff_4 <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/Rural_Urbain_INSEE.xlsx")
BDD_GWR_Diff_5 <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/INSEE/Var_emploi_cadre.xlsx")
BDD_GWR_Diff_3 = BDD_GWR_Diff_3 %>%
  mutate(Comm_Zone = case_when(Nb_Emplois_par_actif_occupe < 1.05 ~ "<1",
                               Nb_Emplois_par_actif_occupe >= 1.05  ~ ">=1"))
BDD_GWR_Diff = BDD_GWR_Diff_0 %>%
  left_join(BDD_GWR_Diff_1, by = "idcom")%>%
  left_join(BDD_GWR_Diff_2, by = "idcom")%>%
  left_join(BDD_GWR_Diff_3, by = "idcom")%>%
  left_join(BDD_GWR_Diff_4, by = "idcom")%>%
  left_join(BDD_GWR_Diff_5, by = "idcom")%>%
  filter(!idcom==75101,!idcom==75102,!idcom==75103
         ,!idcom==75104,!idcom==75105,!idcom==75106
         ,!idcom==75107,!idcom==75108,!idcom==75109
         ,!idcom==75110,!idcom==75111,!idcom==75112
         ,!idcom==75113,!idcom==75114,!idcom==75115
         ,!idcom==75116,!idcom==75117,!idcom==75118
         ,!idcom==75119,!idcom==75120,!idcom==13201
         ,!idcom==13202,!idcom==13203,!idcom==13204
         ,!idcom==13205,!idcom==13206,!idcom==13207
         ,!idcom==13208,!idcom==13209,!idcom==13210
         ,!idcom==13211,!idcom==13212,!idcom==13213
         ,!idcom==13214,!idcom==13215,!idcom==13216
         ,!idcom==69381,!idcom==69382,!idcom==69383
         ,!idcom==69384,!idcom==69385,!idcom==69386
         ,!idcom==69387,!idcom==69388,!idcom==69389)
rm(BDD_GWR_Diff_1, BDD_GWR_Diff_2, BDD_GWR_Diff_3,
   BDD_GWR_Diff_4, BDD_GWR_Diff_5)

BDD_GWR_Diff$Dep = substr(BDD_GWR_Diff$idcom, start = 1, stop = 2)
BDD_GWR_Diff$Dep = factor(BDD_GWR_Diff$Dep)
colnames(BDD_GWR_Diff)
BDD_GWR_Diff$UU = as.factor(BDD_GWR_Diff$UU)
BDD_GWR_Diff$Comm_Zone = as.factor(BDD_GWR_Diff$Comm_Zone)
BDD_GWR_Diff$Typo_Rural_Urbain = as.factor(BDD_GWR_Diff$Typo_Rural_Urbain)
library(lmtest)
library(sandwich)
OLS_1 = lm(Diff_Niveau~Var_Part_Res_Sec+
             Var_Part_Prop+
             Multi_Diff+TM+
             Var_Rev_Med+
             log(Valeur_foncière_2022_Ensemble)+
             Diff_Cadres_Sup+
             APL+
             Var_Part_Pers_65*relevel(Typo_Rural_Urbain, ref = "rural autonome très peu dense"),
           data=BDD_GWR_Diff)
summary(OLS_1)
coeftest(OLS_1, vcov = vcovHC, type = "HC0")
options(scipen = 4, digits = 4)


BDD_GWR_Diff$libfua[is.na(BDD_GWR_Diff$libfua)] <- 0
BDD_GWR_Diff = BDD_GWR_Diff %>%
  mutate(libfua = case_when(libfua == 0 ~ 0,
                            TRUE ~ 1))

#FUA
OLS_12 = lm(Diff_Niveau~Var_Part_Res_Sec+
              Var_Part_Prop+
              Multi_Diff+TM+
              Var_Rev_Med+
              log(Valeur_foncière_2022_Ensemble)+
              Diff_Cadres_Sup+
              APL+
              loilitt_simp+
              Var_Part_Pers_65*
              libfua,
            data=BDD_GWR_Diff)
summary(OLS_12)
coeftest(OLS_12, vcov = vcovHC, type = "HC0")

OLS_2 = lm(Multi_Diff~Var_Part_Res_Sec+
              Var_Part_Prop+
              Diff_Niveau+TM+
              Var_Rev_Med+
              log(Valeur_foncière_2022_Ensemble)+
              Diff_Cadres_Sup+
              APL+
              loilitt_simp+
              Var_Part_Pers_65*
              libfua,
            data=BDD_GWR_Diff)
summary(OLS_2)
coeftest(OLS_2, vcov = vcovHC, type = "HC0")

####Modèles spatiaux####
Comm_SHP = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/DSN/Communes France + ROM',
                       layer = 'COMMUNE')
Comm_SHP <- sf::st_transform(Comm_SHP, crs = 4326)
Comm_SHP = Comm_SHP %>%
  rename(idcom = `INSEE_COM`)
Comm_SHP = Comm_SHP %>%
  right_join(BDD_GWR_Diff, by = "idcom")

Comm_SHP = Comm_SHP[!is.na(Comm_SHP$TN),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$TM),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$Var_Part_Res_Princ),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$Var_Part_Res_Sec),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$Valeur_foncière_2022_Ensemble),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$Var_Part_Pers_65),]
Comm_SHP = Comm_SHP[!is.na(Comm_SHP$Var_Rev_Med),]

#Faire correspondre les lignes de la matrice W et la DF
Comm_SHP_patial <- as(Comm_SHP, "Spatial")
library(sp)
library(spatialreg)
library(spdep)
#Première matrice de poids
#Elhorst (2010)
coords <- st_centroid(st_geometry(Comm_SHP), of_largest_polygon=TRUE)
nb = poly2nb(Comm_SHP, queen=T, row.names = Comm_SHP$idcom)
table(duplicated(Comm_SHP$idcom))
knn_nb <- knn2nb(knearneigh(coords, k = 3))  # 3 voisins les plus proches
for (i in seq_along(nb)) {
  if (length(nb[[i]]) == 1) {
    nb[[i]] <- knn_nb[[i]]  # Remplacement par les plus proches voisins
  }
}
W <- nb2listw(nb, style = "S",zero.policy = T)

isolated = which(sapply(nb, length) == 0)
if (length(isolated) > 0) {
  cat("Nombre de communes isolées :", length(isolated), "\n")
  cat("Indices des communes isolées :", isolated, "\n")
} else {
  cat("Aucune commune isolée.\n")
}
#Pour les observations qui n'ont pas de contiguité (iles, 
#communes limitrophes, on prend les 3 plus proches voisins)
SDM = lagsarlm(Diff_Niveau~Var_Part_Res_Sec+
                 Var_Part_Prop+
                 Multi_Diff+TM+
                 Var_Rev_Med+
                 log(Valeur_foncière_2022_Ensemble)+
                 Diff_Cadres_Sup+
                 APL+
                 loilitt_simp+
                 Var_Part_Pers_65*
                 relevel(Typo_Rural_Urbain, ref = "rural autonome très peu dense"),
               listw=W, type = "mixed",
               data=Comm_SHP, method="LU",
               zero.policy = T)
summary(SDM)
impacts(SDM, listw = W, R = 100)

SDM_12 = lagsarlm(Diff_Niveau~Var_Part_Res_Sec+
                    Var_Part_Prop+
                    Multi_Diff+TM+
                    Var_Rev_Med+
                    log(Valeur_foncière_2022_Ensemble)+
                    Diff_Cadres_Sup+
                    APL+
                    loilitt_simp+
                    Var_Part_Pers_65*libfua,
                  type = "mixed",
              listw=W, data=Comm_SHP, method="LU",
               zero.policy = T)
summary(SDM_12)
impacts(SDM_12, listw = W, R = 100)

SDM_2 = lagsarlm(Multi_Diff~
                    Diff_Niveau+TM+
                    Var_Rev_Med+
                    log(Valeur_foncière_2022_Ensemble)+
                    Diff_Cadres_Sup+
                    APL+
                    loilitt_simp+
                    Var_Part_Pers_65*libfua,
                  type = "mixed",
                  listw=W, data=Comm_SHP, method="LU",
                  zero.policy = T)
summary(SDM_2)
impacts(SDM_2, listw = W, R = 100)


options(scipen=4, digits= 4)
SAR_SLS = stsls(Diff_Niveau~Var_Part_Res_Sec+
                  Var_Part_Prop+
                  Multi_Diff+TM+
                  Var_Rev_Med+
                  log(Valeur_foncière_2022_Ensemble)+
                  Diff_Cadres_Sup+
                  APL+
                  loilitt_simp+
                  Var_Part_Pers_65*
              relevel(Typo_Rural_Urbain, ref = "rural autonome très peu dense"),
            listw=W, data=Comm_SHP,
            robust = T,
               zero.policy = T)
summary(SAR_SLS)

options(scipen=4, digits= 4)
SAR_SLS_1 = stsls(Diff_Niveau~Var_Part_Res_Sec+
                    Var_Part_Prop+
                    Multi_Diff+TM+
                    Var_Rev_Med+
                    log(Valeur_foncière_2022_Ensemble)+
                    Diff_Cadres_Sup+
                    APL+
                    loilitt_simp+
                    Var_Part_Pers_65*
                libfua,listw=W, data=Comm_SHP,
            robust = T,
            zero.policy = T)
summary(SAR_SLS_1)
modelsummary::modelsummary(SAR_SLS_1)

SAR_SLS_2 = stsls(Multi_Diff~Var_Part_Res_Sec+
                    Var_Part_Prop+
                    Diff_Niveau+TM+
                    Var_Rev_Med+
                    log(Valeur_foncière_2022_Ensemble)+
                    Diff_Cadres_Sup+
                    APL+
                    loilitt_simp+
                    Var_Part_Pers_65*
                    libfua,listw=W, data=Comm_SHP,
                  robust = T,
                  zero.policy = T)
summary(SAR_SLS_2)
modelsummary::modelsummary(SAR_SLS_2)

####MUA - Centre####
table(BDD_GWR_Diff$LIBZE2020)
MUA = BDD_GWR_Diff %>% filter(LIBZE2020=="Bordeaux"|
                              LIBZE2020=="Brest"|
                              LIBZE2020=="Clermont-Ferrand"|
                              LIBZE2020=="Dijon"|
                              LIBZE2020=="Grenoble"|
                              LIBZE2020=="Lille"|
                              LIBZE2020=="Lyon"|
                              LIBZE2020=="Marseille"|
                              LIBZE2020=="Metz"|
                              LIBZE2020=="Montpellier"|
                              LIBZE2020=="Nancy"|
                              LIBZE2020=="Nantes"|
                              LIBZE2020=="Nice"|
                              LIBZE2020=="Orléans"|
                              LIBZE2020=="Paris"|
                              LIBZE2020=="Rennes"|
                              LIBZE2020=="Rouen"|
                              LIBZE2020=="Saint Etienne"|
                              LIBZE2020=="Strasbourg"|
                              LIBZE2020=="Toulon"|
                              LIBZE2020=="Toulouse"|
                              LIBZE2020=="Tours")

MUA = MUA %>% filter(!idcom=="33063",
                       !idcom=="29019",
                       !idcom=="63113",
                       !idcom=="21231",
                       !idcom=="38185",
                       !idcom=="59350",
                       !idcom=="69123",
                       !idcom=="13055",
                       !idcom=="57463",
                       !idcom=="34172",
                       !idcom=="54395",
                       !idcom=="44109",
                       !idcom=="06088",
                       !idcom=="45234",
                       !idcom=="75056",
                       !idcom=="35238",
                       !idcom=="42218",
                       !idcom=="67482",
                       !idcom=="83137",
                       !idcom=="31555",
                       !idcom=="37261")

MUA = MUA %>%
  select(idcom, Libellé, LIBZE2020 ,Var_Part_Pers_65, Diff_Niveau)
MUA = MUA %>%
  group_by(idcom, LIBZE2020)%>%
  summarize(`VarNombre+65` = mean(Var_Part_Pers_65, na.rm = T),
            `VarK+65` = mean(Diff_Niveau, na.rm = T))

writexl::write_xlsx(MUA, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/MUA_Sans_Ville_Centre.xlsx")

####MUA - FUA####
colnames(BDD_GWR_Diff)
table(BDD_GWR_Diff$libfua)
MUA = BDD_GWR_Diff %>% filter(libfua=="Bordeaux"|
                                libfua=="Brest"|
                                libfua=="Clermont-Ferrand"|
                                libfua=="Dijon"|
                                libfua=="Grenoble"|
                                libfua=="Lille"|
                                libfua=="Lyon"|
                                libfua=="Marseille"|
                                libfua=="Metz"|
                                libfua=="Montpellier"|
                                libfua=="Nancy"|
                                libfua=="Nantes"|
                                libfua=="Nice"|
                                libfua=="Orléans"|
                                libfua=="Paris"|
                                libfua=="Rennes"|
                                libfua=="Rouen"|
                                libfua=="Saint-Étienne"|
                                libfua=="Strasbourg"|
                                libfua=="Toulon"|
                                libfua=="Toulouse"|
                                libfua=="Tours")

MUA = MUA %>% filter(!LIBZE2020=="Bordeaux",
                       !LIBZE2020=="Brest",
                       !LIBZE2020=="Clermont-Ferrand",
                       !LIBZE2020=="Dijon",
                       !LIBZE2020=="Grenoble",
                       !LIBZE2020=="Lille",
                       !LIBZE2020=="Lyon",
                       !LIBZE2020=="Marseille",
                       !LIBZE2020=="Metz",
                       !LIBZE2020=="Montpellier",
                       !LIBZE2020=="Nancy",
                       !LIBZE2020=="Nantes",
                       !LIBZE2020=="Nice",
                       !LIBZE2020=="Orléans",
                       !LIBZE2020=="Paris",
                       !LIBZE2020=="Rennes",
                       !LIBZE2020=="Rouen",
                       !LIBZE2020=="Saint Etienne",
                       !LIBZE2020=="Strasbourg",
                       !LIBZE2020=="Toulon",
                       !LIBZE2020=="Toulouse",
                       !LIBZE2020=="Tours")

MUA = MUA %>%
  select(idcom, Libellé, libfua ,Var_Part_Pers_65, Diff_Niveau)
MUA = MUA %>%
  group_by(libfua)%>%
  summarize(`VarNombre+65` = mean(Var_Part_Pers_65, na.rm = T),
            `VarK+65` = mean(Diff_Niveau, na.rm = T))

writexl::write_xlsx(MUA, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/FUA_Sans_MUA.xlsx")


####GWR####
##Fond de carte SHP##
Comm_SHP = sf::read_sf(dsn = 'C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/DSN/Communes France + ROM',
                       layer = 'COMMUNE')
trueCentroids = sf::st_centroid(Comm_SHP,byid=TRUE)
Centroides = as.data.frame(trueCentroids$geometry)
EPCI_Data = as.data.frame(Comm_SHP$INSEE_COM)
trueCentroids = data.frame(sf::st_coordinates(sf::st_cast(trueCentroids$geometry,"POINT")))
trueCentroids = trueCentroids %>%
  rename(Longitude = X,
         Latitude = Y)
Comm_SHP = cbind(EPCI_Data, trueCentroids)
Comm_SHP = Comm_SHP %>%
  rename(idcom = `Comm_SHP$INSEE_COM`)

BDD_GWR_Diff = left_join(BDD_GWR_Diff, Comm_SHP,
                         by = "idcom")
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Var_Part_Res_Sec),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Var_Part_Prop),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Var_Part_Loc),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Multi_Diff),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$TM),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$TN),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Var_Part_Pers_65),]
BDD_GWR_Diff = BDD_GWR_Diff[!is.na(BDD_GWR_Diff$Longitude),]

library(spdep)
library(sp)
library(GWmodel)
my.sf.point <- sf::st_as_sf(x = BDD_GWR_Diff,
                            coords = c("Longitude", "Latitude"),
                            crs = "+proj=longlat +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0")
Fusion_EPCI_patial <- as(my.sf.point, "Spatial")

coords <- as.matrix(coordinates(Fusion_EPCI_patial))
dm.calib <- gw.dist(dp.locat=coordinates(Fusion_EPCI_patial))

bw0 <- bw.gwr(Diff_Niveau~Var_Part_Res_Sec+
                Var_Part_Prop+
                Multi_Diff+TN+TM+
                log(Valeur_foncière_2022_Ensemble)+
                loilitt_simp+
                Part_Cadres_Sup+
                log(Med_Niv_Vie)+
                Var_Part_Pers_65*
                relevel(Typo_Rural_Urbain, ref = "rural autonome très peu dense")+
                APL,
              data = Fusion_EPCI_patial, approach="AICc",
              kernel="bisquare",
              adaptive=T,dMat=dm.calib)
#425
Sca_GWR = gwr.scalable(Diff_Niveau~Var_Part_Res_Sec+
                         Var_Part_Prop+
                         Multi_Diff+TN+TM+
                         log(Valeur_foncière_2022_Ensemble)+
                         loilitt_simp+
                         Part_Cadres_Sup+
                         log(Med_Niv_Vie)+
                         Var_Part_Pers_65*
                         relevel(Typo_Rural_Urbain, ref = "rural autonome très peu dense")+
                         APL,
                       dMat = dm.calib,
                      bw.adapt = 310, longlat = F,
                       kernel="gaussian")
Sca_GWR
sp = Sca_GWR$SDF
BDD_GWR_Diff$Var_OLDDEP_Niv
sp$idcom = BDD_GWR_Diff$idcom
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
library(raster)
shapefile(sp, "Cartes GWR/GWR_Commune_Diff_OLDDEP.shp",overwrite=TRUE)


##########Graphiques coefficients##############
library(ggplot2)
library(ggthemes)
help(expression)
ggplot(BDD_GWR_Diff, aes(y = Diff_Niveau, x = Var_Part_Pers_65)) +
  theme_minimal()+
  geom_smooth(method = lm, formula = y ~ x, se = FALSE, color = "cyan4") +
  geom_point()+
  ylab(expression(Delta~"HDE"))+
  xlab(expression(Delta~"65+"))+
  theme(axis.text.x = element_text(size = 19, family="serif", color = "black"),
        axis.text.y = element_text(size = 19, family="serif", color = "black"),
        axis.title.y = element_text(size = 22, family="serif", color = "black"),
        axis.title.x = element_text(size = 22, family="serif", color = "black"))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
ggsave("Retirees_Housdep.jpeg", units="in", width=10, height=6.5)

Valorisation = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats/Valorisation fusion.xlsx",
                             sheet = "Différences de richesses")
ggplot(Valorisation, aes(y = Diff_Pourcentage, x = Age)) +
  theme_classic()+
  geom_hline(yintercept=0,
             size = 1.5, color = "black")+
  geom_line(color = "cyan4", size = 1.5) +
  ylab(expression(Delta~"HDE"))+
  xlab("Age of owner")+
  scale_y_continuous(labels = scales::percent)+
  theme(axis.text.x = element_text(size = 19, family="serif", color = "black"),
        axis.text.y = element_text(size = 19, family="serif", color = "black"),
        axis.title.y = element_text(size = 22, family="serif", color = "black"),
        axis.title.x = element_text(size = 22, family="serif", color = "black"),
        panel.grid.major = element_line(color = "gray39", linewidth = 0.25, linetype = "dashed"),  # Quadrillage principal
        panel.grid.minor = element_line(color = "gray39", linewidth = 0.25, linetype = "dashed"))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Résultats")
ggsave("Delta_HDE par age.jpeg", units="in", width=10, height=6.5)

colnames(BDD_GWR_Diff)
BDD_GWR_Diff$Surplus = BDD_GWR_Diff$Diff_Niveau-BDD_GWR_Diff$Var_Part_Pers_65
mean(BDD_GWR_Diff$Surplus, na.rm = T)

colnames(BDD_GWR_Diff)
BDD_GWR_Diff$Dep = substr(BDD_GWR_Diff$idcom, start = 1, stop = 2)
Surplus_Dep = 
  BDD_GWR_Diff %>% 
  group_by(Dep) %>% 
  summarise(Surplus = mean(Surplus, na.rm = T))
mean(Surplus_Dep$Surplus)
writexl::write_xlsx(Surplus_Dep, "Surplus_Departement_2.xlsx")
