library("dplyr")

IRS2019 = read.csv(file.choose())

IRS2019 <- IRS2019 %>% filter(STATE %in% c("AL","TN","FL"))

write.csv(IRS2019,"/Users/tomvdo29/Desktop/Consulting Project/Data/IRS/2019/IRS2019_3states.csv")