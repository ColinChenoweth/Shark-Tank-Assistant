# Load required libraries
library(shiny)
library(dplyr)
library(ggplot2)
library(readr)  
library(gridExtra)

# Read your dataset
sharktank_data <- read_csv("~/Downloads/SharkTankUSdataset.csv")

# Define UI for application
ui <- fluidPage(
  titlePanel("Learn About A Shark!"),
  sidebarLayout(
    sidebarPanel(
      selectInput("Shark", "Select Shark:", 
                  choices = c("Barbara Corcoran", "Lori Greiner", "Mark Cuban", "Robert Herjavec", "Daymond John", "Kevin O Leary"),
                  selected = "Barbara Corcoran"),
      width = 3  # Adjust the width as needed
    ),
    mainPanel(
      fluidRow(
        column(6, plotOutput("avgInvestmentBarChart", height = 400, width = 900)),  # Adjust the height as needed
        column(6, plotOutput("avgEquityBarChart", height = 400, width = 900))  # Adjust the height as needed
      ),
      fluidRow(
        column(12, verbatimTextOutput("highestInvestment"))
      ),
      fluidRow(
        column(12, plotOutput("pitchInvestmentPieChart", height = 400, width = 900))
      )
    )
  )
)


# Define the server
server <- function(input, output) {
  
  # Filter data based on selected shark
  filtered_data_for_piechart <- reactive({
    sharktank_data %>%
      filter(
        case_when(
          input$Shark == "Barbara Corcoran" ~ !is.na(`Barbara Corcoran Present`),
          input$Shark == "Lori Greiner" ~ !is.na(`Lori Greiner Present`),
          input$Shark == "Mark Cuban" ~ !is.na(`Mark Cuban Present`),
          input$Shark == "Robert Herjavec" ~ !is.na(`Robert Herjavec Present`),
          input$Shark == "Daymond John" ~ !is.na(`Daymond John Present`),
          input$Shark == "Kevin O Leary" ~ !is.na(`Kevin O Leary Present`)
        )
      )
  })
  
  # Create a reactive expression for the pie chart data
  pitchInvestmentData <- reactive({
    num_present <- sum(filtered_data_for_piechart() %>%
                         select(starts_with(input$Shark)) %>%
                         rowSums(na.rm = TRUE) > 0)
    
    num_invested <- sum(!is.na(filtered_data_for_piechart() %>%
                                 select(paste(input$Shark, "Investment Amount"))))
    
    data.frame(
      Category = c("Present and invested", "Present and didn't invest"),
      Count = c(num_invested, num_present - num_invested)
    )
  })
  
  # Render the pie chart plot
  output$pitchInvestmentPieChart <- renderPlot({
    pie_chart_data <- pitchInvestmentData()
    
    if (sum(pie_chart_data$Count) > 0) {
      percentages <- round((pie_chart_data$Count / sum(pie_chart_data$Count)) * 100, 1)
      labels <- paste(
        pie_chart_data$Category,
        sprintf("%.1f%%", percentages)
      )
      
      pie(pie_chart_data$Count, labels = labels, col = c("#5D6D7E", "#AEB6BF"),
          main = paste("Proportion of Pitches Invested In vs. Not Invested In by", input$Shark))
    } else {
      plot(0, type = "n", axes = FALSE, ann = FALSE)
    }
  })
  
  # Filter data based on selected shark
  filtered_data <- reactive({
    sharktank_data %>%
      filter(
        case_when(
          input$Shark == "Barbara Corcoran" ~ !is.na(`Barbara Corcoran Investment Amount`),
          input$Shark == "Lori Greiner" ~ !is.na(`Lori Greiner Investment Amount`),
          input$Shark == "Mark Cuban" ~ !is.na(`Mark Cuban Investment Amount`),
          input$Shark == "Robert Herjavec" ~ !is.na(`Robert Herjavec Investment Amount`),
          input$Shark == "Daymond John" ~ !is.na(`Daymond John Investment Amount`),
          input$Shark == "Kevin O Leary" ~ !is.na(`Kevin O Leary Investment Amount`)
        )
      )
  })
  
  # Create a ggplot bar plot for average investment
  output$avgInvestmentBarChart <- renderPlot({
    # Get a complete set of industries
    all_industries <- unique(sharktank_data$Industry)
    
    # Summarize data to get average investment per industry
    avg_investment <- filtered_data() %>%
      group_by(Industry) %>%
      summarize(avg_investment = mean(case_when(
        input$Shark == "Barbara Corcoran" ~ `Barbara Corcoran Investment Amount`,
        input$Shark == "Lori Greiner" ~ `Lori Greiner Investment Amount`,
        input$Shark == "Mark Cuban" ~ `Mark Cuban Investment Amount`,
        input$Shark == "Robert Herjavec" ~ `Robert Herjavec Investment Amount`,
        input$Shark == "Daymond John" ~ `Daymond John Investment Amount`,
        input$Shark == "Kevin O Leary" ~ `Kevin O Leary Investment Amount`
      ), na.rm = TRUE))
    
    # Merge with all industries to ensure all are included
    avg_investment <- merge(data.frame(Industry = all_industries), avg_investment, all.x = TRUE)
    
    
    # Create a ggplot bar plot with custom appearance for average investment
    p1 <- ggplot(avg_investment, aes(x = Industry, y = avg_investment)) +
      geom_bar(stat = "identity", fill = "#7FB3D5", size = 0.7) +  # Sea green color
      labs(title = paste("Average Investment by", input$Shark),
           x = "Industry",
           y = "Average Investment Amount") +
      theme_classic() +  # Use a classic theme
      theme(
        panel.background = element_rect(fill = "white"),  # Set background color to white
        axis.text.x = element_text(color = "black", angle = 45, hjust = 1),  # Rotate x-axis labels
        axis.text.y = element_text(color = "black"),  # Set y-axis labels color to black
        axis.title = element_text(color = "black", size = 12),  # Set axis title color, font size, and vertical justification
        plot.title = element_text(color = "black", size = 20, hjust = 0.5)  # Set plot title color, font size, center it, and adjust vertical justification
      ) +
      scale_y_continuous(limits = c(0, 800000), expand = c(0, 0))  # Set fixed y-axis limits without a gap
    
    # Output highest investment
    output$highestInvestment <- renderText({
      # Find the row with the highest investment for the selected shark
      max_investment_row <- filtered_data() %>%
        filter(
          case_when(
            input$Shark == "Barbara Corcoran" ~ `Barbara Corcoran Investment Amount`,
            input$Shark == "Lori Greiner" ~ `Lori Greiner Investment Amount`,
            input$Shark == "Mark Cuban" ~ `Mark Cuban Investment Amount`,
            input$Shark == "Robert Herjavec" ~ `Robert Herjavec Investment Amount`,
            input$Shark == "Daymond John" ~ `Daymond John Investment Amount`,
            input$Shark == "Kevin O Leary" ~ `Kevin O Leary Investment Amount`
          ) == max(
            case_when(
              input$Shark == "Barbara Corcoran" ~ `Barbara Corcoran Investment Amount`,
              input$Shark == "Lori Greiner" ~ `Lori Greiner Investment Amount`,
              input$Shark == "Mark Cuban" ~ `Mark Cuban Investment Amount`,
              input$Shark == "Robert Herjavec" ~ `Robert Herjavec Investment Amount`,
              input$Shark == "Daymond John" ~ `Daymond John Investment Amount`,
              input$Shark == "Kevin O Leary" ~ `Kevin O Leary Investment Amount`
            ),
            na.rm = TRUE
          )
        ) %>%
        slice(1)
      
      # Extract industry and investment amount
      industry <- max_investment_row$Industry
      investment <- max_investment_row[[paste(input$Shark, "Investment Amount")]]  # Use the correct column name
      
      # Format the investment amount
      formatted_investment <- format(investment, big.mark = ",", scientific = FALSE)
      
      # Return the text
      paste("Highest Investment by", input$Shark,": $", formatted_investment, "in", industry)
    })
    
    
    
    # Summarize data to get average equity per industry
    avg_equity <- filtered_data() %>%
      group_by(Industry) %>%
      summarize(avg_equity = mean(case_when(
        input$Shark == "Barbara Corcoran" ~ `Barbara Corcoran Investment Equity`,
        input$Shark == "Lori Greiner" ~ `Lori Greiner Investment Equity`,
        input$Shark == "Mark Cuban" ~ `Mark Cuban Investment Equity`,
        input$Shark == "Robert Herjavec" ~ `Robert Herjavec Investment Equity`,
        input$Shark == "Daymond John" ~ `Daymond John Investment Equity`,
        input$Shark == "Kevin O Leary" ~ `Kevin O Leary Investment Equity`
      ), na.rm = TRUE))
    
    # Merge with all industries to ensure all are included
    avg_equity <- merge(data.frame(Industry = all_industries), avg_equity, all.x = TRUE)
    
    
    # Create a ggplot bar plot with custom appearance for average equity
    p2 <- ggplot(avg_equity, aes(x = Industry, y = avg_equity)) +
      geom_bar(stat = "identity", fill = "#2471A3", size = 0.7) +  # Sea green color
      labs(title = paste("Average Equity by", input$Shark),
           x = "Industry",
           y = "Average Equity Amount") +
      theme_classic() +  # Use a classic theme
      theme(
        panel.background = element_rect(fill = "white"),  # Set background color to white
        axis.text.x = element_text(color = "black", angle = 45, hjust = 1),  # Rotate x-axis labels
        axis.text.y = element_text(color = "black"),  # Set y-axis labels color to black
        axis.title = element_text(color = "black", size = 12),  # Set axis title color, font size, and vertical justification
        plot.title = element_text(color = "black", size = 20, hjust = 0.5)  # Set plot title color, font size, center it, and adjust vertical justification
      ) +
      scale_y_continuous(limits = c(0, 50), expand = c(0, 0))  # Set fixed y-axis limits without a gap
    
    # Arrange plots side by side with smaller widths
    grid.arrange(p1, p2, ncol = 2, widths = c(0.4, 0.4))
  })
  
}


# Run the Shiny app
shinyApp(ui, server)
