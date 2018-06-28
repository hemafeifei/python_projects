library(shiny)
library(leaflet)
# stations <- read.csv('D:/R/shinyAPP/02_od_plot/data/station_location.txt')
ui <- shinyUI(bootstrapPage(
  tags$style(type = "text/css", "html, body {width:100%;height:100%}"),
  leafletOutput("map", width = "100%", height = "90%"),
  absolutePanel(top = 15, right = 10,
                sliderInput("slider", "Slider:",
                            min = 1, max = 10, value =5, step=1),
                selectInput("select", "Selection:", choices = c(letters[1:4]), selected = 'd'),
                actionButton("submit", "Update",
                             style="color: #fff; background-color: #337ab7; border-color: #2e6da4")),
  h4("Note: make with R Shiny")

  
))

server <- shinyServer(function(input, output, session) {
  output$map <- renderLeaflet({
      leaflet()%>% addProviderTiles(providers$Hydda.Base)%>%
        addCircles(data = stations, ~wgs_lng, ~wgs_lat, col = 'red')
    
  })
  
})

shinyApp(ui, server)

