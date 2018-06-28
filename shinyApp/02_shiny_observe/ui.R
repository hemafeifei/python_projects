library(shiny)
library(leaflet)

ui <- bootstrapPage(
  tags$style(type="text/css", "html, body {width:100%, height: 100%}"),
  leafletOutput("map", <a class="vglnk" title="Link added by VigLink" href="http://www.amazon.com/gp/search?ie=UTF8&camp=1789&creative=9325&index=aps&keywords=width%2B100&linkCode=ur2" rel="nofollow"><span>width</span><span>="</span><span>100</span><span>%</span></a>", height="100%"),
  absolutePanel(top=10, right = 10,
                selectInput("location", "Community", c("", locs$loc), selected = ""),
                conditionalPanel("input.location !==null && input.location!==''",
                                 actionButton("button_plot_and_table", "View Plot/Table", class="btn-block")))
)