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
    navbarPage("Navbar Page",
               tabPanel("Origin",
                            leafletOutput("map",  height = 700)

                        
               ),
               tabPanel("Destination"),
               navbarMenu("More",
                          tabPanel("Summary"),
                          "----",
                          "Section header",
                          tabPanel("Table")
               )
    )
)

))

server <- shinyServer(function(input, output, session) {
  
  output$map <- renderLeaflet({
    leaflet()%>% addProviderTiles(providers$Hydda.Base)%>%
      addCircles(data = stations, ~wgs_lng, ~wgs_lat, col = 'red')
    
  })
  
  
})

shinyApp(ui, server)