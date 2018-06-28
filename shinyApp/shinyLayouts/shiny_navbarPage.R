library(shiny)
library(leaflet)

ui <- shinyUI(
  navbarPage("Navbar Page",
             tabPanel("Origin",
                      div(class = "outer",
                      tags$style(type = "text/css", ".outer {position: fixed; top: 41px; left: 0; right: 0; bottom: 0; overflow: hidden; padding: 0}"),
                      leafletOutput("map", width = '100%', height = '100%'),
                      absolutePanel(top = 15, right = 10,
                                    sliderInput("slider", "Slider:",
                                                min = 1, max = 10, value =5, step=1),
                                    selectInput("select", "Selection:", choices = c(letters[1:4]), selected = 'd'),
                                    actionButton("submit", "Update",
                                                 style="color: #fff; background-color: #337ab7; border-color: #2e6da4"))
                          )
                      # tags$style(type = "text/css", ".outer {position: fixed; top: 41px; left: 0; right: 0; bottom: 0; overflow: hidden; padding: 0}"),
                      # leafletOutput("map", width = 1920, height = 1080)
                      
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

server <- shinyServer(function(input, output, session) {
  
  output$map <- renderLeaflet({
    leaflet()%>% addProviderTiles(providers$Hydda.Base)%>%
      addCircles(data = stations, ~wgs_lng, ~wgs_lat, col = 'red')
  })
  
})


shinyApp(ui, server)