
#required libraries
# library(sp)
# library(ggplot2)
library(leaflet)
library(dplyr)
# library(maptools)
# library(ggmap)
library(rgdal)
library(shiny)
library(plotly)
library(data.table)
library(networkD3)
library(parsetR)
library(geosphere)
library(RColorBrewer)
#load lujing
# load shapfile; csv data
district <- readOGR(dsn ='Daten/guangzhou_wgs84/gz_district.shp', encoding = "gbk")#块
metroLines  <- readOGR(dsn = 'Daten/guangzhou_merged/metroline_merged.shp',encoding = "gbk")#线

df_volume = read.csv('Daten/df_volume_plot.csv',sep=",")
df_volume1 = filter(df_volume, day =="2017-03-20")

metroLines$line_id<-as.character(metroLines$line_id)
metroLines<-metroLines[order(as.numeric(metroLines$line_id)),]
metroLines$line_id<-factor(metroLines$line_id,as.character(c(1:8,30,60,68)))#改换顺序
df_volume$line_id<-factor(df_volume$line_id,as.character(c(1:8,30,60,68)))


# set color palette
#lines_colors <- data.frame("line_id" = c(1,2,3,30,4,5,6,60,68,7,8), "colors" =c('#F9E103','#0066CC','#EA6632','#EA6632','#139E13','#F00061','#8B1F5C','#CAE78E','#00A1CB','#42A480','#00C183'))
#pal <- colorFactor(as.character(lines_colors$colors), domain=metroLines$line_id)
lines_color <- data.frame("line"=c(1:3,4:8,30,60,68),"color"=c("#F9E103","#0066CC",
                                                               "#EA6632","#139E13",
                                                               "#FF2C2C","#8B1F5C","#42A480","#00A1CC","#EA6632","#CAE78E","#00A1CB"),
                          mc=factor(c("地铁1号线","地铁2号线","地铁3号线","地铁4号线","地铁5号线","地铁6号线",
                                      "地铁7号线","地铁8号线","地铁3号线延长线","广佛线",
                                      "APM线"),levels=c("地铁1号线","地铁2号线","地铁3号线","地铁4号线","地铁5号线","地铁6号线",
                                                       "地铁7号线","地铁8号线","地铁3号线延长线","广佛线",
                                                       "APM线")))#构造线路颜色
pal1<- colorFactor(as.character(lines_color$color), domain=lines_color$mc)#修改图例

lines_colors1<- data.frame("line_id"=c(1:3,4:8,30,60,68),"colors"=c("#F9E103","#0066CC",
                                                                    "#EA6632","#139E13",
                                                                    "#FF2C2C","#8B1F5C","#42A480","#00A1CC","#EA6632","#CAE78E","#00A1CB"))

pal <- colorFactor(as.character(lines_colors1$colors), domain=metroLines$line_id)#地铁图例

stations  <- read.csv('Daten/station_baidu_gg_wgs84_modified.csv', encoding = "gbk")#站点基本信息

names(lines_color)[1]<-"line_id"
stations<-merge(stations,lines_color,by="line_id",all.x=T)
stations$mc<-factor(stations$mc,levels=c("地铁1号线","地铁2号线","地铁3号线","地铁4号线","地铁5号线","地铁6号线",
                                         "地铁7号线","地铁8号线","地铁3号线延长线","广佛线","APM线"))

gz_metro_station_lin <- readOGR(dsn ='Daten/gz_metro_station_line/gz_metro_station_lin.shp', encoding = "gbk")#断面拓展图

gz_metro_station_lin1<-fortify(gz_metro_station_lin)
data<-data.frame(group=unique(gz_metro_station_lin1$group),
                 sx=abs(rnorm(169,mean=0,sd=1)*1000),xq=abs(rnorm(169,mean=0,sd=1))*1000)#定义上下行数据量
data$VM<-data$sx+data$xq#总量
a<-rep(c("All","SX","XQ"),each=169)
b<-c(data$VM,data$sx,data$xq)
data1<-data.frame(level=a,sx=b,stringsAsFactors=F)

