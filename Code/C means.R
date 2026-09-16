rm(list=ls())
library(dplyr)
Indices_socio_démo <- readxl::read_excel("C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Indices socio-démo.xlsx")
Indices_socio_démo = Indices_socio_démo[!is.na(Indices_socio_démo$Valeur_foncière),]
Indices_socio_démo = Indices_socio_démo %>% filter(!Dep==75)
Indices = Indices_socio_démo %>% select(Part_prop_occupant, Solde_Migratoire_Pop,
                                        Population, Solde_naturel_Pop,
                                        Part_actifs_occupés, Part_cadres_PIS, Taux_Pauvreté,
                                        Part_logements_sociaux, Valeur_foncière, Part_65_plus)
Indices_Norm = as.data.frame(scale(Indices))

#Kmeans
library(e1071)
library(factoextra)
library(clValid)
NbClust(Indices_Norm, method = 'complete', index = 'all')$Best.nc

set.seed(123)
wss <- function(k) {
  kmeans(Indices_Norm, k, nstart = 10 )$tot.withinss
}
k.values <- 1:15
gap.stat <- clusGap(Indices_Norm, FUNcluster = kmeans, K.max = 15)
gap.stat
fviz_nbclust(Indices_Norm, kmeans, method = "silhouette", k.max = 10) + theme_minimal() + ggtitle("The Silhouette Plot")

intern <- clValid(Indices_Norm, nClust = 2:10, 
                  clMethods = c("hierarchical","kmeans","pam"), validation = "internal")


Clusters = cmeans(Indices_Norm, 4)
Indices = cbind(Indices_socio_démo, Clusters$cluster)

writexl::write_xlsx(Indices, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Indices socio-démo_Cluster.xlsx")

####PCA + C-Means####
library(factoextra)
library(FactoMineR)
res.pca = PCA(Indices_Norm, scale.unit = TRUE, ncp = 3, graph = TRUE)
res.pca
eig.val <- get_eigenvalue(res.pca)
eig.val


PCA_Final = PCA(Indices_Norm, scale.unit = TRUE, ncp = 3, graph = TRUE)
DF_PCA =  as.data.frame(PCA_Final[["ind"]][["coord"]])
Clusters = cmeans(DF_PCA, 4)
Indices = cbind(Indices_socio_démo, Clusters$cluster)
writexl::write_xlsx(Indices, "C:/Users/guill/Desktop/Master APE/Doctorat/Thèse cifre/Valorisation/Indices socio-démo_Cluster_PCA.xlsx")