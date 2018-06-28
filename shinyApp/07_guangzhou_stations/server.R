#required libraries
library(leaflet)
library(dplyr)
library(raster)
library(shiny)
library(plotly)
library(data.table)


# load shapfile; csv data
district <- shapefile('data/gz_district.shp', encoding = "gbk")
metroLines  <- shapefile('data/gz_metroline_osm_gbk.shp', encoding = "gbk")
df_volume = read.csv('data/df_volume_plot_gbk.txt', encoding = 'gbk')


# set color palette
lines_colors <- data.frame("line" = c(1,2,3,30,4,5,6,7,8,60,68), "colors" =c('#F9E103','#0066CC','#EA6632','#EA6632','#139E13','#F00061','#8B1F5C','#42A480','#00C183','#CAE78E','#00A1CB'))

pal <- colorFactor(as.character(lines_colors$colors), domain=metroLines$line, levels = c(1,2,3,30,4,5,6,7,8,60,68))

#district <- fortify(district)
# draw basemap with district and Metrolines
base_gz <- leaflet(district) %>% addProviderTiles("CartoDB.Positron") %>% 
  addPolygons( weight = 0.5, smoothFactor = 0.5, fillColor = "transparent") %>% 
  addPolylines(data=metroLines,group =~line, color=~pal(line), weight = 2)

# base_gz %>% addCircles(data=df_volume1,lng= ~wgs_lng, lat = ~wgs_lat, radius =~origin/80, color = ~pal(in_line), fillOpacity = 0.5,stroke = FALSE, popup=paste(df_volume1$name,df_volume1$origin,sep="\n"))



# set label
b <- list(x = 0, y = 1,bgcolor = "#00FFFFFF")
yax <- list(
  title = "",
  zeroline = FALSE,
  showline = FALSE,
  showticklabels = FALSE,
  showgrid = FALSE
)

xax <- list(
  title = "",
  titlefont = list(size = 8),
  tickangle = -20,
  color = "black"
)