pal2 <- colorNumeric(c("darkgreen", "yellow","red"),as.numeric(data$sx))#断面量图例只定义上

dm_base_gz<-leaflet(gz_metro_station_lin) %>% addProviderTiles("CartoDB.Positron")%>%
  addPolygons(weight = 5,color=~pal2(as.numeric(data$sx)),fill=~as.numeric(data$sx)) %>% 
  addLegend(pal = pal2, values = data$sx,position="bottomright",
            title = "断面客流量（万人）") %>%
  addCircleMarkers(stations$wgs_lng, stations$wgs_lat,stroke = FALSE, 
                   popup=paste(stations$mc,as.character(stations$name),stations$station_id,sep=","), 
                   col="4",radius =1)#断面图

#metroLines<-fortify(metroLines)
#district <- fortify(district)
# draw basemap with district and Metrolines
base_gz <- leaflet(district) %>% addProviderTiles("CartoDB.Positron") %>% 
  addPolygons( weight = 0.5, smoothFactor = 0.5, fillColor = "transparent") %>% 
  addPolylines(data=metroLines,group =~line_id, color=~pal(line_id), weight = 5)


#metroLines<-fortify(metroLines)
#district <- fortify(district)
# draw basemap with district and Metrolines
base_gz <- leaflet(district) %>% addProviderTiles("CartoDB.Positron") %>% 
  addPolygons( weight = 0.5, smoothFactor = 0.5, fillColor = "transparent") %>% 
  addPolylines(data=metroLines,group =~line_id, color=~pal(line_id), weight = 5)#地图线基本图

# base_gz %>% addCircles(data=df_volume1,lng= ~wgs_lng, lat = ~wgs_lat, radius =~origin/80, color = ~pal(in_line), fillOpacity = 0.5,stroke = FALSE, popup=paste(df_volume1$name,df_volume1$origin,sep="\n"))


#base_gzz
base_gzz <- leaflet(district) %>% addProviderTiles("CartoDB.Positron") %>% 
  addPolygons( weight = 0.5, smoothFactor = 0.5, fillColor = "transparent") %>% 
  addCircleMarkers(stations$wgs_lng, stations$wgs_lat,stroke = F, radius=5,opacity=0.2,color = "black",
                   popup=paste(stations$mc,as.character(stations$name),stations$station_id,sep=","))


df4  <- read.csv("Daten/df3.csv")#OD数据
df3<-df4
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




