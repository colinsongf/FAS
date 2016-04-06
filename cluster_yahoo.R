library(corrplot)

corr2<-read.csv("/home/asus/quickrank/data/Fold1/spear_corr.txt",sep='\t', header=0)
corr2<-as.matrix(corr2[,1:136])
col1 <-rainbow(100, s = 1, v = 1, start = 0.2, end = 1, alpha = 1)
corrplot(abs(corr2), order = "hclust",method = "color",cl.pos="n", tl.pos="n",addrect = 13)

corr2<-read.csv("/home/asus/quickrank/data/Fold1/spear_corr.txt",sep='\t', header=0)
corr2<-as.matrix(corr2[,1:136])
colnames(corr2)<-seq(1,136)
hc=hclust(as.dist(1-abs(corr2)),method = "mcquitty", members = NULL)
plot(hc, cex=0.2) 
trials=c(7,14,27,41,54,68,102)

for(i in 1:length(trials)) 
{
  print(i)
  path=paste("/home/asus/quickrank/data/Fold1/g",toString(trials[i]),".txt",sep="")
  g<-cutree(hc,k=trials[i])
  write.csv(g,file=path,sep = "\t", col.names = FALSE, quote = FALSE)
}


lista<-read.csv("/home/asus/quickrank/data/Webscope_C14B/nonescludere.txt",sep='\t', header=0)
lista<-as.matrix(lista)

corr<-read.csv("/home/asus/quickrank/data/Webscope_C14B/spear_corr.txt",sep='\t', header=0)
corr<-corr[lista,lista]
corr<-as.matrix(corr)
library(corrplot)

#col1 <-rainbow(100, s = 1, v = 1, start = 0.2, end = 1, alpha = 1)
corrplot(abs(corr), order = "hclust",method = "color",addgrid.col = NULL,cl.pos="n", tl.pos="n",addrect = 50)
library(RColorBrewer)
corrplot(abs(corr), order="hclust", tl.pos="n",addrect = 50, addgrid.col = NULL,col=brewer.pal(n=4, name="Blues"))
corr<-abs(corr)
corr[!is.finite(corr)] <- 0
hc=hclust(as.dist(1-abs(corr)),method = "single", members = NULL)

plot(hc, cex=0.2) 

trials=c(26,52,104,156,208,260,389)

for(i in 1:length(trials)) 
{
  print(i)
  path=paste("/home/asus/quickrank/data/Webscope_C14B/g_",toString(trials[i]),".txt",sep="")
  g<-cutree(hc,k=trials[i])
  write.csv(g,file=path,sep = "\t", col.names = FALSE, quote = FALSE)
}


corr<-read.csv("/home/asus/quickrank/data/Fold1/spear_corr.txt",sep='\t', header=FALSE,col.names = seq(1,137))
corr<-as.matrix(corr)
corr<-abs(as.matrix(corr[1:136,1:136]))
colnames(corr)<-seq(1,136)
corr[!is.finite(corr)] <- 0
hc=hclust(as.dist(1-abs(corr)),method = "complete", members = NULL)

plot(hc, cex=0.5) 

trials=trials=c(7,14,27,41,54,68,102)

for(i in 1:length(trials)) 
{
  print(i)
  path=paste("/home/asus/quickrank/data/Fold1/g",toString(trials[i]),".txt",sep="")
  g<-cutree(hc,k=trials[i])
  write.csv(g,file=path,sep = "\t", col.names = FALSE, quote = FALSE)
}

g<-cutree(hc,k=50)
write.csv(g,file="/home/asus/quickrank/data/Webscope_C14B/g")