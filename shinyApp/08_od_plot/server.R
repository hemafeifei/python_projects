library(shiny)
library(leaflet)
library(raster)
library(dplyr)
library(DBI)
library(rJava)
library(RJDBC)
library(geosphere)
library(RColorBrewer)

stations <- read.csv('data/station_location.txt', 
                     encoding = "utf8", colClasses = c("character", "character","character", rep("numeric",2)))

district <- shapefile('data/gz_district.shp', encoding = "utf8")
#set driver
drv <-JDBC("oracle.jdbc.driver.OracleDriver", "D:/R/ojdbc8.jar", identifier.quote="\"")
#set connection
conn<-dbConnect(drv,"jdbc:oracle:thin:@172.20.10.178:1521/dwpdb","dw","Admin123")#172.20.10.178

shinyServer(function(input, output, session) {
  
  output$map <- renderLeaflet({
    # map <- leaflet() %>% addProviderTiles("CartoDB.Positron")
    leaflet() %>% addProviderTiles("CartoDB.Positron")%>% 
      # addCircles(data=stations,~wgs_lng, ~wgs_lat)
      addCircleMarkers(stations$wgs_lng, stations$wgs_lat, radius = 0.2, col = "grey")
    
  })
  
  filteredData_date <- reactive({
    sql_1 <- "select start_line_id, start_station_id, end_line_id, end_station_id,
    sum(num) as ctn from tam_flux_od where (SQUAD_DATE ="
    sql_4 <- ") group by start_line_id, start_station_id,  END_LINE_ID,
    END_STATION_ID order by ctn desc"
    dbGetQuery(conn, paste(sql_1, gsub('-','',as.character(input$date)), sql_4, sep = ""))
    
  })    
  
  observe({
    x <- input$select_line
    if(is.null(x)){
      y <- character(0)
    }
    else{
      mydata <- stations[stations$line_id==x,]
      y1<-mydata$name
      y<-y1
    }
    
    updateSelectInput(session, "select_station",
                      label = paste("Select Station"),
                      choices = y,
                      selected = head(y,1)
    )
  })
  
  
  mydata11 <- reactive({
    
    # df<-stations[(stations[,3]==input$inSelect)&(stations[,1]==input$select_line),]
    if (is.null(input$select_line))
      return(NULL)
    sta <- stations[stations$line_id == input$select_line,]
    sta[sta[,3]==(input$select_station),]
  })
  

  
  od <- reactive({
    filteredData <- filteredData_date()
    mydata <- mydata11()
    
    if (length(filteredData) == 0 | length(mydata) ==0)
      return(NULL)
    empl1 <- filteredData[(filteredData[,1] == mydata[,1])&(filteredData[,2] == mydata[,2]),] %>% as.data.frame()
    if (length(empl1[,1])>1) {
      df2 <-na.omit(empl1) %>% 
        slice(2:11) %>% 
        left_join(stations, by = c("END_LINE_ID" = "line_id", "END_STATION_ID"="station_id" ))
      df2 <-na.omit(df2)
      
      df2$origin <- as.character(input$select_station)
      df2 <- df2 %>% left_join(stations[,c(-3)],  by = c("START_LINE_ID" = "line_id", "START_STATION_ID"="station_id" ))
      df2 <- df2[!duplicated(df2),] %>% as.data.frame()
    }else{
      data.frame()
    }
  })
  
  
  flow<- eventReactive(input$submit,{
    if(length(od())>1){
      df2<-od()
      flows<-gcIntermediate(df2[,10:11], df2[,7:8], sp = TRUE, addStartEnd = TRUE)
      flows$origins <- df2$origin
      flows$destinations <- df2$name
      flows$counts <- as.integer(df2$CTN)
      flows
    }else{
      data.frame()
    }
  })
  
  output$table <- renderTable({ flow()
  })

  observe({
    if(mode(flow())=="S4"){
      if(length(flow()@data)>1){
        flows<-flow()
        hover <- paste0(flows$origins, " to ",
                        flows$destinations, ': ',
                        as.character(flows$counts))
        # pal <- colorFactor(brewer.pal(10, 'Paired'), flows@data$destinations)
        
        leafletProxy("map")%>%
          clearShapes() %>%
          addProviderTiles("CartoDB.Positron")%>%
          # addCircleMarkers(stations$wgs_lng, stations$wgs_lat, radius = 1, col = "grey")%>%
          addPolygons(data=district,weight = 0.5, smoothFactor = 0.5, fillColor = "transparent") %>% 
          addPolylines(data = flows, weight = ~(counts/200), label = hover, color = input$color)
        
      }
    }
  })
  
  ###########################################
  #destination server
  output$map2 <- renderLeaflet({
    # map <- leaflet() %>% addProviderTiles("CartoDB.Positron")
    leaflet() %>% addProviderTiles("providers$Hydda.Base")%>% 
      # addCircles(data=stations,~wgs_lng, ~wgs_lat)
      addCircleMarkers(stations$wgs_lng, stations$wgs_lat, radius = 0.2, col = "grey")
    
  })
  
  filteredData_date2 <- reactive({
    sql_1 <- "select start_line_id, start_station_id, end_line_id, end_station_id,
    sum(num) as ctn from tam_flux_od where (SQUAD_DATE ="
    sql_4 <- ") group by start_line_id, start_station_id,  END_LINE_ID,
    END_STATION_ID order by ctn desc"
    dbGetQuery(conn, paste(sql_1, gsub('-','',as.character(input$date2)), sql_4, sep = ""))
    
  })    
  
  observe({
    x <- input$select_line2
    if(is.null(x)){
      y <- character(0)
    }
    else{
      mydata <- stations[stations$line_id==x,]
      y1<-mydata$name
      y<-y1
    }
    
    updateSelectInput(session, "select_station2",
                      label = paste("Select Station"),
                      choices = y,
                      selected = head(y,1)
    )
  })
  
  
  mydata12 <- reactive({
    
    # df<-stations[(stations[,3]==input$inSelect)&(stations[,1]==input$select_line),]
    if (is.null(input$select_line2))
      return(NULL)
    sta <- stations[stations$line_id == input$select_line2,]
    sta[sta[,3]==(input$select_station2),]
  })
  
  
  
  od_2 <- reactive({
    filteredData <- filteredData_date2()
    mydata <- mydata12()
    
    if (length(filteredData) == 0 | length(mydata) ==0)
      return(NULL)
    empl1 <- filteredData[(filteredData[,3] == mydata[,1])&(filteredData[,4] == mydata[,2]),] %>% as.data.frame()
    if (length(empl1[,1])>1) {
      df2 <-na.omit(empl1) %>% 
        slice(2:11) %>% 
        left_join(stations, by = c("START_LINE_ID" = "line_id", "START_STATION_ID"="station_id" ))
      df2 <-na.omit(df2)
      
      df2$destination <- as.character(input$select_station)
      df2 <- df2 %>% left_join(stations[,c(-3)],  by = c("END_LINE_ID" = "line_id", "END_STATION_ID"="station_id" ))
      df2 <- df2[!duplicated(df2),] %>% as.data.frame()
    }else{
      data.frame()
    }
  })
  
  
  flow_2<- eventReactive(input$submit2,{
    if(length(od_2())>1){
      df2<-od_2()
      flows<-gcIntermediate(df2[,10:11], df2[,7:8], sp = TRUE, addStartEnd = TRUE)
      flows$origins <- df2$name
      flows$destinations <- df2$destination
      flows$counts <- as.integer(df2$CTN)
      flows
    }else{
      data.frame()
    }
  })
  
  output$table2 <- renderTable({ flow_2()
  })
  
  observe({
    if(mode(flow_2())=="S4"){
      if(length(flow_2()@data)>1){
        flows<-flow_2()
        hover <- paste0(flows$origins, " to ",
                        flows$destinations, ': ',
                        as.character(flows$counts))
        # pal <- colorFactor(brewer.pal(10, 'Paired'), flows@data$destinations)
        
        leafletProxy("map2")%>%
          clearShapes() %>%
          addProviderTiles("CartoDB.Positron")%>%
          # addCircleMarkers(stations$wgs_lng, stations$wgs_lat, radius = 1, col = "grey")%>%
          addPolygons(data=district,weight = 0.5, smoothFactor = 0.5, fillColor = "transparent") %>% 
          addPolylines(data = flows, weight = ~(counts/200), label = hover, color = input$color2)
        
      }
    }
  })
  
})