ui <- navbarPage("GZMetro_by PCI DATA",
                         tabPanel("ORIGIN",
                                  div(class="outer",
                                      
                                      #tags$style(type = "text/css", "html, body {width:100%;height:100%}"),
                                      tags$style(type = "text/css", ".outer {position: fixed; top: 41px; left: 0; right: 0; bottom: 0; overflow: hidden; padding: 0}"),
                                      
                                      leafletOutput("map", width = "100%", height = "100%"),
                                      absolutePanel(top = 10, right = 10,
                                                    h4(textOutput("output_slider_time")),
                                                    sliderInput("slider_time", "Date:",
                                                                #min=as.POSIXct(min(filter(shmetro_in, M5>30)$M5)*5*60, origin = "2015-04-01", tz = "GMT"),
                                                                #max=as.POSIXct(max(shmetro_in$M5)*5*60, origin = "2015-04-01", tz = "GMT"),
                                                                #value=as.POSIXct(min(shmetro_in$M5)*5*60, origin = "2015-04-01", tz = "GMT"),
                                                                min = as.POSIXct(5*60*60, origin = "2017-03-20", tz = "GMT"),
                                                                max = as.POSIXct(24*60*60, origin = "2017-03-27", tz = "GMT"),
                                                                value = as.POSIXct(5*60*60, origin = "2017-03-20", tz = "GMT"),
                                                                step = 24*60*60,
                                                                timeFormat = "%d",
                                                                timezone = "GMT",animate=animationOptions(interval=3000, loop=T)),
                                                    selectInput("select_line", "Line",
                                                                c("All",lines_colors1$line_id)),
                                                    h4("TOP 5"),
                                                    plotlyOutput("in_top5",height = 200),
                                                    checkboxInput("legend", "Show legend", TRUE)
                                      )
                                  )
                         ),
                         tabPanel("DESTINATION",
                                  div(class="outer",
                                      
                                      #tags$style(type = "text/css", "html, body {width:100%;height:100%}"),
                                      tags$style(type = "text/css", ".outer {position: fixed; top: 41px; left: 0; right: 0; bottom: 0; overflow: hidden; padding: 0}"),
                                      
                                      leafletOutput("map_out", width = "100%", height = "100%"),
                                      absolutePanel(top = 10, right = 10,
                                                    h4(textOutput("output_slider_time_out")),
                                                    sliderInput("slider_time_out", "Date:",
                                                                #min=as.POSIXct(min(filter(shmetro_in, M5>30)$M5)*5*60, origin = "1960-01-01", tz = "GMT"),
                                                                #max=as.POSIXct(max(shmetro_in$M5)*5*60, origin = "1960-01-01", tz = "GMT"),
                                                                #value=as.POSIXct(min(shmetro_in$M5)*5*60, origin = "1960-01-01", tz = "GMT"),
                                                                min = as.POSIXct(5*60*60, origin = "2017-03-20", tz = "GMT"),
                                                                max = as.POSIXct(24*60*60, origin = "2017-03-27", tz = "GMT"),
                                                                value = as.POSIXct(5*60*60, origin = "2017-03-20", tz = "GMT"),
                                                                step = 24*60*60,
                                                                timeFormat = "%d",
                                                                timezone = "GMT",animate=animationOptions(interval=3000, loop=T)),
                                                    selectInput("select_line_out", "Line",
                                                                c("All",lines_colors1$line_id)),
                                                    h4("TOP 5"),
                                                    plotlyOutput("out_top5",height = 200),
                                                    checkboxInput("legend_out", "Show legend", TRUE)
                                      )
                                  )
                         )
                         ,
                         tabPanel("DUANMIAN",
                                  div(class="outer",
                                      
                                      #tags$style(type = "text/css", "html, body {width:100%;height:100%}"),
                                      tags$style(type = "text/css", ".outer {position: fixed; top: 41px; left: 0; right: 0; bottom: 0; overflow: hidden; padding: 0}"),
                                      
                                      leafletOutput("map_dm", width = "100%", height = "100%"),
                                      absolutePanel(top = 10, right = 10,
                                                    h4(textOutput("output_slider_time_dm")),
                                                    sliderInput("slider_time_dm", "Date:",
                                                                #min=as.POSIXct(min(filter(shmetro_in, M5>30)$M5)*5*60, origin = "1960-01-01", tz = "GMT"),
                                                                #max=as.POSIXct(max(shmetro_in$M5)*5*60, origin = "1960-01-01", tz = "GMT"),
                                                                #value=as.POSIXct(min(shmetro_in$M5)*5*60, origin = "1960-01-01", tz = "GMT"),
                                                                min = as.POSIXct(5*60*60, origin = "2017-03-20", tz = "GMT"),
                                                                max = as.POSIXct(24*60*60, origin = "2017-03-27", tz = "GMT"),
                                                                value = as.POSIXct(5*60*60, origin = "2017-03-20", tz = "GMT"),
                                                                step = 24*60*60,
                                                                timeFormat = "%d",
                                                                timezone = "GMT"),
                                                    selectInput("select_line_dm", "DS",
                                                                c(unique(data1$level))),
                                                    verbatimTextOutput("summary")
                                                    
                                      )
                                  )
                         ),
                         tabPanel("OD",
                                  div(class="outer",
                                      
                                      #tags$style(type = "text/css", "html, body {width:100%;height:100%}"),
                                      tags$style(type = "text/css", ".outer {position: fixed; top: 41px; left: 0; right: 0; bottom: 0; overflow: hidden; padding: 0}"),
                                      
                                      leafletOutput("map_od", width = "100%", height = "100%"),
                                      absolutePanel(top = 10, right = 10,
                                                    h4(textOutput("output_slider_time_od")),
                                                    sliderInput("slider_time_od", "Date:",
                                                                # min=as.POSIXct(min(filter(shmetro_in, M5>30)$M5)*5*60, origin = "1960-01-01", tz = "GMT"),
                                                                # max=as.POSIXct(max(shmetro_in$M5)*5*60, origin = "1960-01-01", tz = "GMT"),
                                                                # value=as.POSIXct(min(shmetro_in$M5)*5*60, origin = "1960-01-01", tz = "GMT"),
                                                                min = as.POSIXct(5*60*60, origin = "2017-03-20", tz = "GMT"),
                                                                max = as.POSIXct(24*60*60, origin = "2017-03-27", tz = "GMT"),
                                                                value = as.POSIXct(5*60*60, origin = "2017-03-20", tz = "GMT"),
                                                                step = 24*60*60,
                                                                timeFormat = "%d",
                                                                timezone = "GMT",animate=animationOptions(interval=3000, loop=T)),
                                                    selectInput("inCheckboxGroup", "Input checkbox",
                                                                unique(df4$orgins_id)),
                                                    checkboxGroupInput("inSelect", "Select input",
                                                                       c("Item A", "Item B", "Item C"))
                                      )
                                  )
                         )
                         
                         
)















