library(shiny)

shinyUI(fluidPage(
  
  titlePanel("Hello Shiny"),
  
  sidebarLayout(
    
    sidebarPanel(
      
      sliderInput("bins", "Number of bins:",
                  min = 1, max = 50, value = 15),
      
      selectInput("color", "Setting displot color: ",
                  choices = c('darkgray', 'skyblue'))
    ),

    mainPanel(
      
      plotOutput("distPlot")
    )
  )
))