library(shiny)

shinyUI(fluidPage(
  titlePanel("stockVis"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("Select a stock to examine. 
        Information will be collected from Google finance."),
    
      textInput("symb", "Symbol", "AAPL"),
    
      dateRangeInput("dates", 
        "Date range",
        start = "2017-01-01", 
        end = as.character(Sys.Date())),
      
      br(),
      br(),
      
      checkboxInput("log", "Plot y axis on log scale", 
        value = FALSE),
      
      checkboxInput("adjust", 
        "Adjust prices for inflation", value = FALSE)
    ),
    
    mainPanel(plotOutput("plot"))
  )
))