import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
from scipy.stats import zscore

df = pd.read_csv("data/pop_and_net_migration.csv")

# df.sample(10)
df.info()

df["Country"].value_counts()

start_year = df["Year"].min()
end_year = df["Year"].max()

print(f"The dataset shows statistics of migration from {start_year} to {end_year}")

# 1. Population Growth Rate (percentage change from previous year)
df['population_growth_rate'] = df.groupby('Country')['total_population'].pct_change() * 100

# 2. Migration Rate (percentage change in net migration)
df['migration_rate'] = df.groupby('Country')['net_migration'].pct_change() * 100

# 3. Population Migration Ratio (net migration / total population)
df['population_migration_ratio'] = df['net_migration'] / df['total_population']

# 4. Total Migration by Country (sum of net migration for each country)
migration_by_country = df.groupby('Country')['net_migration'].sum().reset_index()
migration_by_country = migration_by_country.rename(columns={'net_migration': 'total_migration'})

# Merge the total migration by country back into the main dataframe
df = df.merge(migration_by_country[['Country', 'total_migration']], on='Country', how='left')


fig_population = px.line(
    df,
    x="Year",
    y="total_population",
    color="Country",
    title="Total Population Over the Years",
    labels={"total_population": "Total Population"},
    markers=True,
)

fig_population.update_layout(
    plot_bgcolor="black",    
    paper_bgcolor="black",   
    font_color="white"      
)

fig_population.update_traces(line_shape="spline")  
fig_population.show()

fig_population_trend = px.scatter(
    df,
    x="Year",
    y="total_population",
    color="Country",
    title="Population Trends with Trendlines",
    trendline="ols", 
    labels={"total_population": "Total Population"},
)

fig_population_trend.update_layout(
    plot_bgcolor="black",    
    paper_bgcolor="black",   
    font_color="white"       
)

fig_population_trend.show()

fig_migration = px.line(
    df,
    x="Year",
    y="net_migration",
    color="Country",
    title="Net Migration Trends Over the Years",
    labels={"net_migration": "Net Migration"},
    markers=True,
)

fig_migration.update_layout(
    plot_bgcolor="black",    
    paper_bgcolor="black",   
    font_color="white"       
)

fig_migration.update_traces(line_shape="spline") 
fig_migration.show()

fig_migration_trend = px.scatter(
    df,
    x="Year",
    y="net_migration",
    color="Country",
    title="Net Migration Trends with Trendlines",
    trendline="ols",
    labels={"net_migration": "Net Migration"},
)

fig_migration_trend.update_layout(
    plot_bgcolor="black",    
    paper_bgcolor="black",   
    font_color="white"       
)

fig_migration_trend.show()

fig_total_migration = px.bar(
    migration_by_country,
    x="Country",
    y="total_migration",
    title="Total Migration by Country",
    labels={"total_migration": "Total Migration"},
)

fig_total_migration.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_total_migration.show()

df_sorted_by_years = df.sort_values(by="Year")

fig_population_map = px.choropleth(
    df_sorted_by_years,
    locations="Country",
    locationmode="country names",
    color="total_population",
    hover_name="Country",
    animation_frame="Year",
    color_continuous_scale="Viridis", 
    title="Total Population by Country",
    labels={"total_population": "Total Population"}
)

fig_population_map.update_layout(
    geo=dict(bgcolor="black"), 
    paper_bgcolor="black",      
    font_color="white",        
)

fig_population_map.show()

fig_migration_map = px.choropleth(
    df_sorted_by_years,
    locations="Country",
    locationmode="country names",
    color="net_migration",
    hover_name="Country",
    animation_frame="Year",
    color_continuous_scale="RdBu",  
    title="Net Migration by Country",
    labels={"net_migration": "Net Migration"}
)

fig_migration_map.update_layout(
    geo=dict(bgcolor="black"),  
    paper_bgcolor="black",     
    font_color="white",        
)

fig_migration_map.show()

fig_line = px.line(
    df,
    x="Year",
    y=["total_population", "net_migration"],
    title="Comparative Line Plot: Total Population vs Net Migration",
    labels={"total_population": "Total Population", "net_migration": "Net Migration"},
    line_shape="linear"
)

fig_line.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_line.show()

fig_bar = px.bar(
    df,
    x="Year",
    y=["total_population", "net_migration"],
    title="Comparative Bar Plot: Total Population vs Net Migration by Year",
    labels={"total_population": "Total Population", "net_migration": "Net Migration"},
)

