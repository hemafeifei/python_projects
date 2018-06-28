library(shiny)
library(leaflet)

stations <- read.csv('data/station_location.txt', 
                     encoding = "utf8", colClasses = c("character", "character","character", rep("numeric",2)))

shinyUI(
  navbarPage("OD distribution",
             tabPanel("Origin 客流去向",
                      fluidRow(
                        column(8,
                               leafletOutput("map", height = "400px")),
                        column(4,
                               dateInput("date", "Date",
                                         value = "2014-07-02",
                                         language = "zh-CN",weekstart = 1),
                               selectInput("select_line","Select Line:",
                                           choices = unique(stations$line_id),
                                           selected = head(unique(stations$line_id),1)
                                           ),
                               selectInput("select_station", "Station Name",
                                           c("Item A", "Item B", "Item C")),
                               # uiOutput("station_name"),
                               selectInput("color", "OD Line Color:",
                                           choices = c('red','blue','turquoise'), selected = 'tuiquoise'),
                               # tags$head(
                               #   tags$style(HTML('#run{background-color:orange}'))
                               # ),

                               actionButton("submit", "更新",  
                                            style="color: #fff; background-color: #337ab7; border-color: #2e6da4"),
                               h4("Top10 去向"),
                               tableOutput("table")
                               
                               )
            
                      )),
             tabPanel("Destination 客流来源",
                      fluidRow(
                        column(8,
                               leafletOutput("map2", height = "400px")),
                        column(4,
                               dateInput("date2", "Date",
                                         value = "2014-07-02",
                                         language = "zh-CN",weekstart = 1),
                               selectInput("select_line2","Select Line:",
                                           choices = unique(stations$line_id),
                                           selected = head(unique(stations$line_id),1)
                               ),
                               selectInput("select_station2", "Station Name",
                                           c("Item A", "Item B", "Item C")),
                               # uiOutput("station_name"),
                               selectInput("color2", "OD Line Color:",
                                           choices = c('red','blue','turquoise'), selected = 'tuiquoise'),
                               actionButton("submit2", "更新",
                                            style="color: #fff; background-color: #337ab7; border-color: #2e6da4"),
                               h4("Top10 来源"),
                               tableOutput("table2")
                               
                        )
                        
                      ))
                      
                      )

)

