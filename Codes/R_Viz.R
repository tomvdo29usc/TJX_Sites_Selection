library(sf) 
library(dplyr)
library(tmap)
library(stringr)
tmap_mode("view")
# Load map data
FL_map <- st_read("/Users/tomvdo29/Desktop/Consulting Project/Data/All_Tracts/FL_tract/tl_2022_12_tract.shp", stringsAsFactors = FALSE)
TN_map <- st_read("/Users/tomvdo29/Desktop/Consulting Project/Data/All_Tracts/TN_tract/tl_2022_47_tract.shp", stringsAsFactors = FALSE)
AL_map <- st_read("/Users/tomvdo29/Desktop/Consulting Project/Data/All_Tracts/AL_tract/tl_2022_01_tract.shp", stringsAsFactors = FALSE)

states_map = rbind(AL_map,FL_map,TN_map)
states_map$GEOID <- as.numeric(states_map$GEOID)
Tract_Pop <- read.csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Final_Data/all_states_tract_pop.csv")
pop_map <- left_join(states_map, Tract_Pop[,c("GEOID","Tract_Population")], by = c("GEOID" = "GEOID"))

#pop_map <- pop_map %>% filter(STATEFP == "47")

clientDF <-  read.csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Final_Data/CLients_Data.csv")

HG_data <- clientDF %>% filter(Name == "HomeGoods") %>%
  st_as_sf(coords = c("Long","Lat"))
TJ_data <- clientDF %>% filter(Name == "T.J. Maxx") %>%
  st_as_sf(coords = c("Long","Lat")) 
MS_data <- clientDF %>% filter(Name == "Marshalls") %>%
  st_as_sf(coords = c("Long","Lat"))


tm_shape(st_as_sf(pop_map)) + 
  tm_fill("Tract_Population",palette="Greens",id="NAME") +
tm_shape(HG_data) + 
  tm_dots("Total_Visits", palette="Purples", size = 0.05,title = "HomeGoods",popup.vars=c("Rank","Total_Visits"),id="Name")+
tm_shape(MS_data) + 
  tm_dots("Total_Visits", palette="Blues", size = 0.05,title = "Marshalls",popup.vars=c("Rank","Total_Visits"),id="Name")+
tm_shape(TJ_data) + 
  tm_dots("Total_Visits", palette="Reds", size = 0.05,title = "T.J. Maxx",popup.vars=c("Rank","Total_Visits"),id="Name")



###############
library(ggplot2)
library(scales)
final_data <-  read.csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Final_Data/3states_final.csv")

comp_df <- final_data %>% select("Rank":"State","Total_Visits","num_nearby_Burlington":"tot_visits_nearby_Marshalls")
marshalls_can <- final_data %>% 
  select("Rank":"State","Total_Visits",ends_with("_Marshalls")) %>%
  filter(Name == "Marshalls") %>%
  group_by(num_nearby_Marshalls) %>%
  summarise(Avg_Visit = mean(Total_Visits), Avg_Visit_to_Nearby_Marshalls = sum(tot_visits_nearby_Marshalls)/sum(num_nearby_Marshalls))

sfactor <- max(marshalls_can$Avg_Visit, na.rm=TRUE)/max(marshalls_can$Avg_Visit_to_Nearby_Marshalls,na.rm=TRUE)
marshalls_can %>%
  ggplot() +
  geom_bar((aes(x=as.factor(num_nearby_Marshalls),y=Avg_Visit)),stat="identity",fill="#182C54",colour="white",alpha=0.95)+
  geom_line(aes(x=as.factor(num_nearby_Marshalls),y=Avg_Visit_to_Nearby_Marshalls*sfactor),stat="identity",group = 1, color = "#FFD100",size=1.5,,alpha=0.95)+
  scale_y_continuous(labels = label_number(suffix = "K", scale = 1e-3),
                     "Average Visits", 
                     sec.axis = sec_axis(trans= ~./sfactor, 
                                         name = "Nearby Marshalls Average Visit",
                                         labels = label_number(suffix = "K", scale = 1e-3)))+
  xlab("Number of Nearby Marshalls Stores")+
  ggtitle("Marshalls Store Loses Its Customers To Its Nearby Stores")+
  theme(axis.text=element_text(size=14),
        axis.title=element_text(size=14,face="bold"),
        plot.title = element_text(size = 30, face = "bold"),
        axis.line = element_line(color = "black"),
        axis.line.y = element_line())


TJ_can <- final_data %>% 
  select("Rank":"State","Total_Visits",ends_with("_T.J._Maxx")) %>%
  filter(Name == "T.J. Maxx") %>%
  group_by(num_nearby_T.J._Maxx) %>%
  summarise(Avg_Visit = mean(Total_Visits), Avg_Visit_to_Nearby_T.J._Maxx = sum(tot_visits_nearby_T.J._Maxx)/sum(num_nearby_T.J._Maxx))