fig_bar.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_bar.show()

fig_box = px.box(
    df,
    x="Year",
    y="total_population",
    title="Box Plot: Distribution of Total Population by Year",
    labels={"total_population": "Total Population"},
)

fig_box.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_box.show()

fig_box_migration = px.box(
    df,
    x="Year",
    y="net_migration",
    title="Box Plot: Distribution of Net Migration by Year",
    labels={"net_migration": "Net Migration"},
)

fig_box_migration.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_box_migration.show()

fig_scatter = px.scatter(
    df,
    x="total_population",
    y="net_migration",
    color="Year",
    title="Scatter Plot: Total Population vs Net Migration",
    labels={"total_population": "Total Population", "net_migration": "Net Migration"},
    color_continuous_scale="Viridis"
)

fig_scatter.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_scatter.show()

fig_scatter = px.scatter(
    df,
    x="total_population",
    y="net_migration",
    color="Country",
    title="Scatter Plot: Total Population vs Net Migration",
    labels={"total_population": "Total Population", "net_migration": "Net Migration"},
    color_continuous_scale="Viridis"
)

fig_scatter.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_scatter.show()

fig_hist_population = px.histogram(
    df,
    x="total_population",
    title="Histogram: Distribution of Total Population",
    labels={"total_population": "Total Population"},
    nbins=40, 
)

fig_hist_population.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_hist_population.show()

fig_kde_population = px.density_contour(
    df,
    x="total_population",
    title="KDE Plot: Distribution of Total Population",
    labels={"total_population": "Total Population"},
)

fig_kde_population.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_kde_population.show()

fig_violin_population = px.violin(
    df,
    x="Year",
    y="total_population",
    box=True,
    points="all",
    color="Country",
    title="Violin Plot: Distribution of Total Population by Year",
    labels={"total_population": "Total Population", "Year": "Year"},
)

fig_violin_population.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_violin_population.show()


fig_hist_migration = px.histogram(
    df,
    x="net_migration",
    title="Histogram: Distribution of Net Migration",
    labels={"net_migration": "Net Migration"},
    nbins=40,
)

fig_hist_migration.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_hist_migration.show()

fig_kde_migration = px.density_contour(
    df,
    x="net_migration",
    title="KDE Plot: Distribution of Net Migration",
    labels={"net_migration": "Net Migration"},
)

fig_kde_migration.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_kde_migration.show()


fig_violin_migration = px.violin(
    df,
    x="Year",
    y="net_migration",
    box=True,
    points="all",
    color="Country",
    title="Violin Plot: Distribution of Net Migration by Year",
    labels={"net_migration": "Net Migration", "Year": "Year"},
)

fig_violin_migration.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_violin_migration.show()

fig_violin = px.violin(
    df,
    y="net_migration",
    x="Country",
    color="Country",
    box=True,
    points="all",
    title="Distribution of Net Migration across Countries",
    labels={"net_migration": "Net Migration"},
)

fig_violin.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_violin.show()


df["yoy_change_population"] = df.groupby("Country")["total_population"].pct_change() * 100
df["yoy_change_migration"] = df.groupby("Country")["net_migration"].pct_change() * 100


fig_line_population = px.line(
    df,
    x="Year",
    y="yoy_change_population",
    color="Country",
    title="Year-on-Year Change in Total Population",
    labels={"yoy_change_population": "YoY Change in Total Population (%)", "Year": "Year"},
)

fig_line_population.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_line_population.show()


fig_bar_population = px.bar(
    df,
    x="Year",
    y="yoy_change_population",
    color="Country",
    title="Year-on-Year Change in Total Population",
    labels={"yoy_change_population": "YoY Change in Total Population (%)", "Year": "Year"},
)

fig_bar_population.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_bar_population.show()


fig_line_migration = px.line(
    df,
    x="Year",
    y="yoy_change_migration",
    color="Country",
    title="Year-on-Year Change in Net Migration",
    labels={"yoy_change_migration": "YoY Change in Net Migration (%)", "Year": "Year"},
)

fig_line_migration.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_line_migration.show()


fig_bar_migration = px.bar(
    df,
    x="Year",
    y="yoy_change_migration",
    color="Country",
    title="Year-on-Year Change in Net Migration",
    labels={"yoy_change_migration": "YoY Change in Net Migration (%)", "Year": "Year"},
)

fig_bar_migration.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_bar_migration.show()

