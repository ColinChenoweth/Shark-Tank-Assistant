library(shiny)
library(plotly)
library(ggplot2)


sharktankdata <- read.csv("C:/Users/tenni/Documents/GitHub/Shark-Tank-Assistant/Data/SharkTankUSdataset.csv")
successfulpitches <- sharktankdata[complete.cases(sharktankdata$Total.Deal.Amount), ]
sharktankdata <- read.csv("Data/SharkTankUSdataset.csv")




ui <- fluidPage(
  titlePanel("Different Values by Industry"),
  sidebarLayout(
    sidebarPanel(
      selectInput("industry", "Select an Industry:", choices = unique(sharktankdata$Industry)),
      radioButtons("data_type", "Select Data:", choices = c("Original Ask Amount", "Valuation Requested",  "Total Deal Amount", "Deal Valuation"), selected = "Original Ask Amount")
    ),
    mainPanel(
      plotOutput("barChart")
    )
  )
)

server <- function(input, output) {
  output$barChart <- renderPlot({
    if (input$data_type == "Original Ask Amount") {
      filtered_data <- sharktankdata[sharktankdata$Industry == input$industry, ]
      data_to_plot <- filtered_data$Original.Ask.Amount
      title <- paste("Original Ask Amount in", input$industry, "Industry")
    } else if (input$data_type == "Valuation Requested") {
      filtered_data <- sharktankdata[sharktankdata$Industry == input$industry, ]
      data_to_plot <- filtered_data$Valuation.Requested
      title <- paste("Valuation Requested in", input$industry, "Industry")
    } else if (input$data_type == "Total Deal Amount") {
      filtered_data <- successfulpitches[successfulpitches$Industry == input$industry, ]
      data_to_plot <- filtered_data$Total.Deal.Amount
      title <- paste("Total Deal Amount in", input$industry, "Industry")
    } else if (input$data_type == "Deal Valuation") {
      filtered_data <- successfulpitches[successfulpitches$Industry == input$industry, ]
      data_to_plot <- filtered_data$Deal.Valuation
      title <- paste("Deal Valuation in", input$industry, "Industry")
    } 

    
    if (input$data_type == "Original Ask Amount") {
      bar_chart <- ggplot(data.frame(Value = data_to_plot), aes(x = Value)) +
        geom_histogram(binwidth = 50000, fill = "sky blue", color = "black") +
        labs(x = input$data_type, y = "Count", title = title) +
        theme_minimal()
    }
    else if (input$data_type == "Valuation Requested") {
      bar_chart <- ggplot(data.frame(Value = data_to_plot), aes(x = Value)) +
        geom_histogram(binwidth = 1000000, fill = "medium sea green", color = "black") +
        labs(x = input$data_type, y = "Count", title = title) +
        theme_minimal()
    }
    else if (input$data_type == "Total Deal Amount") {
      bar_chart <- ggplot(data.frame(Value = data_to_plot), aes(x = Value)) +
        geom_histogram(binwidth = 50000, fill = "light slate blue", color = "black") +
        labs(x = input$data_type, y = "Count", title = title) +
        theme_minimal()
    }
    else if (input$data_type == "Deal Valuation") {
      bar_chart <- ggplot(data.frame(Value = data_to_plot), aes(x = Value)) +
        geom_histogram(binwidth = 1000000, fill = "bisque1", color = "black") +
        labs(x = input$data_type, y = "Count", title = title) +
        theme_minimal()
    } 
    print(bar_chart)
  })
}

shinyApp(ui = ui, server = server)