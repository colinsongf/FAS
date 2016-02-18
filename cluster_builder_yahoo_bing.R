#YAHOOOOOOO

lista<-read.csv("/home/asus/quickrank/data/Webscope_C14B/nonescludere.txt",sep='\t', header=0)
lista<-as.matrix(lista)

corr<-read.csv("/home/asus/quickrank/data/Webscope_C14B/spear_corr.txt",sep='\t', header=0)
corr<-corr[lista,lista]
corr<-as.matrix(corr)

abs.corr<-abs(corr)
abs.corr[!is.finite(abs.corr)] <- 0
hc=hclust(as.dist(1-abs.corr),method = "ward.D", members = NULL)

plot(hc, cex=0.2) 

trials=c(26,52,104,156,208,260,389)

for(i in 1:length(trials)) 
{
  print(i)
  path=paste("/home/asus/quickrank/data/Webscope_C14B/g_",toString(trials[i]),".txt",sep="")
  g<-cutree(hc,k=trials[i])
  write.csv(g,file=path,sep = "\t", col.names = FALSE, quote = FALSE)
}

#BING
corr<-as.matrix(corr)
abs.corr<-abs(as.matrix(corr[1:136,1:136]))
corr<-read.csv("/home/asus/quickrank/data/MSLR-WEB30K/Fold1/spear_corr.txt",sep='\t', header=FALSE,col.names = seq(1,137))
colnames(corr) <- seq(1,137)
abs.corr[!is.finite(abs.corr)] <- 0
hc2=hclust(as.dist(1-abs.corr),method = "ward.D", members = NULL)

plot(hc2, cex=0.5) 

trials=c(7,14,27,41,54,68,102)

for(i in 1:length(trials)) 
{
  print(i)
  path=paste("/home/asus/quickrank/data/MSLR-WEB30K/Fold1/g",toString(trials[i]),".txt",sep="")
  g<-cutree(hc2,k=trials[i])
  print(g)
  write.csv(g,file=path,sep = "\t", col.names = FALSE, quote = FALSE)
}
