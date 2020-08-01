library(shiny)
library(shinydashboard)

ui<-dashboardPage(skin = "green",
  #dashboardBody(),
  dashboardHeader(title="Automobile Insurance Fruad Detection Using PCA",titleWidth=500),
  dashboardSidebar(
    sidebarMenu(
      menuItem("Home", tabName = "home", icon = icon("Home")),
      menuItem("Dashboard", tabName = "dashboard", icon = icon("dashboard")),
      menuItem("Widgets", tabName = "widgets", icon = icon("th")),
      menuItem("Charts", tabName = "charts")
    )
  ),
  dashboardBody(
    
  tabItems(
    # First tab content
    tabItem(tabName = "home",
            h3("Auto Mobile Insurance  Fruad Detection and the insurance claimed by the people "),
            tags$img(
              src = "http://stuffshuf.com/wp-content/uploads/2019/05/Automobile-Insurance-USA-Stuffshuf.png",
              height = "100%",
              width="100%")
              #style="position:absolute")
            ),
    tabItem(tabName = "dashboard",
            selectInput("select1", label = h1("Hobbies"), 
                        choices = list("Camping" = 1, "Chess" = 2, "Cross fit" = 3), 
                        selected = 1),
            selectInput("select2", label = h1("Incident-Severity"), 
                        choices = list("Major Damage" = 1, "Others" = 2), 
                        selected = 1),
            selectInput("select3", label = h1("Auto year"), 
                        choices = list("2004" = 1, "Others" = 2), 
                        selected = 1)
    ),
    
    # Second tab content
    tabItem(tabName = "widgets",
            h2("Widgets tab content")
    ),
    tabItem(tabName="charts",
            h2("charts are not available")
            )
  )
)
)

    


server<-function(input,output){
 
  
}
shinyApp(ui,server)


