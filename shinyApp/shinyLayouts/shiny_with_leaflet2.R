library(shiny)
library(leaflet)
library(RColorBrewer)

ui <- shinyUI(
  bootstrapPage(
    tags$style(type = "text/css", "html, body {width:100%;height:100%}"),
    leafletOutput("map", width = "100%", height = "80%"),
    absolutePanel(top = 10, right = 10,
                  sliderInput("range", "Manitudes",
                              min(quakes$mag), max(quakes$mag),
                              value = range(quakes$mag), step = 0.1),
                  selectInput("colors", "Color Scheme",
                              rownames(subset(brewer.pal.info, category %in% c("seq","div")))),
                  
                  checkboxInput("legend", "Show Legend", TRUE)
                  
                  )
  )
)


server <- shinyServer(function(input, output, session) {
  
  output$map <- renderLeaflet({
    leaflet(quakes)%>% addTiles()%>%
      fitBounds(~min(long), ~min(lat), ~max(long), ~max(lat))
    
  })
})

shinyApp(ui, server)