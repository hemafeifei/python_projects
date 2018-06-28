shinyUI(pageWithSidebar(
  headerPanel("Iris k-means clustering by Wei"),
  sidebarPanel(
    selectInput('xcol', '设置X 变量', names(iris)),
    selectInput('ycol', '设置Y 变量', names(iris),
                selected = names(iris)[[2]]),
    numericInput('clusters', 'Cluster count', 3,
                 min = 1, max= 9)
  ),
  mainPanel(
    plotOutput('plot1')
  )
))