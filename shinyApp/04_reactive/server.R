shinyServer(function(input, output) {
  
  output$text1 <- renderText({ 
    paste("You have selected:", input$var)
    

  })
  
  output$text2 <- renderText({ 
  
    paste("You have also selected:", input$range[1], "to", input$range[2])
  })
  
}
)