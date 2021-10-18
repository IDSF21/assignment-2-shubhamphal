# Covid-19 Vaccine Analytics Dashboard


### Description
The goal of this project is to provide users with an indepth analysis of the Covid-19 Vaccination status around the world.

The Dashboard solicits data from an open-source [Kaggle](https://www.kaggle.com/gpreda/covid-world-vaccination-progress) dataset and summarizes information at different levels of granularity. In particular, users can choose between viewing the summary statistics at a global level or fine grained  comparative analysis at a country level.

Salient Features:
- Global Level
  - Summary statistics of Total Vaccinations, Number of People Fully Vaccinated and Most Popular Vaccine
  - Interactive Orthographic projection of the World Map to view vaccine distribution with options to filter by choice of metric and date
  - An interactive horizontal stacked column chart showing the Top K regions by vaccine coverage and the proportion of vaccine by manufacturer in each region till a given date. Additional filtering can also be applied by clicking on the names of the vaccine manufacturers to enable/disable them in the current view
  - Distribution statistics of each vaccine by manufacturer
- Country Level
  - Select any country to view if its vaccination statistics per capita are above or below global average
  - An interactive area chart describing the daily vaccination rate of the country with a range based time slider to view vaccination rates at different granularities example, day, month etc
  - An interactive area chart to compare multiple countries on different metrics example total vaccinations per hundred etc.
  - Vaccination data of the country as solicited from the dataset with 'Missing Data' explicity highlighted to uphold the integrity of the analysis.



The project aims to uncover the answers to some interesting questions such as 
> **Which is the most popular vaccine in distribution around the world today?** <br/>
> **How does a country compare against other countries on metrics such as total vaccinations per capita?** <br/>
> **What are the vaccines in use in a given country?**<br/>
> **Which regions have the highest vaccination rates per capita and which vaccines have been distributed in them?** <br/>

### Design decisions
- **Choropleth Map**: As the vaccination data contained vaccine information at the country level and the number of countries is very large I hypothesised that an effective visual encoding must be able to convey all the information pertaining to a country in the most minimalistic fashion and at the same time allow users to visually discern the differences between countries. As such I decided to use a choropleth map to represent this information. Within choropleth maps I had the option to choose between a flat world map or an orthographic projection. To me the orthographic projection seemed highly visually appealing and enabled users to have a higher order of interaction, hence I chose this encoding.
- **Stacked Column Chart**: I wanted to represent the vaccine coverage(distribution) in different regions of the world and at the same time the type of vaccines distributed in each region. This would enable the user to easily understand the dynamics of the global vaccine supply chain. Given the data I considered using bar charts to represent this information but soon realised that this would confound the users as they would have to look at 2 different bar charts to discern which vaccines were most prominently used in the high coverage regions. In this case stacked column charts provided a convinient alternative solution that allowed me to achieve both my goals.
- **Area Chart** In order to visually depict the metrics such as daily vaccination rate, I used an area chart as it allows effective and visually appealing visualizations of time series data. I also used an area chart to compare between the selected country(baseline) and other countries on different metrics as based on the same analogy as stated above




### Development process
The project was developed by me individually. It took me about 15 hours spread across multiple days with an average of 1 hour per day to develop the project. I spent 20% of my time in researching datasets for visualization and getting familiar with the streamlit api. Around 40% of my time in exploratory data analysis and deciding on which aspects of the dataset to focus on for visualization in order to convey maximum information in the most succinct manner. And the rest in developing and deploying the application  
