library(shiny)

ui <- shinyUI(
  fluidPage(
    titlePanel("Hello Shiny"),
    
    sidebarLayout(
      
      sidebarPanel(
        
        sliderInput(inputId = "bins",
                    label = "Number of bins:",
                    min = 1,
                    max = 40,
                    value = 20),
        hr(),
        h3("test"),
        h3("你好")
      ),
      
      mainPanel(
        
        plotOutput(outputId = "distplot")
      )
    )
  )
)

server <- shinyServer(function(input, output) {
  
  output$distplot <- renderPlot({
    
    x <- faithful$waiting
    bins <- seq(min(x), max(x), length.out = input$bins +1)
    hist(x, breaks = bins, col = "#75AADB", border = "white",
         xlab = "waiting times (min)",
         main = "Histogram of waiting times")
  })
})

shinyApp(ui, server)