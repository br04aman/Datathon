from flask import Flask, render_template
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from scipy.stats import zscore

# Initialize Flask app
server = Flask(__name__)

# Initialize Dash app with a modern theme
app = Dash(__name__, server=server, routes_pathname_prefix='/dash/', 
           external_stylesheets=[dbc.themes.CYBORG, dbc.icons.BOOTSTRAP])

# Load all datasets once
slavery_data = pd.read_csv('./data/Global_Slavery_Index_2023.csv')
migration_data = pd.read_csv('./data/pop_and_net_migration.csv')
refugee_data = pd.read_csv('./data/United_Nations_Refugee_Data.csv')

# Clean slavery data
slavery_data.columns = slavery_data.columns.str.strip()
# Fix: Corrected the str.replace() syntax
slavery_data["Population"] = slavery_data["Population"].str.replace(",", "","-").astype(float)
slavery_data["Estimated number of people in modern slavery"] = (
    slavery_data["Estimated number of people in modern slavery"].str.replace(",", "").astype(float)
)

# Fill missing values
slavery_data["Population"].fillna(slavery_data["Population"].median(), inplace=True)
slavery_data["Estimated prevalence of modern slavery per 1,000 population"].fillna(
    slavery_data["Estimated prevalence of modern slavery per 1,000 population"].median(), inplace=True
)
slavery_data["Estimated number of people in modern slavery"].fillna(
    slavery_data["Estimated number of people in modern slavery"].median(), inplace=True
)

# Prepare migration data
migration_data['population_growth_rate'] = migration_data.groupby('Country')['total_population'].pct_change() * 100
migration_data['migration_rate'] = migration_data.groupby('Country')['net_migration'].pct_change() * 100
migration_data['population_migration_ratio'] = migration_data['net_migration'] / migration_data['total_population']
migration_data['z_total_population'] = zscore(migration_data['total_population'])
migration_data['z_net_migration'] = zscore(migration_data['net_migration'])

# Navigation bar with War Analysis link added
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Dashboard", href="/dash/")),
        dbc.NavItem(dbc.NavLink("War Analysis", href="/war-analysis.html")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Refugee Analysis", href="/dash/refugees"),
                dbc.DropdownMenuItem("Migration Trends", href="/dash/migration"),
                dbc.DropdownMenuItem("Slavery Index", href="/dash/slavery"),
            ],
            nav=True,
            in_navbar=True,
            label="Sections",
        ),
    ],
    brand="Global Humanitarian Dashboard",
    brand_href="/",
    color="primary",
    dark=True,
    className="mb-4",
)

# In app.py
# Update the tabs in app.layout to include a "War Analysis" tab

app.layout = dbc.Container([
    navbar,
    dbc.Row([
        dbc.Col(html.H1("Global Humanitarian Dashboard", className="text-center mb-4"), width=12),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Navigation"),
                dbc.CardBody([
                    dcc.Tabs(id="tabs", value="overview", children=[
                        dcc.Tab(label="Overview", value="overview"),
                        dcc.Tab(label="Refugee Analysis", value="refugees"),
                        dcc.Tab(label="Migration Trends", value="migration"),
                        dcc.Tab(label="Slavery Index", value="slavery"),
                        dcc.Tab(label="War Analysis", value="war"),  # Add new tab
                    ]),
                ])
            ], className="mb-4 shadow")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col(html.Div(id="tabs-content"), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.Footer("Data sourced from Global Slavery Index, World Bank, and UNHCR", className="text-center text-muted mt-4 pt-3 border-top"), width=12)
    ])
], fluid=True, className="pb-4")

