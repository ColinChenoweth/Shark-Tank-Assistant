library(shiny)
library(plotly)

sharktankdata <- read.csv("Data/SharkTankUSdataset.csv")



ui <- fluidPage(
  titlePanel("Different Values by Industry"),
  sidebarLayout(
    sidebarPanel(
      selectInput("industry", "Select an Industry:", choices = unique(sharktankdata$Industry)),
      radioButtons("data_type", "Select Data:", choices = c("Original Ask Amount", "Valuation Requested"), selected = "Original Ask Amount")
    ),
    mainPanel(
      plotOutput("barChart")
    )
  )
)

server <- function(input, output) {
  output$barChart <- renderPlot({
    filtered_data <- sharktankdata[sharktankdata$Industry == input$industry, ]
    
    if (input$data_type == "Original Ask Amount") {
      data_to_plot <- filtered_data$Original.Ask.Amount
      title <- paste("Original Ask Amount in", input$industry, "Industry")
    } else if (input$data_type == "Valuation Requested") {
      data_to_plot <- filtered_data$Valuation.Requested
      title <- paste("Valuation Requested in", input$industry, "Industry")
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
  
    
    print(bar_chart)
  })
}

shinyApp(ui = ui, server = server)