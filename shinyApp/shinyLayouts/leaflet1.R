library(htmlwidgets)
library(htmltools)
library(leaflet)

install.packages("geojsonio")
library(geojsonio)
origin <- read.csv("C:/Users/Administrator/PycharmProjects/untitled/df2_O_merge.csv",encoding ="gbk")
stations <- read.csv("C:/Users/Administrator/PycharmProjects/untitled/SH_M1M2.csv",encoding ="gbk")

line1 = stations[stations$LINE==1,]
line2 = stations[stations$LINE==2,]
pal <- colorFactor(c("#ED3229","#36B854"), domain = c(1,2))

Shanghai <- leaflet() %>% 
  setView(lng = 121.60, lat = 31.20, zoom = 10) %>% 
  addProviderTiles("CartoDB.Positron") %>%
  addLegend(position = "bottomleft",pal=pal,values = stations$LINE)  %>% 
  addPolylines(data=line1, lng= ~LON, lat = ~LAT, weight =3, color="#ED3229")%>%
  addPolylines(data=line2, lng= ~LON, lat = ~LAT, weight =3, color="#36B854")

Shanghai

# add leaflet-timeline as a dependency
#  to get the js and css
Shanghai$dependencies[[length(Shanghai$dependencies)+1]] <- htmlDependency(
  name = "leaflet-timeline",
  version = "1.0.0",
  src = c("href" = "http://skeate.github.io/Leaflet.timeline/"),
  script = "javascripts/leaflet.timeline.js",
  stylesheet = "stylesheets/leaflet.timeline.css"
)

# use the new onRender in htmlwidgets to run
#  this code once our leaflet map is rendered
#  I did not spend time perfecting the leaflet-timeline
#  options
Shanghai %>%
  setView(lng = 121.60, lat = 31.20, zoom = 10) %>%
  onRender(sprintf(
    '
    function(el,x){
    var power_data = %s;
    
    var timeline = L.timeline(power_data, {
    pointToLayer: function(data, latlng){
    var hue_min = 120;
    var hue_max = 0;
    var hue = hue_min;
    return L.circleMarker(latlng, {
    radius: 10,
    color: "hsl("+hue+", 100%%, 50%%)",
    fillColor: "hsl("+hue+", 100%%, 50%%)"
    });
    },
    steps: 1000,
    duration: 10000,
    showTicks: true
    });
    timeline.addTo(this);
    }
    ',
    origin
  ))
orign %>% arrange()
