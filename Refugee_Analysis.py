import pandas as pd
import plotly.express as px

# Assuming the data is stored in a DataFrame named 'refugee_data'
# Replace 'data.csv' with the actual file path if the data is in a CSV file
# Read the data into a DataFrame
refugee_data = pd.read_csv('./data/United_Nations_Refugee_Data.csv')

# Display the first few rows of the dataset to understand its structure
print(refugee_data.head())
# Get an overview of the dataset
print(refugee_data.info())

# Summary statistics
print(refugee_data.describe())

# Plotting refugee count by year
fig = px.bar(refugee_data, x='Year', y='Refugees under UNHCR\'s mandate', title='Refugee Count by Year')
fig.show()

# Plotting top countries hosting refugees
top_host_countries = refugee_data.groupby('Country of asylum')['Refugees under UNHCR\'s mandate'].sum().reset_index()
top_host_countries = top_host_countries.sort_values(by='Refugees under UNHCR\'s mandate', ascending=False).head(10)

fig = px.bar(top_host_countries, x='Country of asylum', y='Refugees under UNHCR\'s mandate',
             title='Top 10 Countries Hosting Refugees')
fig.show()

# Grouping data by year and summing up refugee counts
refugee_counts_by_year = refugee_data.groupby('Year')['Refugees under UNHCR\'s mandate'].sum().reset_index()

# Plotting the trend of refugee counts over time
fig = px.line(refugee_counts_by_year, x='Year', y='Refugees under UNHCR\'s mandate',
              title='Evolution of Refugee Counts Over Time')
fig.update_traces(mode='lines+markers')
fig.show()

# Grouping data by year and summing up counts for stateless persons and other concerns
stateless_others_counts = refugee_data.groupby('Year')[['Stateless persons', 'Others of concern']].sum().reset_index()

# Creating a stacked area chart to show the evolution of stateless persons and others of concern
fig = px.area(stateless_others_counts, x='Year', y=['Stateless persons', 'Others of concern'],
              title='Stateless Persons vs Others of Concern Over Time')
fig.show()

# Grouping data by year and summing up counts for stateless persons and other concerns
stateless_others_counts = refugee_data.groupby('Year')[['Stateless persons', 'Others of concern']].sum().reset_index()

# Creating a stacked area chart to show the evolution of stateless persons and others of concern
fig = px.area(stateless_others_counts, x='Year', y=['Stateless persons', 'Others of concern'],
              title='Stateless Persons vs Others of Concern Over Time')
fig.show()

# Filter data for top host countries
top_host_countries = refugee_data.groupby('Country of asylum')['Refugees under UNHCR\'s mandate'].sum().reset_index()
top_host_countries = top_host_countries.sort_values(by='Refugees under UNHCR\'s mandate', ascending=False).head(5)
top_host_country_names = top_host_countries['Country of asylum'].tolist()

# Filter data for the top host countries
filtered_data_top_countries = refugee_data[refugee_data['Country of asylum'].isin(top_host_country_names)]

# Creating a line plot to show refugee counts in top host countries over years
fig = px.line(filtered_data_top_countries, x='Year', y='Refugees under UNHCR\'s mandate',
              color='Country of asylum', title='Refugee Counts in Top Host Countries Over Years')
fig.show()

origin_destination_totals = refugee_data.groupby(['Country of origin', 'Country of asylum (ISO)', 'Year']).sum()["Refugees under UNHCR's mandate"].reset_index()

fig_world_map = px.choropleth(origin_destination_totals, 
                              locations='Country of asylum (ISO)',
                              color='Refugees under UNHCR\'s mandate',
                              animation_frame='Year',
                              title='Refugees Distribution Over Time',
                              color_continuous_scale='Viridis',
                              labels={'Refugees under UNHCR\'s mandate': 'Number of Refugees', 'Country of asylum (ISO)': 'Country of asylum'},
                              category_orders={'Year': sorted(origin_destination_totals['Year'].unique())})

fig_world_map.update_layout(height=800, width=1200)
fig_world_map.show()

origin_totals = refugee_data.groupby(['Country of origin (ISO)', 'Year']).sum()["Refugees under UNHCR's mandate"].reset_index()
fig_world_map_origin = px.choropleth(origin_totals, 
                                     locations='Country of origin (ISO)',
                                     color='Refugees under UNHCR\'s mandate',
                                     animation_frame='Year',
                                     title='Refugees Distribution Over Time (Origin Only)',
                                     color_continuous_scale='Viridis',
                                     labels={'Refugees under UNHCR\'s mandate': 'Number of Refugees', 'Country of origin (ISO)': 'Country of origin'},
                                     category_orders={'Year': sorted(origin_totals['Year'].unique())})

fig_world_map_origin.update_layout(height=800, width=1200)
fig_world_map_origin.show()

