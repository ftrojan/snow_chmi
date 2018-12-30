#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(dplyr)
library(readr)
library(ggplot2)

cs = cols(
  country = col_character(),
  date_valid = col_datetime(format = ""),
  snow = col_number(), # force number
  source = col_character(),
  station = col_character()
)
sh = read_tsv("../data/snow_history.txt", col_types = cs)
st = unique(sh$station)

# Define UI for application that draws a histogram
ui <- fillPage(
   
   # Application title
   titlePanel("Snow Viewer"),
   
   # Sidebar with a slider input for number of bins 
   sidebarLayout(
      sidebarPanel(
        selectInput(
          "station",
          "Search station:",
          choices = st,
          selected = NULL
        ),
         radioButtons(
           "lod",
           "Level of detail:",
          choices = c("World","Country","Station"))
      ),
      
      # Show a plot of the generated distribution
      mainPanel(
        fillRow(
          column(
            10, plotOutput("snow", height = "800px")
          )
        )
      )
   )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
   
   output$snow <- renderPlot({
     tc = seq(0, 100, by = 10)
     if (input$lod == "World") {
       ggplot(sh, aes(x = factor(as.Date(date_valid)), y = snow)) +
         scale_y_continuous(breaks = tc, minor_breaks = tc, limits = c(0, 100)) + 
         geom_boxplot() +
         theme_bw()
     } else if (input$lod == "Country") {
       xs = sh %>% filter(station == input$station)
       cs = xs$country[1]
       x = sh %>% filter(country == cs)
       sm = pmax(10*ceiling((max(x$snow, na.rm = TRUE) + 5)/10), 100)
       tc = seq(0, sm, by = 10)
       ggplot(x, aes(x = factor(as.Date(date_valid)), y = snow, color = country)) +
         scale_y_continuous(breaks = tc, minor_breaks = tc, limits = c(0, sm)) + 
         geom_boxplot() +
         theme_bw()
     } else {
       x = sh %>% filter(station == input$station)
       if (nrow(x) > 0) {
         sm = pmax(10*ceiling((max(x$snow, na.rm = TRUE) + 5)/10), 100)
         tc = seq(0, sm, by = 10)
         ggplot(x, aes(x = date_valid, y = snow, color = source)) +
           scale_y_continuous(breaks = tc, minor_breaks = tc, limits = c(0, sm)) + 
           geom_line(size = 2, alpha = 0.6) + 
           geom_point() +
           theme_bw()
       }
     }
   })
}

# Run the application 
shinyApp(ui = ui, server = server)