# Overview dashboard
def overview_dashboard():
    # Create cards with key stats
    refugee_total = refugee_data["Refugees under UNHCR's mandate"].sum()
    slavery_total = slavery_data["Estimated number of people in modern slavery"].sum()
    
    cards = dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Total Refugees", className="text-center"),
            dbc.CardBody([
                html.H2(f"{refugee_total:,.0f}", className="text-center text-primary"),
            ])
        ], className="mb-4 shadow"), width=4),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader("People in Modern Slavery", className="text-center"),
            dbc.CardBody([
                html.H2(f"{slavery_total:,.0f}", className="text-center text-danger"),
            ])
        ], className="mb-4 shadow"), width=4),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader("Countries Analyzed", className="text-center"),
            dbc.CardBody([
                html.H2(f"{len(slavery_data['Country'].unique())}", className="text-center text-success"),
            ])
        ], className="mb-4 shadow"), width=4),
    ])
    
    # Create world map with refugee distribution
    refugee_by_country = refugee_data.groupby("Country of asylum")["Refugees under UNHCR's mandate"].sum().reset_index()
    refugee_map = px.choropleth(refugee_by_country, 
                                locations="Country of asylum",
                                locationmode="country names",
                                color="Refugees under UNHCR's mandate",
                                title="Global Refugee Distribution",
                                color_continuous_scale="Blues",
                                template="plotly_dark")
    
    # Create slavery prevalence map
    slavery_map = px.choropleth(slavery_data, 
                                locations="Country",
                                locationmode="country names",
                                color="Estimated prevalence of modern slavery per 1,000 population",
                                title="Modern Slavery Prevalence per 1,000 Population",
                                color_continuous_scale="Reds",
                                template="plotly_dark")
    
    # Create migration trends visualization
    migration_chart = px.scatter(migration_data,
                               x="total_population", 
                               y="net_migration",
                               color="Country",
                               size="Year",
                               title="Population vs Net Migration",
                               template="plotly_dark")
    
    # Add link to War Analysis page
    war_analysis_link = dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Special Section: War Analysis"),
            dbc.CardBody([
                html.P("Examine the humanitarian impact of armed conflicts with our interactive Power BI dashboard."),
                dbc.Button("Go to War Analysis", href="templates/war-analysis.html", color="danger", className="mt-2")
            ])
        ], className="mb-4 shadow"), width=12)
    ])
    
    return html.Div([
        cards,
        war_analysis_link,  # Add the War Analysis link card
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("About This Dashboard"),
                dbc.CardBody([
                    html.P("""
                        This dashboard provides comprehensive insights into global humanitarian data, 
                        focusing on three critical areas: refugee statistics, migration patterns, and modern slavery.
                        Use the tabs above to explore detailed analysis of each topic.
                    """)
                ])
            ], className="mb-4 shadow"), width=12)
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=refugee_map), width=12, className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=slavery_map), width=6),
            dbc.Col(dcc.Graph(figure=migration_chart), width=6)
        ])
    ])
    
    # Function to generate war analysis content with embedded Power BI
def war_analysis_tab():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("War Analysis Dashboard"),
                    dbc.CardBody([
                        html.P("This dashboard examines the humanitarian impact of armed conflicts worldwide, showing displacement patterns, casualties, and humanitarian aid distribution.")
                    ])
                ], className="mb-4 shadow")
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Iframe(
                        src="https://app.powerbi.com/view?r=eyJrIjoiMjk3MjY1NDMtYjBjMi00Y2YxLTkxNjAtMmUzODI3NzVjOGYyIiwidCI6IjBmOWUzNWRiLTU0NGYtNGY2MC1iZGNjLTVlYTQxNmU2ZGM3MCIsImMiOjh9&pageName=ReportSectiona6258af90d41da03a35a",  # Replace with your actual Power BI embed URL
                        style={
                            "width": "100%", 
                            "height": "700px", 
                            "border": "none",
                            "border-radius": "10px",
                            "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.2)"
                        }
                    )
                ], className="ratio ratio-16x9")
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("About This Analysis"),
                    dbc.CardBody([
                        html.P("This interactive war analysis dashboard visualizes data from multiple conflict zones, highlighting:"),
                        html.Ul([
                            html.Li("Refugee flows and displacement patterns from conflict areas"),
                            html.Li("Civilian vs. military casualties by region "),
                            html.Li("Humanitarian aid allocation and effectiveness"),
                            html.Li("Historical conflict trends and humanitarian outcomes")
                        ]),
                        html.P("Data is sourced from UN OCHA, Uppsala Conflict Data Program, and Armed Conflict Location & Event Data Project (ACLED).")
                    ])
                ], className="mt-4 shadow")
            ], width=12)
        ])
    ])

# Callback for updating tab content
@app.callback(
    Output("tabs-content", "children"),
    Input("tabs", "value")
)
def update_tab(tab_name):
    if tab_name == "overview":
        return overview_dashboard()
    elif tab_name == "refugees":
        return refugee_analysis()
    elif tab_name == "migration":
        return migration_analysis()
    elif tab_name == "slavery":
        return slavery_analysis()
    elif tab_name == "war":
        return war_analysis_tab() 

