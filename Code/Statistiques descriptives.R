rm(list=ls())
library(dplyr)
library(ggplot2)
library(ggthemes)
Fusion_11 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/11_Fusion.csv")
Fusion_24 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/24_Fusion.csv")
Fusion_27 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/27_Fusion.csv")
Fusion_28 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/28_Fusion.csv")
Fusion_32 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/32_Fusion.csv")
Fusion_44 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/44_Fusion.csv")
Fusion_52 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/52_Fusion.csv")
Fusion_53 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/53_Fusion.csv")
Fusion_75 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/75_Fusion.csv")
Fusion_76 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/76_Fusion.csv")
Fusion_84 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/84_Fusion.csv")
Fusion_93 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/93_Fusion.csv")
Fusion_94 = readr::read_csv("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Données/DV3F/DV3F_CSV/94_Fusion.csv")

Fusion = rbind(Fusion_11, Fusion_24, Fusion_27, Fusion_28,
               Fusion_32, Fusion_44, Fusion_52, Fusion_53,
               Fusion_75, Fusion_76, Fusion_84, Fusion_93,
               Fusion_94)
rm(Fusion_11, Fusion_24, Fusion_27, Fusion_28,
   Fusion_32, Fusion_44, Fusion_52, Fusion_53,
   Fusion_75, Fusion_76, Fusion_84, Fusion_93,
   Fusion_94)
Fusion_Vente = Fusion %>% filter(fflogsoc == FALSE)
Fusion_Vente_Maison = Fusion %>% filter(fflogsoc == FALSE,
                                        ffctyploc == 1)
Fusion_Vente_Appart = Fusion %>% filter(fflogsoc == FALSE,
                                        ffctyploc == 2)

Luxe = Fusion %>% mutate(Luxe = case_when(valeurfonc >=1000000~1,
                                          TRUE~0))
Luxe$NB = 1
Luxe$Dep = substr(Luxe$ffcodinsee, start = 1, stop = 2)

Luxe_Dep = Luxe %>%
  group_by(Dep, dateannee)%>%
  summarise(Nombre_Trans_Luxe = sum(Luxe),
            Nombre_Trans = sum(NB))
260353/288549
writexl::write_xlsx(Luxe_Dep, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Chapitre 1 luxe/Faits stylisés/Nb_transactions_luxe_par_département.xlsx")

mean(Fusion_Vente$pm2)
Fusion_Vente_Prix_M2 = Fusion_Vente %>%
                        filter(dateannee==2022)%>%
                        group_by(ffcodinsee)%>%
                        summarise(Prix_médian = median(pm2))
writexl::write_xlsx(Fusion_Vente_Prix_M2, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Cartes/Prix médians par commune 2022_1.xlsx")

Fusion_Vente$NB = 1
FF = Fusion_Vente %>%
  group_by(ffcodinsee)%>%
  summarise(Somme = sum(NB))
writexl::write_xlsx(FF, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Cartes/Nombre_de_transactions_1.xlsx")
####Graphiques Stats descriptives####
Unites_urbaines = readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Grille_Densité.xlsx")
Fusion_Vente = left_join(Fusion_Vente, Unites_urbaines, 
                         by = 'ffcodinsee')
Fusion_Vente$NB = 1
colnames(Fusion_Vente)
Fusion_Vente = Fusion_Vente %>% mutate(Lib_dens_1 = case_when(DENS == 7~"Rural à habitat dispersé",
                                                              TRUE~LIB_DENS))

table(Fusion_Vente$Lib_dens_1)
Fusion_Vente$Lib_dens_1 = as.character(Fusion_Vente$Lib_dens_1)
Nb_Ventes = Fusion_Vente %>%
  group_by(Lib_dens_1)%>%
  summarise(Nb_transacs = sum(NB))
Nb_Ventes = Nb_Ventes[!is.na(Nb_Ventes$Lib_dens_1),]

ggplot(Nb_Ventes, aes(x = Lib_dens_1,y=Nb_transacs,
                      fill=Lib_dens_1), color = "black") +
  geom_col()+
  theme_classic()+
  scale_fill_stata()+
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
  ylab('Nombre de transactions')+
  guides(fill=guide_legend(title="Type de commune",
                           nrow=2,byrow=TRUE))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Graphiques")
ggsave("NB_transacs_UU.jpeg", units="in", width=14, height=10)
writexl::write_xlsx(Nb_Ventes,"C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Graphiques/Nombre de ventes par unité urbaine.xlsx")

Nb_Ventes = Fusion_Vente %>%
  group_by(CATAEU2010.y, dateannee)%>%
  summarise(Nb_transacs = sum(NB))
Nb_Ventes = Nb_Ventes[!is.na(Nb_Ventes$CATAEU2010.y),]
Nb_Ventes$dateannee = as.character(Nb_Ventes$dateannee)

ggplot(Nb_Ventes, aes(x = dateannee,y=Nb_transacs,
                      group=CATAEU2010.y, color = CATAEU2010.y)) +
  geom_line(size = 2)+
  theme_classic()+
  scale_color_stata()+
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
  ylab('Nombre de transactions')+
  guides(fill=guide_legend(title="Type de commune",
                           nrow=2,byrow=TRUE))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Graphiques")
ggsave("NB_transacs_Année.jpeg", units="in", width=15, height=11)

Nb_Ventes = Fusion_Vente %>%
  group_by(ffcodinsee)%>%
  summarise(Nb_transacs = sum(NB))
writexl::write_xlsx(Nb_Ventes, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Cartes/Nombre_de_transactions.xlsx")

#Histogramme prix####
ggplot(Fusion, aes(x = ffshab)) +
  geom_histogram(fill = "gray45", colour = "black")+
  theme_classic()+
  scale_colour_stata()+
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
  ylab('Living area')+
  guides(fill=guide_legend(title="Type de commune",
                           nrow=2,byrow=TRUE))
setwd("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Graphiques")
ggsave("Hist_PM2.jpeg", units="in", width=14, height=10)
