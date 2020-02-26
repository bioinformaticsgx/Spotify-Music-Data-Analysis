## scatterplot matrix example
p16 = ggplot(data=d,aes(x=album_popularity, y=track_popularity)) + geom_point(col=rgb(0,0,215,5,maxColorValue=255), pch=16) + geom_smooth(method=glm,se=TRUE,size=0.5,color="gold") + theme(panel.background = element_blank())


## barplot
ggplot(data=data, aes(fill=Class, y=Track_Num, x=reorder(Genres,-Track_Num))) + geom_bar(stat="identity") + theme(panel.background = element_blank(),axis.text.x = element_text(angle = 45, hjust = 1,size=8)) + ylab("Num") + xlab("Genres")

## boxplot matrix example
q16 = ggplot(d, aes(x=factor(year), y=album_popularity)) + geom_boxplot(fill=rgb(0,0,215,100,maxColorValue=255),lwd=0.2,colour="black",outlier.colour="brown", outlier.shape=20, outlier.size=1) + stat_summary(fun.y=mean, geom="line", aes(group=2),colour="gold",size=0.9)  + stat_summary(fun.y=mean, geom="point",size=0.5,colour="black") + theme(panel.background = element_blank(),axis.text.x = element_text(angle = 45, hjust = 1,size=4)) + xlab('year')

## chord diagram
corr <- cor(dat)
chordDiagram(corr)

##
geom_line
