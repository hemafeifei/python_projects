library(shiny)
library(shinydashboard)

ui <- shinyUI(dashboardPage(
  dashboardHeader(title = "Dashboard Page"),
  dashboardSidebar(
                   sliderInput("slider", "Slider:",
                               min = 1, max = 10, value =5, step=1),
                   selectInput("select", "Selection:", choices = c(letters[1:4]), selected = 'd'),
                   actionButton("submit", "Update",
                                style="color: #fff; background-color: #337ab7; border-color: #2e6da4")

  ),
  dashboardBody(
    fluidRow(
      box(title = "Box title", "Box content",
          leafletOutput("map"), width = 300)
      # box(status = "warning", "Box content")
    ),
    
    fluidRow(
      box(
        title = "Title 1", width = 4, solidHeader = TRUE, status = "primary",
        "Box content"
      ),
      box(
        title = "Title 2", width = 4, solidHeader = TRUE,
        "Box content"
      ),
      box(
        title = "Title 1", width = 4, solidHeader = TRUE, status = "warning",
        "Box content"


  )))

))

server <- shinyServer(function(input, output, session) {
  
  output$map <- renderLeaflet({
    leaflet()%>% addProviderTiles(providers$Hydda.Base)%>%
      addCircles(data = stations, ~wgs_lng, ~wgs_lat, col = 'red')
    
  })
  
  
})

shinyApp(ui, server)