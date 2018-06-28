library(shiny)
library(leaflet)
# stations <- read.csv('D:/R/shinyAPP/02_od_plot/data/station_location.txt')

ui <- shinyUI(
  fluidPage(titlePanel("This is title"),
    sidebarLayout(
      sidebarPanel(
        sliderInput("slider", "Slider:",
                    min = 1, max = 10, value =5, step=1),
        selectInput("select", "Selection:", choices = c(letters[1:4]), selected = 'd'),
        actionButton("submit", "Update")
      ),
      mainPanel(

        leafletOutput("map", height = 800),
        h4("make with R Shiny, fluidPage")
        
      )
    )
  )
)

server <- shinyServer(function(input, output, session) {
  
  output$map <- renderLeaflet({
    leaflet()%>% addProviderTiles(providers$Stamen.TonerLite)%>%
      addCircles(data = stations, ~wgs_lng, ~wgs_lat)
  }) 
  
})

shinyApp(ui, server)