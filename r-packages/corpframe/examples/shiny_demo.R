# corpframe Shiny demo — run with:
#   cd r-packages/corpframe
#   /usr/local/bin/Rscript examples/shiny_demo.R

library(shiny)
library(plotly)
library(ggplot2)

devtools::load_all("../shinycapture")
devtools::load_all(".")

ui <- fluidPage(
  titlePanel("corpframe — Corporate Chart Export (Shiny)"),

  h3("Plotly chart (browser capture)"),
  plotlyOutput("revenue_chart", width = "700px", height = "400px"),
  actionButton("export_plotly", "Export Plotly (Corporate)"),

  hr(),

  h3("ggplot2 chart (server-side rendering)"),
  plotOutput("gg_chart", width = "700px", height = "400px"),
  actionButton("export_gg", "Export ggplot2 (Corporate)"),
)

server <- function(input, output, session) {

  # --- Plotly chart ---
  output$revenue_chart <- renderPlotly({
    plot_ly(
      x = c("Q1", "Q2", "Q3", "Q4"),
      y = c(120, 145, 132, 178),
      type = "bar",
      name = "2025",
      marker = list(color = "#1a1a2e")
    ) %>%
      add_trace(
        y = c(135, 160, 148, 195),
        name = "2026",
        marker = list(color = "#e94560")
      ) %>%
      layout(
        title = "Quarterly Revenue (CHF M)",
        xaxis = list(title = ""),
        yaxis = list(title = "Revenue (CHF M)"),
        barmode = "group"
      )
  })

  # One line — Plotly export with editable fields
  corporate_export_plotly(
    plot_id = "revenue_chart",
    trigger_id = "export_plotly",
    title = "Quarterly Revenue",
    subtitle = "Comparison 2025 vs 2026, all regions",
    footnotes = "Preliminary figures, subject to audit",
    sources = "Source: Internal ERP, March 2026"
  )

  # --- ggplot2 chart ---
  my_gg <- reactive({
    ggplot(mtcars, aes(wt, mpg, color = factor(cyl))) +
      geom_point(size = 3) +
      labs(x = "Weight (1000 lbs)", y = "Miles per Gallon",
           color = "Cylinders") +
      theme_minimal()
  })

  output$gg_chart <- renderPlot({ my_gg() })

  # One line — ggplot2 export with editable fields (no browser capture!)
  corporate_export_gg(
    plot_reactive = my_gg,
    trigger_id = "export_gg",
    title = "Weight vs Fuel Efficiency",
    subtitle = "Motor Trend Car Road Tests, 1974",
    footnotes = "N = 32 observations",
    sources = "Source: R datasets (mtcars)"
  )
}

shinyApp(ui, server)