fig_scatter = px.scatter(
    df,
    x="total_population",
    y="net_migration",
    color="Country",
    title="Relationship between Total Population and Net Migration",
    labels={"total_population": "Total Population", "net_migration": "Net Migration"},
)

fig_scatter.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_scatter.show()


fig_bubble = px.scatter(
    df,
    x="total_population",
    y="net_migration",
    size="Year", 
    color="Country",
    title="Relationship between Total Population, Net Migration, and Year (Bubble Plot)",
    labels={"total_population": "Total Population", "net_migration": "Net Migration", "Year": "Year"},
)

fig_bubble.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_bubble.show()

corr_matrix = df[["total_population", "net_migration", "Year"]].corr()

fig_heatmap = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.columns,
    colorscale="Viridis"
))

fig_heatmap.update_layout(
    title="Correlation Matrix between Total Population, Net Migration, and Year",
    xaxis=dict(title="Variables"),
    yaxis=dict(title="Variables"),
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_heatmap.show()


corr_matrix = df[['total_population', 'net_migration']].corr()

fig_heatmap = px.imshow(
    corr_matrix,
    text_auto=True,
    title="Correlation Heatmap between Total Population and Net Migration",
    labels={"x": "Variables", "y": "Variables"}
)

fig_heatmap.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_heatmap.show()

fig_3d = go.Figure(data=[go.Scatter3d(
    x=df["total_population"],
    y=df["net_migration"],
    z=df["Year"],
    mode="markers",
    marker=dict(
        size=12,
        color=df["Year"],
        colorscale="Viridis",
        opacity=0.8
    ),
    text=df["Country"],
)])

fig_3d.update_layout(
    title="3D Scatter Plot: Total Population, Net Migration, and Year",
    scene=dict(
        xaxis_title="Total Population",
        yaxis_title="Net Migration",
        zaxis_title="Year"
    ),
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

# fig_3d.show()

fig_box = px.box(
    df,
    y="total_population",
    color="Country",
    title="Box Plot of Total Population (Identifying Outliers)",
    labels={"total_population": "Total Population"}
)

fig_box.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_box.show()


fig_box_migration = px.box(
    df,
    y="net_migration",
    color="Country",
    title="Box Plot of Net Migration (Identifying Outliers)",
    labels={"net_migration": "Net Migration"}
)

fig_box_migration.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_box_migration.show()


df['z_total_population'] = zscore(df['total_population'])
df['z_net_migration'] = zscore(df['net_migration'])

outliers_population = df[df['z_total_population'].abs() > 3]
outliers_migration = df[df['z_net_migration'].abs() > 3]

fig_scatter_outliers = px.scatter(
    df,
    x="total_population",
    y="net_migration",
    color="Country",
    title="Scatter Plot with Anomalies (Z-Score > 3)",
    labels={"total_population": "Total Population", "net_migration": "Net Migration"}
)

fig_scatter_outliers.add_scatter(
    x=outliers_population['total_population'],
    y=outliers_population['net_migration'],
    mode='markers',
    marker=dict(color='red', size=12, symbol='x'),
    name='Outliers (Population)'
)

fig_scatter_outliers.add_scatter(
    x=outliers_migration['total_population'],
    y=outliers_migration['net_migration'],
    mode='markers',
    marker=dict(color='yellow', size=12, symbol='x'),
    name='Outliers (Migration)'
)

fig_scatter_outliers.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_scatter_outliers.show()


df['z_total_population'] = zscore(df['total_population'])
df['z_net_migration'] = zscore(df['net_migration'])

outliers_population = df[df['z_total_population'].abs() > 3]
outliers_migration = df[df['z_net_migration'].abs() > 3]

fig_scatter_outliers = px.scatter(
    df,
    x="total_population",
    y="net_migration",
    color="Country",
    title="Scatter Plot with Anomalies (Z-Score > 3)",
    labels={"total_population": "Total Population", "net_migration": "Net Migration"}
)

fig_scatter_outliers.add_scatter(
    x=outliers_population['total_population'],
    y=outliers_population['net_migration'],
    mode='markers',
    marker=dict(color='red', size=12, symbol='x'),
    name='Outliers (Population)'
)

fig_scatter_outliers.add_scatter(
    x=outliers_migration['total_population'],
    y=outliers_migration['net_migration'],
    mode='markers',
    marker=dict(color='yellow', size=12, symbol='x'),
    name='Outliers (Migration)'
)

fig_scatter_outliers.update_layout(
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color="white",
)

fig_scatter_outliers.show()
