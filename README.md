# Global Humanitarian Dashboard

A modern, interactive dashboard that visualizes and analyzes global humanitarian data including modern slavery, migration patterns, and refugee statistics.

## Features

- Modern Slavery Analysis
  - Prevalence map by country
  - Regional distribution of modern slavery
  - Top affected countries

- Migration Patterns
  - Net migration trends over time
  - Population vs. migration correlation
  - Migration distribution by country

- Refugee Statistics
  - Global refugee trends
  - Interactive refugee distribution map
  - Top refugee hosting countries

## Script Descriptions

- **Global_slavery_index.py**: Analyzes global slavery data, visualizing the prevalence and distribution of modern slavery.
- **Refugee_Analysis.py**: Analyzes refugee data, visualizing trends and statistics related to refugees.
- **Migration_World_Bank_Report.py**: Analyzes migration data, visualizing population growth and migration trends.

## Setup Instructions

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your web browser and navigate to:
```
http://localhost:5000
```

## Data Sources

- Global Slavery Index 2023
- World Bank Migration Data
- UNHCR Refugee Statistics

## Technologies Used

- Flask
- Dash
- Plotly
- Pandas
- Bootstrap
- Custom CSS

## Project Structure

```
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── static/
│   └── css/
│       └── style.css     # Custom styling
└── data/
    ├── Global_Slavery_Index_2023.csv
    ├── pop_and_net_migration.csv
    └── United_Nations_Refugee_Data.csv
```

## Contributing

Feel free to submit issues and enhancement requests!
