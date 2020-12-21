rm(list = ls())
options(scipen = 999)
library(reticulate)
py_install("")

setwd("~/Desktop/rsdata/")

library(dplyr)
library(tidyr)
library(tidyverse)
library(reshape)
library(ggplot2)
library(GGally)
library(gridExtra)
library(plotly)



# Creating a space for all the days data 
gen = function(firstday, lastday){
  step  = seq(firstday,lastday, by = 1)
  Rs = "Rs"
  rep = rep(Rs, lastday)
  for(i in step) {
    space =paste0(rep,step)
  }
  return(space)
}

# First day = 1 Last Day = Last Rs number in File 
sample = gen(firstday = 1, lastday = 95)
View(sample)
# reading in
mylist <- list() 
for (i in 1:length(sample)){
  mylist[[i]] <- read.csv(sample[i])
  mylist[[i]] = mylist[[i]][,-c(1,2,4,5)]
  colnames(mylist[[i]]) = c("Item", "Price")
}
# Dates 
date  = seq(as.Date("2020-08-16"), as.Date("2020-11-18"), by="days")

tail(date)

for(i in 1:length(date)){
  mylist[[i]]$date <- date[i]
  mylist[[i]]$day <- weekdays(as.Date(mylist[[i]]$date))
}

View(mylist)

# Merging
data <- merge_recurse(mylist)

View(data)


# Export 
write.csv(data,"RunescapeItems.csv", row.names = FALSE)
# Import
rune = read_csv("RunescapeItems.csv")
View(rune)


# Example for future reference 
check = rune %>% filter(rune$Item == "Abyssal whip")

p = ggplot(check) + aes(date, Price) + 
  geom_line(linetype = "dashed") + 
  geom_point(color="deepskyblue", size=1) + 
  labs(title = "Abyssal whip", x = "Date",y = "Price") + 
  theme_bw()+
  theme(plot.title = element_text(hjust = 0.5))

ggplotly(p)
# Corr
ggpairs(check)

# When I was switching back and worth 
ab = check[,-c(1,4)]
write.csv(ab,"whip.csv", row.names = FALSE)