# Function to generate refugee analysis content with improved visualizations
def refugee_analysis():
    # Refugee count by year
    refugee_counts_by_year = refugee_data.groupby('Year')['Refugees under UNHCR\'s mandate'].sum().reset_index().sort_values(by='Year')

    fig_trend = px.line(refugee_counts_by_year.sort_values('Year'), 
                      x='Year', 
                      y='Refugees under UNHCR\'s mandate',
                      title='Global Refugee Trend Over Time',
                      template="plotly_dark")
    fig_trend.update_traces(mode='lines+markers', line=dict(width=3))
    
    # Top host countries
    top_host_countries = refugee_data.groupby('Country of asylum')['Refugees under UNHCR\'s mandate'].sum().reset_index()
    top_host_countries = top_host_countries.sort_values(by='Refugees under UNHCR\'s mandate', ascending=False).head(10)
    fig_top_countries = px.bar(top_host_countries, 
                             x='Country of asylum', 
                             y='Refugees under UNHCR\'s mandate',
                             title='Top 10 Countries Hosting Refugees',
                             color='Refugees under UNHCR\'s mandate',
                             color_continuous_scale="Blues",
                             template="plotly_dark")
    
    # Refugee map - Fix: Completely rewritten to avoid duplication and undefined variables
    fig_map = None
    if 'Country of asylum (ISO)' in refugee_data.columns:
        # Get unique years for animation
        years = sorted(refugee_data['Year'].unique())
        
        # Create origin-destination data
        origin_destination_totals = refugee_data.groupby(['Country of asylum (ISO)', 'Year']).sum()["Refugees under UNHCR's mandate"].reset_index()
        
        # Create animated map
        fig_map = px.choropleth(origin_destination_totals, 
                              locations='Country of asylum (ISO)',
                              color='Refugees under UNHCR\'s mandate',
                              animation_frame='Year',
                              title='Refugee Distribution By Year',
                              color_continuous_scale='Blues',
                              template="plotly_dark")
        
        # Configure animation settings
        fig_map.update_layout(
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [{
                    'label': 'Play',
                    'method': 'animate',
                    'args': [None, {'frame': {'duration': 1000, 'redraw': True}, 'fromcurrent': True}]
                }]
            }]
        )
        
        # Set slider properties for better year selection
        fig_map.layout.sliders[0].currentvalue = {'prefix': 'Year: ', 'visible': True}
        fig_map.layout.sliders[0].pad = {'t': 50, 'b': 10}
        
        # Create steps for each year
        slider_steps = [
            {'args': [[str(year)], {'frame': {'duration': 300, 'redraw': True}, 'mode': 'immediate'}],
             'label': str(year), 'method': 'animate'} for year in years
        ]
        fig_map.layout.sliders[0].steps = slider_steps
    else:
        # Fallback if ISO codes aren't available
        refugee_by_country = refugee_data.groupby("Country of asylum")["Refugees under UNHCR's mandate"].sum().reset_index()
        fig_map = px.choropleth(refugee_by_country, 
                              locations="Country of asylum",
                              locationmode="country names",
                              color="Refugees under UNHCR's mandate",
                              title="Global Refugee Distribution",
                              color_continuous_scale="Blues",
                              template="plotly_dark")
    
    # Add War Analysis link in the refugee section
    war_link = dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Related Analysis"),
            dbc.CardBody([
                html.P("See how armed conflicts impact refugee patterns in our special war analysis section."),
                dbc.Button("View War Analysis", href="./templates/war-analysis.html", color="danger", className="mt-2")
            ])
        ], className="mb-4 shadow"), width=12)
    ])
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Refugee Analysis"),
                    dbc.CardBody([
                        html.P("This section analyzes global refugee trends based on UNHCR data, showing distribution patterns, top host countries, and changes over time.")
                    ])
                ], className="mb-4 shadow")
            ], width=12)
        ]),
        war_link,  # Add War Analysis link
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_trend), width=12, className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_top_countries), width=6),
            dbc.Col(dcc.Graph(figure=fig_map), width=6)
        ])
    ])

