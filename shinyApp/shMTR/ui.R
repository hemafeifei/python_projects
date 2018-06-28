library(shiny)

shinyUI(navbarPage("SHMetro",
                   tabPanel("进站流量",
                            div(class="outer",
                                
                                #tags$style(type = "text/css", "html, body {width:100%;height:100%}"),
                                tags$style(type = "text/css", ".outer {position: fixed; top: 41px; left: 0; right: 0; bottom: 0; overflow: hidden; padding: 0}"),
                                
                                leafletOutput("map", width = "100%", height = "100%"),
                                absolutePanel(top = 10, right = 10,
                                              h4(textOutput("output_slider_time")),
                                              sliderInput("slider_time", "Time:",
                                                          #min=as.POSIXct(min(filter(shmetro_in, M5>30)$M5)*5*60, origin = "2015-04-01", tz = "GMT"),
                                                          #max=as.POSIXct(max(shmetro_in$M5)*5*60, origin = "2015-04-01", tz = "GMT"),
                                                          #value=as.POSIXct(min(shmetro_in$M5)*5*60, origin = "2015-04-01", tz = "GMT"),
                                                          min = as.POSIXct(5*60*60, origin = "2015-04-01", tz = "GMT"),
                                                          max = as.POSIXct(24*60*60, origin = "2015-04-01", tz = "GMT"),
                                                          value = as.POSIXct(5*60*60, origin = "2015-04-01", tz = "GMT"),
                                                          step = 60*5,
                                                          timeFormat = "%T",
                                                          timezone = "GMT"),
                                              selectInput("select_line", "Line",
                                                          c("All",lines_color$LINE)),
                                              h4("TOP 5"),
                                              plotlyOutput("in_top5",height = 200),
                                              checkboxInput("legend", "Show legend", TRUE)
                                )
                            )
                   ),
                   tabPanel("出站流量",
                            div(class="outer",
                                
                                #tags$style(type = "text/css", "html, body {width:100%;height:100%}"),
                                tags$style(type = "text/css", ".outer {position: fixed; top: 41px; left: 0; right: 0; bottom: 0; overflow: hidden; padding: 0}"),
                                
                                leafletOutput("map_out", width = "100%", height = "100%"),
                                absolutePanel(top = 10, right = 10,
                                              h4(textOutput("output_slider_time_out")),
                                              sliderInput("slider_time_out", "Time:",
                                                          #min=as.POSIXct(min(filter(shmetro_in, M5>30)$M5)*5*60, origin = "1960-01-01", tz = "GMT"),
                                                          #max=as.POSIXct(max(shmetro_in$M5)*5*60, origin = "1960-01-01", tz = "GMT"),
                                                          #value=as.POSIXct(min(shmetro_in$M5)*5*60, origin = "1960-01-01", tz = "GMT"),
                                                          min = as.POSIXct(5*60*60, origin = "2015-04-01", tz = "GMT"),
                                                          max = as.POSIXct(24*60*60, origin = "2015-04-01", tz = "GMT"),
                                                          value = as.POSIXct(5*60*60, origin = "2015-04-01", tz = "GMT"),
                                                          step = 60*5,
                                                          timeFormat = "%T",
                                                          timezone = "GMT"),
                                              selectInput("select_line_out", "Line",
                                                          c("All",lines_color$line)),
                                              h4("TOP 5"),
                                              plotlyOutput("out_top5",height = 200),
                                              checkboxInput("legend_out", "Show legend", TRUE)
                                )
                            )
                   )
              
)
)

