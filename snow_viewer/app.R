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
  date_valid = col_date(format = ""),
  snow = col_number(), # force number
  source = col_character(),
  station = col_character()
)
sh = read_tsv("../data/snow_history.txt", col_types = cs)
#sh = read_tsv("data/snow_history.txt", col_types = cs)
st = unique(sh$station)
today = Sys.Date()

# Define UI for application that draws a histogram
ui <- fillPage(
   
   # Application title
   titlePanel("Snow Viewer"),
   
   # Sidebar with a slider input for number of bins 
   sidebarLayout(
      sidebarPanel(
        dateInput("ded", "Data end date:", value = today),
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
        fluidRow(
          column(10, plotOutput("snow", height = "400px"))
        ),
        fluidRow(
          column(10, DT::dataTableOutput("toptotal"))
        )
      )
   )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
   
   output$snow <- renderPlot({
     tc = seq(0, 100, by = 10)
     if (input$lod == "World") {
       x = sh %>% filter(date_valid <= input$ded)
       ggplot(x, aes(x = factor(as.Date(date_valid)), y = snow)) +
         scale_y_continuous(breaks = tc, minor_breaks = tc, limits = c(0, 100)) + 
         geom_boxplot() +
         theme_bw()
     } else if (input$lod == "Country") {
       xs = sh %>% filter(station == input$station)
       cs = xs$country[1]
       x = sh %>% filter(date_valid <= input$ded & country == cs)
       sm = pmax(10*ceiling((max(x$snow, na.rm = TRUE) + 5)/10), 100)
       tc = seq(0, sm, by = 10)
       ggplot(x, aes(x = factor(as.Date(date_valid)), y = snow, color = country)) +
         scale_y_continuous(breaks = tc, minor_breaks = tc, limits = c(0, sm)) + 
         geom_boxplot() +
         theme_bw()
     } else {
       x = sh %>% filter(date_valid <= input$ded & station == input$station)
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
   
   output$toptotal = DT::renderDataTable({
     ded = max(sh$date_valid, na.rm = TRUE)
     if (input$lod == "World") {
       x = sh %>% filter(!is.na(snow) & date_valid == input$ded) %>% arrange(desc(snow))
       x = x[1:10,]
     } else if (input$lod == "Country") {
       xs = sh %>% filter(station == input$station)
       cs = xs$country[1]
       x = sh %>% filter(!is.na(snow) & date_valid == input$ded & country == cs) %>% arrange(desc(snow))
       x = x[1:10,]
     } else {
       x = sh %>% filter(station == input$station & date_valid == input$ded)
     }
     return(x)
   })
}

# Run the application 
shinyApp(ui = ui, server = server)

