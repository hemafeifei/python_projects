# server.R

library(quantmod)
source("helpers.R")

shinyServer(function(input, output) {
  
  dataInput <- reactive({
    getSymbols(input$symb, src = "google", 
               from = input$dates[1],
               to = input$dates[2],
               auto.assign = FALSE)})
  # data2 <- reactive({
  #   data2 <- dataInput()
  #   if (input$adjust) data2 <- adjust(dataInput())
  # })
  
  finalInput <- reactive({
    if (!input$adjust) return(dataInput())
    adjust(dataInput())
  })

  output$plot <- renderPlot({
    chartSeries(finalInput(), theme = chartTheme("white"), 
      type = "line", log.scale = input$log, TA = NULL)
  })
  
})