# base_gz

# set serve
server<-function(input, output, session){
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
    paste0("Time: ", format(input$slider_time, format="%Y-%m-%d"))
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
      proxy %>%
        #addLegend(position = "bottomleft",pal=pal,values = metroLines$line_id)
        addLegend(position = "bottomleft",pal=pal1,values = lines_color$mc)
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
    paste0("Time: ", format(input$slider_time_out, format="%Y-%m-%d"))
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
      proxy %>% 
        addLegend(position = "bottomleft",pal=pal1,values = lines_color$mc)
      #addLegend(position = "bottomleft",pal=pal,values = metroLines$line_id)
    }
  })
  
  filteredData_dm <- reactive({
    data1%>%filter(level==as.character(input$select_line_dm))
  })
  
  
  
  # map
  output$map_dm <- renderLeaflet({
    data2<-filteredData_dm()
    pal2 <- colorNumeric(c("darkgreen", "yellow","red"),as.numeric(data2$sx))
    leaflet(gz_metro_station_lin) %>% addProviderTiles("CartoDB.Positron")%>%
      addPolygons(weight = as.numeric(data2$sx)/300,color=~pal2(as.numeric(data2$sx)),fill=~as.numeric(data2$sx)) %>% 
      addLegend(pal = pal2, values = data2$sx,position="bottomright",
                title = "people")
    # %>%
    #   addCircleMarkers(stations$wgs_lng, stations$wgs_lat,stroke = FALSE, 
    #                    popup=paste(stations$mc,as.character(stations$name),stations$station_id,sep=","), 
    #                    radius=2,col="4")
  })
  # map_od
  observe({
    x <- input$inCheckboxGroup
    
    # Can use character(0) to remove all choices
    if(is.null(x)){
      y <- character(0)
    }
    else{
      y1<- df4 %>% filter(orgins_id==x)
      y<-y1[,2]
    }
    # Can also set the label and select items
    updateCheckboxGroupInput(session, "inSelect",
                             label = paste("Select input label", length(y)),
                             choices = y,selected = tail(y, 1))
    
    output$map_od<-renderLeaflet({
      df3<-df4[df4[,2] %in% input$inSelect,]
      flows <- gcIntermediate(df3[,5:6], df3[,7:8], sp = TRUE, addStartEnd = TRUE)
      flows$counts <- df3$counts
      flows$origins <- df3$origins
      flows$destinations <- df3$destinations
      hover <- paste0(flows$origins, " to ", 
                      flows$destinations, ': ', 
                      as.character(flows$counts))
      palzz <- colorFactor(topo.colors(flows$origins), flows$origins)
      base_gzz %>%
        addPolylines(data = flows, weight = ~counts/10, label = hover, 
                     group = ~origins, color = ~palzz(origins))
      
    })
  })
  
  
}

shinyApp(ui=ui,server=server)




