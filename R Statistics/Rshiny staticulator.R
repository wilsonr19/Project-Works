library(shiny)

library(shinyWidgets)

library(shinythemes)

library(plotly)

ui=fluidPage(
  
  navbarPage(theme=shinytheme("darkly"),titlePanel("STATICULATOR"),
             
             navbarMenu("Data Visualzation",
                        
                        tabPanel("Import file",fileInput("file", h3("Choose a csv file")
                                                         
                        ), 
                        
                        #checkboxInput('header', 'Header', TRUE),
                        
                        radioButtons('sep', 'Separator',
                                     
                                     c(Comma=',',
                                       
                                       Semicolon=';',
                                       
                                       Tab='\t'),
                                     
                                     'Comma'),selectInput("columns","Select a column",""),
                        
                        tabPanel("summary",verbatimTextOutput("summ"))),
                        
                        tabPanel("View data",tableOutput("table1")),
                        
                        tabPanel("Plots",splitLayout(cellWidths=c("50%","50%"),plotlyOutput("plots"),plotlyOutput("plot"))
                                 
                                 
                                 
                                 
                                 
                        )),
             
             tabPanel("Testing of Hypothesis",sidebarLayout(sidebarPanel(
               
               selectInput("columns","Select a column","")),mainPanel())),
             
             tabPanel("Distributions",sidebarLayout(sidebarPanel(
               
               selectInput("columns","Select a column","")),mainPanel()))
             
             
             
  ))



server=function(input,output,session){
  
  
  
  data<-reactive({
    
    file1<-input$file
    
    if(is.null(file1)){return()}
    
    read.table(file=file1$datapath,sep=input$sep,header = T)
    
  })
  
  
  
  output$table1<-renderTable({
    
    if(is.null(data())){return()}
    
    data()
    
  })
  
  
  
  observe({
    
    updateSelectInput(session,"columns",choices = names(data()))
    
  })
  
  
  
  
  
  output$summ<-renderPrint({
    
    if(is.null(input$file)){return()}
    
    summary(data()[ ,input$columns])
    
  })
  
  
  
  output$selectbox<-renderUI({
    
    selectInput(inputId = "column",label = "Select a column",choices = names(data()))
    
  })
  
  
  
  
  
  
  
  output$plots<-renderPlotly({
    
    plots.obj<-data()
    
    x<-list(title=input$columns)
    
    plot_ly(x=plots.obj[[input$columns]],type='box')%>%
      
      layout(
        
        title="Box plot",
        
        xaxis =x
        
      )
    
  })
  
  
  
  output$plot<-renderPlotly({
    
    plot.obj<-data()
    
    x<-list(title=input$columns)
    
    plot_ly(x=plot.obj[[input$columns]],type='histogram')%>%
      
      layout(
        
        title="Histogram",
        
        xaxis =x)
    
    
    
  })
  
  
  
}



shinyApp(ui,server)

