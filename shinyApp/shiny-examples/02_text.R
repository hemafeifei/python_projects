library(shiny)

ui <- shinyUI(
  fluidPage(
    titlePanel("Shiny Text-文本发布"),
    
    sidebarLayout(
      
      sidebarPanel(
        
        selectInput(inputId = "dataset",
                    label = "选择数据集:",
                    choices = c("rock", "pressure", "汽车")),
        
        numericInput(inputId = "obs",
                     label = "查看数据条数:",
                     value = 10)
      ),
      
      mainPanel(
        
        verbatimTextOutput("summary"),
        
        tableOutput("view")
      )
    )
  )
)

server <- shinyServer(function(input, output) {
  
  datasetInput <- reactive({
    switch(input$dataset,
           "rock" = rock,
           "pressure" = pressure,
           "汽车" = cars)
  })
  
  output$summary <- renderPrint({
    dataset <- datasetInput()
    summary(dataset)
  })
  
  output$view <- renderTable({
    head(datasetInput(), n= input$obs)
  })
})

shinyApp(ui, server)