# Function to generate migration analysis content with improved visualizations
def migration_analysis():
    # Migration over time
    fig_line = px.line(migration_data,
                      x="Year",
                      y=["total_population", "net_migration"],
                      title="Total Population vs Net Migration Over Time",
                      template="plotly_dark")
    
    # Population vs Migration scatter
    fig_scatter = px.scatter(migration_data,
                            x="total_population",
                            y="net_migration",
                            color="Country",
                            size="Year",
                            title="Population vs Net Migration",
                            template="plotly_dark")
    
    # Migration rate by country
    migration_by_country = migration_data.groupby('Country')['net_migration'].sum().reset_index()
    migration_by_country = migration_by_country.sort_values(by='net_migration', ascending=False)
    
    fig_bar = px.bar(migration_by_country.head(10),
                    x='Country',
                    y='net_migration',
                    title='Top 10 Countries by Net Migration',
                    color='net_migration',
                    color_continuous_scale="RdBu",
                    template="plotly_dark")
    
    # Identify outliers in migration patterns
    outliers = migration_data[migration_data['z_net_migration'].abs() > 3]
    
    fig_box = px.box(migration_data,
                    y="net_migration",
                    color="Country",
                    title="Net Migration Distribution by Country",
                    template="plotly_dark")
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Migration Analysis"),
                    dbc.CardBody([
                        html.P("This section explores global migration patterns, showing the relationship between population and migration, trends over time, and identifying outliers.")
                    ])
                ], className="mb-4 shadow")
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_line), width=12, className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_scatter), width=6),
            dbc.Col(dcc.Graph(figure=fig_bar), width=6)
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_box), width=12)
        ])
    ])

# Function to generate slavery analysis content with improved visualizations
def slavery_analysis():
    # Distribution of slavery prevalence
    fig_hist = px.histogram(slavery_data, 
                          x="Estimated prevalence of modern slavery per 1,000 population",
                          title="Distribution of Modern Slavery Prevalence",
                          nbins=20,
                          template="plotly_dark")
    
    # Regional aggregation
    total_by_region = slavery_data.groupby("Region")["Estimated number of people in modern slavery"].sum().reset_index()
    fig_bar = px.bar(total_by_region,
                    x='Region',
                    y='Estimated number of people in modern slavery',
                    title='Modern Slavery by Region',
                    color='Estimated number of people in modern slavery',
                    color_continuous_scale="Reds",
                    template="plotly_dark")
    
    # Top 10 countries with highest prevalence
    top_10_prevalence = slavery_data.nlargest(10, "Estimated prevalence of modern slavery per 1,000 population")
    fig_top10 = px.bar(top_10_prevalence,
                      y='Country',
                      x='Estimated prevalence of modern slavery per 1,000 population',
                      title='Top 10 Countries with Highest Modern Slavery Prevalence',
                      orientation='h',
                      color='Estimated prevalence of modern slavery per 1,000 population',
                      color_continuous_scale="Reds",
                      template="plotly_dark")
    
    # World map of slavery prevalence
    fig_map = px.choropleth(slavery_data,
                           locations="Country",
                           locationmode="country names",
                           color="Estimated prevalence of modern slavery per 1,000 population",
                           title="Modern Slavery Prevalence per 1,000 Population",
                           color_continuous_scale="Reds",
                           template="plotly_dark")
    
    # Add War Analysis link in the slavery section
    war_link = dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Related Analysis"),
            dbc.CardBody([
                html.P("Explore the relationship between armed conflicts and modern slavery in our war analysis section."),
                dbc.Button("View War Analysis", href="/war-analysis.html", color="danger", className="mt-2")
            ])
        ], className="mb-4 shadow"), width=12)
    ])
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Modern Slavery Analysis"),
                    dbc.CardBody([
                        html.P("This section analyzes global modern slavery data, showing prevalence distribution, regional totals, and identifying the most affected countries.")
                    ])
                ], className="mb-4 shadow")
            ], width=12)
        ]),
        war_link,  # Add War Analysis link
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_map), width=12, className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_bar), width=6),
            dbc.Col(dcc.Graph(figure=fig_top10), width=6)
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_hist), width=12)
        ])
    ])

# Route for the main page
@server.route('/')
def index():
    return render_template('index.html')

# Route for the War Analysis page
@server.route('/war-analysis.html')
def war_analysis():
    return render_template('war-analysis.html')

if __name__ == '__main__':
    app.run(debug=True)