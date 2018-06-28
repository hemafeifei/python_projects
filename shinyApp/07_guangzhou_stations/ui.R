library(leaflet)
library(dplyr)
library(raster)
library(shiny)
library(plotly)
library(data.table)

lines_colors <- data.frame("line_id" = c(1,2,3,30,4,5,6,7,8,60,68), "colors" =c('#F9E103','#0066CC','#EA6632','#EA6632','#139E13','#F00061','#8B1F5C','#42A480','#00C183','#CAE78E','#00A1CB'))
shinyUI(navbarPage("GZMetro_by Wei",
                         tabPanel("Entrance",
                                  div(class="outer",
                                      
                                      #tags$style(type = "text/css", "html, body {width:100%;height:100%}"),
                                      tags$style(type = "text/css", ".outer {position: fixed; top: 41px; left: 0; right: 0; bottom: 0; overflow: hidden; padding: 0}"),
                                      
                                      leafletOutput("map", width = "100%", height = "100%"),
                                      absolutePanel(top = 10, right = 10,
                                                    h4(textOutput("output_slider_time")),
                                                    sliderInput("slider_time", "Time:",
                                                                min = as.POSIXct(5*60*60, origin = "2017-03-20", tz = "GMT"),
                                                                max = as.POSIXct(24*60*60, origin = "2017-03-27", tz = "GMT"),
                                                                value = as.POSIXct(5*60*60, origin = "2017-03-23", tz = "GMT"),
                                                                step = 60*60,
                                                                timeFormat = "%d",
                                                                timezone = "GMT"),
                                                    selectInput("select_line", "Line",
                                                                c("All",lines_colors$line_id)),
                                                    h4("TOP 5"),
                                                    plotlyOutput("in_top5",height = 200, width = 300),
                                                    checkboxInput("legend", "Show legend", TRUE)
                                      )
                                  )
                         ),
                         tabPanel("Exit",
                                  div(class="outer",
                                      
                                      #tags$style(type = "text/css", "html, body {width:100%;height:100%}"),
                                      tags$style(type = "text/css", ".outer {position: fixed; top: 41px; left: 0; right: 0; bottom: 0; overflow: hidden; padding: 0}"),
                                      
                                      leafletOutput("map_out", width = "100%", height = "100%"),
                                      absolutePanel(top = 10, right = 10,
                                                    h4(textOutput("output_slider_time_out")),
                                                    sliderInput("slider_time_out", "Date:",
                                                               
                                                                min = as.POSIXct(5*60*60, origin = "2017-03-20", tz = "GMT"),
                                                                max = as.POSIXct(24*60*60, origin = "2017-03-27", tz = "GMT"),
                                                                value = as.POSIXct(5*60*60, origin = "2017-03-23", tz = "GMT"),
                                                                step = 24*60*60,
                                                                timeFormat = "%d",
                                                                timezone = "GMT"),
                                                    selectInput("select_line_out", "Line",
                                                                c("All",lines_colors$line_id)),
                                                    h4("TOP 5"),
                                                    plotlyOutput("out_top5",height = 200, width = 300),
                                                    checkboxInput("legend_out", "Show legend", TRUE)
                                      )
                                  )
                         )
                         
)
)