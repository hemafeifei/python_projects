library(shiny)

# load datasets
origin <- read.csv("C:/Users/Administrator/PycharmProjects/untitled/df2_O_merge.csv",encoding ="gbk")
stations <- read.csv("C:/Users/Administrator/PycharmProjects/untitled/SH_M1M2.csv",encoding ="gbk")

# draw shanghai basemap
Shanghai <- leaflet() %>% 
  setView(lng = 121.60, lat = 31.20, zoom = 10) %>% 
  addProviderTiles("CartoDB.Positron") %>%
  addLegend(position = "bottomleft",pal=pal,values = stations$LINE)

# set shiny server
shinyServer(function(input, output, session){
  filteredData <- reactive({
    if(input$select_line=="ALL"){
      origin 
    }else{
      origin %>% filter(LINE==as.numeric(input$select_line))
      }
  })
  stations_in_top5 <- reactive({
    filteredData() %>%
      summarise(count= FEES, line=min(line)) %>%
      arrange(desc(count)) %>%
      head(5) %>%
      as.data.frame()
    })
# time
  output$output_slider_time <- renderText({
    paste0("Time: ", format(input$slider_time, "%H:%M:%S"))
  })
# map
  output$map <- renderLeaflet({
    Shanghai %>%
      addCircles(data=origin,lng= ~LON, lat = ~LAT, radius = ~FEES/10, color = ~pal(origin$LINE),
                 stroke = FALSE, weight =2) %>% clearMarkerClusters() %>% clearMarkers()
    })
  output$in_top5 <- renderPlotly({
    if (nrow(stations_in_top5())==0)
        return(NULL)
       
    plot_ly(stations_in_top5(),
            x=stations_in_top5()$STATION,
            y = stations_in_top5()$FEES,
            type = "bar",
            marker = list(color = pal(stations_in_top5()$LINE)),
            bgcolor = "#00FFFFFF")
   })
  
}
)