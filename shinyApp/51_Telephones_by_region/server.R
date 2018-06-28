library(datasets)
shinyServer(function(input, output) {
  output$phonePlot <- renderPlot({
    barplot(WorldPhones[,input$region]*1000,
            main = input$region,
            ylab = "Number of Telephones",
            xlab = "Year")
  })
})