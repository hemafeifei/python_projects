library(shiny)
ui <- fluidPage(
  sliderInput(
    inputId = "num",
    label = "Choose a number",
    value = 25, min = 1, max = 100
  ),
  plotOutput("hist"),
  verbatimTextOutput("stats")
)


server <- function(input, output) {
  
  data <- reactive({
    rnorm(input$num)
  })
  
  output$hist <- renderPlot({
    title <- "100 random normal values"
    hist(data(), main = title)
  })
  
  output$stats <- renderPrint({
    summary(data())
  })
  
}

shinyApp(server = server, ui = ui)
