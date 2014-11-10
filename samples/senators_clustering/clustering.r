library("rjson")
json_file <- "vectors_Senado_2014_33.json"
json_data <- fromJSON(file=json_file)

# number of dimensions 33(number of sessions in 2014 window I picked)
m = matrix( ncol = 33)
a = 0

nombres = names(json_data)
for(congresista in json_data){
  t = output <- matrix(unlist( congresista$vector),ncol = 33, byrow = TRUE)
  dimnames(t) <- list( congresista$partido )
   m = rbind(m, t)  
}

m= na.omit(m)
row.names(m) = nombres
print(m)
library(sparcl)
par(cex=0.5)
d <- dist(m)
hc <- hclust(d)
y = cutree(hc, 5)

ColorDendrogram(hc,
                y=y,
                labels = names(y),
                main = "Senators cluster",
                xlab = NULL,
                sub = NULL,
                ylab = "",
                cex.main = NULL,
                branchlength = 80)

rect.hclust(hc, k=5, border="red")
