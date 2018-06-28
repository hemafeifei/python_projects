library(datasets)
shinyUI(
  fluidPage(
    titlePanel("telephone numbers by region"),
    sidebarLayout(
      sidebarPanel(
        selectInput("region", "Region:",choices = colnames(WorldPhones)),
        # hr(),
        helpText("Data from AT&T (1961) The Worlds's Telephones")
      ),
      mainPanel(
        plotOutput("phonePlot")
      )
    )
  )
)