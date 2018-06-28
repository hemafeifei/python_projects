library(shiny)
shinyUI(fluidPage(
  
  fluidRow(
    
    column(3, h3("Buttons"), actionButton("action", label = "Action"),
           br(),
           br(),
           submitButton("Submit")),
    
    column(3, h3("Single checkbox"), 
           checkboxInput("checkbox", label = "Choice A", value = TRUE)),
    
    column(3, checkboxGroupInput("checkGroup", 
                                 label = h3("Checkbox group"),
                                 choices = list("Choice 1" =1, "Choice 2" =2, "Choice 3" =3),
                                 selected = 1)),
    
    column(3, dateInput("date",
                        label = h3("Calender Date input"),
                        value = "2017-07-31"))
           
  ),
  
  fluidRow(
    
    column(3, dateRangeInput("dates", label = h3("Date Periods"))),
    
    column(3, fileInput("file", label = h3("File input"))),
    
    column(3, h3("Help text"), helpText("Note: help text isn't a true widget,",
                                        "but is provides an easy way to add text to",
                                        "accompany other widgets")),
    
    column(3, numericInput("num", label = h3("Numberic input"), value = 1))
  ),
  
  fluidRow(
    
    column(3, radioButtons("radio", label =h3("Radio buttons"),
                            choices = list("Choice 1" = 1, "Choice 2" = 2,
                                           "Choice 3" = 3), selected =1)),
    
    column(3, selectInput("select", label = h3("Select box"),
                          choices = list("Choice 1" = 1, "Choice 2" = 2,
                                         "Choice 3" = 3), selected =1)),
    
    column(3, sliderInput("slider1", label = h3("Sliders"),
                          min = 0, max = 100, value = 30),
              sliderInput("slider2", "",
                          min = 0, max = 100, value = c(25, 75))),
    
    column(3, textInput("text", label = h3("Text input"),
                        value = "输入信息"))
  )
  
))