shinyServer(function(input, output, session){
  filteredData <- reactive({
    if(input$select_line=="All"){
      df_volume
    }else{
      df_volume %>% filter(line_id==as.numeric(input$select_line))
    }
  })
  
  stations_in_top5 <- reactive({
    
    filteredData()[(format(filteredData()$day,format="%Y-%m-%d")) ==format(input$slider_time, format="%Y-%m-%d"), ] %>%
      # group_by(STATION) %>%
      # summarise(count=sum(FEES),LINE=min(LINE)) %>%
      arrange(desc(origin)) %>%
      head(5) %>%
      as.data.frame()
    
  })
  
  # stations_in_top5 <- reactive({
  #   data_in_circle1 <- filteredData()[(format(filteredData()$DT,format="%H:%M:%S")) ==format(input$slider_time, format="%H:%M:%S"), ]%>%
  #     #data_in_circle1<-df_origin%>%
  #     group_by(STATION) %>%
  #     summarise(count=sum(FEES),line=min(LINE)) %>%
  #     arrange(desc(count)).head(5) %>%
  #     as.data.frame()
  # })
  
  output$output_slider_time <- renderText({
    paste0("Date: ", format(input$slider_time, format="%Y-%m-%d"))
  })
  # map
  output$map <- renderLeaflet({
    base_gz 
  })
  observe({
    data_in_circle <- filteredData()[(format(filteredData()$day,format="%Y-%m-%d")) ==format(input$slider_time, format="%Y-%m-%d"), ]
    # subset(filteredData(), format(filteredData()$DT, format="%H:%M:%S")==format(input$slider_time, format="%H:%M:%S"))
    
    leafletProxy("map", data =data_in_circle)%>%
      clearMarkerClusters()%>%
      clearMarkers()%>%
      addCircleMarkers(data_in_circle$wgs_lng, data_in_circle$wgs_lat, color = pal(data_in_circle$line_id),fillOpacity = 0.5,stroke = FALSE, popup=paste(data_in_circle$line_id,data_in_circle$name, data_in_circle$origin,sep=","), radius=(data_in_circle$origin)/2400)
  })
  
  
  output$in_top5 <- renderPlotly({
    if (nrow(stations_in_top5())==0)
      return(NULL)
    
    plot_ly(stations_in_top5(),
            
            x=factor(as.character(stations_in_top5()$name),levels=as.character(stations_in_top5()$name)),
            y = stations_in_top5()$origin,
            type = "bar",
            marker = list(color = pal(stations_in_top5()$line_id)) ) %>%
      layout(showlegend=FALSE,
             yaxis=yax,xaxis=xax)
    
    
  })
  
  observe({
    proxy <- leafletProxy("map")
    # Remove any existing legend, and only if the legend is
    # enabled, create a new one.
    proxy %>% clearControls()
    if (input$legend) {
      # proxy %>% addLegend(position = "bottomleft",pal=pal,values = metroLines$name_cn)
      proxy %>% addLegend(position = "bottomleft",pal=pal,values = metroLines$line,labFormat = labelFormat(prefix = "line"))
    }
  })
  
  
  
  
  
  
  filteredData_Out <- reactive({
    if(input$select_line_out=="All"){
      df_volume
    }else{
      df_volume %>% filter(line_id==as.numeric(input$select_line_out))
    }
  })
  # stations_in_top5 <- reactive({
  #   filteredData() %>%
  #    origin[origin$LINE==??] %>%
  #     arrange(desc(count)) %>%
  #     head(5) %>%
  #     as.data.frame()
  # })
  
  stations_out_top5 <- reactive({
    
    filteredData_Out()[(format(filteredData_Out()$day,format="%Y-%m-%d")) ==format(input$slider_time_out, format="%Y-%m-%d"), ] %>%
      # group_by(STATION) %>%
      # summarise(count=sum(FEES),LINE=min(LINE)) %>%
      arrange(desc(destination)) %>%
      head(5) %>%
      as.data.frame()
    
  })
  # time
  output$output_slider_time_out <- renderText({
    paste0("Date: ", format(input$slider_time_out, format="%Y-%m-%d"))
  })
  # map
  output$map_out <- renderLeaflet({
    base_gz
  })
  
  
  observe({
    data_out_circle <- filteredData_Out()[(format(filteredData_Out()$day,format="%Y-%m-%d")) ==format(input$slider_time_out, format="%Y-%m-%d"), ]
    # subset(filteredData(), format(filteredData()$DT, format="%H:%M:%S")==format(input$slider_time, format="%H:%M:%S"))
    
    leafletProxy("map_out", data =data_out_circle)%>%
      clearMarkerClusters()%>%
      clearMarkers()%>%
      addCircleMarkers(data_out_circle$wgs_lng, data_out_circle$wgs_lat, color = pal(data_out_circle$line_id),fillOpacity = 0.5,stroke = FALSE, popup=paste(data_out_circle$line_id,data_out_circle$name, data_out_circle$destination,sep=","), radius=(data_out_circle$destination)/2400)
  }) 
  
  output$out_top5 <- renderPlotly({
    if (nrow(stations_out_top5())==0)
      return(NULL)
    
    plot_ly(stations_out_top5(),
            x=factor(as.character(stations_out_top5()$name),levels=as.character(stations_out_top5()$name)),
            
            y = stations_out_top5()$destination,
            type = "bar",
            marker = list(color = pal(stations_out_top5()$line_id)) ) %>%
      layout(showlegend=FALSE,
             yaxis=yax,xaxis=xax)
  })
  observe({
    proxy <- leafletProxy("map_out")
    # Remove any existing legend, and only if the legend is
    # enabled, create a new one.
    proxy %>% clearControls()
    if (input$legend_out) {
      # proxy %>% addLegend(position = "bottomleft",pal=pal,values = metroLines$name_cn)
      proxy %>% addLegend(position = "bottomleft",pal=pal,values = metroLines$line,labFormat = labelFormat(prefix = "line"))
    }
  })
})