sfactor2 <- max(TJ_can$Avg_Visit, na.rm=TRUE)/max(TJ_can$Avg_Visit_to_Nearby_T.J._Maxx,na.rm=TRUE)
TJ_can %>%
  ggplot() +
  geom_bar((aes(x=as.factor(num_nearby_T.J._Maxx),y=Avg_Visit)),stat="identity",fill="#C40D11",colour="white",alpha=0.95)+
  geom_line(aes(x=as.factor(num_nearby_T.J._Maxx),y=Avg_Visit_to_Nearby_T.J._Maxx*sfactor2),stat="identity",group = 1, color = "#FFD100",size=1.5,,alpha=0.95)+
  scale_y_continuous(labels = label_number(suffix = "K", scale = 1e-3),
                     "Average Visits", 
                     sec.axis = sec_axis(trans= ~./sfactor, 
                                         name = "Nearby T.J. Maxx Average Visit",
                                         labels = label_number(suffix = "K", scale = 1e-3)))+
  xlab("Number of Nearby T.J. Maxx Stores")+
  ggtitle("More T.J. Maxx Stores Nearby Increases The Average Visit")+
  theme(axis.text=element_text(size=14),
        axis.title=element_text(size=14,face="bold"),
        plot.title = element_text(size = 30, face = "bold"),
        axis.line = element_line(color = "black"),
        axis.line.y = element_line())


HG_can <- final_data %>% 
  select("Rank":"State","Total_Visits",ends_with("_HomeGoods")) %>%
  filter(Name == "HomeGoods") %>%
  group_by(num_nearby_HomeGoods) %>%
  summarise(Avg_Visit = mean(Total_Visits), Avg_Visit_to_Nearby_HomeGoods = sum(tot_visits_nearby_HomeGoods)/sum(num_nearby_HomeGoods))

sfactor3 <- max(HG_can$Avg_Visit, na.rm=TRUE)/max(HG_can$Avg_Visit_to_Nearby_HomeGoods,na.rm=TRUE)
HG_can %>%
  ggplot() +
  geom_bar((aes(x=as.factor(num_nearby_HomeGoods),y=Avg_Visit)),stat="identity",fill="#C51F3E",colour="white",alpha=0.95)+
  geom_line(aes(x=as.factor(num_nearby_HomeGoods),y=Avg_Visit_to_Nearby_HomeGoods*sfactor3),stat="identity",group = 1, color = "#FFD100",size=1.5,,alpha=0.95)+
  scale_y_continuous(labels = label_number(suffix = "K", scale = 1e-3),
                     "Average Visits", 
                     sec.axis = sec_axis(trans= ~./sfactor, 
                                         name = "Nearby HomeGoods Average Visit",
                                         labels = label_number(suffix = "K", scale = 1e-3)))+
  xlab("Number of Nearby HomeGoods")+
  ggtitle("More HomeGoods Nearby Stores Boost More Visits")+
  theme(axis.text=element_text(size=14),
        axis.title=element_text(size=14,face="bold"),
        plot.title = element_text(size = 30, face = "bold"),
        axis.line = element_line(color = "black"),
        axis.line.y = element_line())

census_income_df = read.csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Final_Data/census_income.csv")

census_income_df %>% filter(Name == "HomeGoods") %>%
  ggplot() +
  geom_point(aes(x=Household_Income_0.25K,y=Total_Visits), color = "#ed5564") + 
  geom_smooth(aes(Household_Income_0.25K,Total_Visits),method=lm,color = "#ed5564")+
  geom_point(aes(x=Household_Income_25K.50K,y=Total_Visits), color = "#ffce54") +
  geom_smooth(aes(Household_Income_25K.50K,Total_Visits),method=lm,color = "#ffce54")+
  geom_point(aes(x=Household_Income_50K.75K,y=Total_Visits), color = "#a0d568") +
  geom_smooth(aes(Household_Income_50K.75K,Total_Visits),method=lm,color = "#a0d568")+
  geom_point(aes(x=Household_Income_75K.100K,y=Total_Visits), color = "#4fc1e8")+
  geom_smooth(aes(Household_Income_75K.100K,Total_Visits),method=lm,color = "#4fc1e8")+
  geom_point(aes(x=Household_Income_100K.150K,y=Total_Visits), color = "#ac92eb") +
  geom_smooth(aes(Household_Income_100K.150K,Total_Visits),method=lm,color = "#ac92eb")+
  geom_point(aes(x=Household_Income_150K.,y=Total_Visits), color = "#c132ab")+
  geom_smooth(aes(Household_Income_150K.,Total_Visits),method=lm,color = "#c132ab")

starbucksdf <- read.csv("/Users/tomvdo29/Desktop/Consulting Project/Data/Final_Data/starbucks.csv")
  
starbucksdf %>%
  select(Name, Total_Visits,num_starbucks) %>%
  group_by(num_starbucks,Name) %>%
  summarise(avg_visit = mean(Total_Visits)) %>%
  ggplot(aes(x=as.factor(num_starbucks),y=avg_visit, fill=Name)) +
  geom_col(position = "dodge", color = "black") +
  scale_fill_manual(values = c("HomeGoods" = "#C51F3E",
                               "T.J. Maxx" = "#C40D11",
                               "Marshalls" = "#182C54"))+
  xlab("Number of Nearby Starbucks")+
  ylab("Average Visit")+
  ggtitle("Nearby Starbucks Increase Visits To TJX Stores")+
  theme(axis.text=element_text(size=14),
        axis.title=element_text(size=14,face="bold"),
        plot.title = element_text(size = 30, face = "bold"),
        axis.line = element_line(color = "black"),
        axis.line.y = element_line())
                                       
                                       