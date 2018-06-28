
server <- function(input, output, session) {
  acm_defaults <- function(map, x, y) addCircleMarkers(map, x, y, radius = 6, color = "black", fillOpacity = 1, opacity = 1, weight = 2, stroke = TRUE, layerId = "Selected")
  
  output$map <- renderLeaflet({
    leaflet() %>% setView(lon, lat, 4) %>% addTiles() %>%
      addCircleMarkers(data=locs, radius = 6, color = "black", stroke=FALSE)
  })
}