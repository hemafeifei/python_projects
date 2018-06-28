library(shiny)

shinyServer(function(input, output) {
  
  output$distPlot <- renderPlot({
    
    x <- faithful[, 2]
    bins <- seq(min(x), max(x), length.out = input$bins +1)
    color <- input$color
    hist(x, breaks = bins, col = color, border = 'white' )
  })
})